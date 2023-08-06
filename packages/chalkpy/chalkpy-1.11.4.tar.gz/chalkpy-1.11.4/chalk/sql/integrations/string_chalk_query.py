import typing
from typing import Mapping, Optional, Sequence, Union

import sqlalchemy
from polars import from_arrow
from sqlalchemy import text
from sqlalchemy.sql import selectable

from chalk.features import DataFrame, Feature
from chalk.logging import chalk_logger
from chalk.sql import BaseSQLSourceProtocol, IncrementalSettings
from chalk.sql.base.protocols import CHALK_QUERY_LOGGING, DBSessionProtocol, StringChalkQueryProtocol
from chalk.sql.integrations.chalk_query import (
    Finalizer,
    _construct_features_df,
    _construct_features_single,
    _resolve_implicit_col_feature_mappings,
)
from chalk.utils.duration import Duration


class StringChalkQuery(StringChalkQueryProtocol):
    def __init__(
        self,
        session: DBSessionProtocol,
        source: BaseSQLSourceProtocol,
        query: Union[str, selectable.Selectable],
        fields: Mapping[str, Union[Feature, str]],
        args: Optional[Mapping[str, str]],
    ):
        self._finalizer: Optional[Finalizer] = None
        self._session = session
        self._source = source
        self._original_query = query
        self._query = text(query) if isinstance(query, str) else query
        self._fields = fields
        self._args = args
        self._incremental_settings: Optional[Union[IncrementalSettings, bool]] = None
        if args is not None:
            self._query = self._query.bindparams(**args)

    def __repr__(self):
        return f"StringChalkQuery(query='{self._query}')"

    def one_or_none(self):
        self._finalizer = Finalizer.OneOrNone
        return self

    def one(self):
        self._finalizer = Finalizer.One
        return self

    def first(self):
        self._finalizer = Finalizer.First
        return self

    def all(self):
        self._finalizer = Finalizer.All
        return self

    def incremental(
        self, *, incremental_column: Optional[str] = None, lookback_period: Duration = "0s", mode: str = "row"
    ):
        if mode in {"row", "group"} and incremental_column is None:
            raise ValueError(f"incremental mode set to '{mode}' but no 'incremental_column' argument was passed.")

        if mode == "parameter" and incremental_column is not None:
            raise ValueError(
                f"incremental mode set to '{mode}' but 'incremental_column' argument was passed."
                + " Please view documentation for proper usage."
            )

        self._finalizer = Finalizer.All
        self._incremental_settings = IncrementalSettings(
            lookback_period=lookback_period, incremental_column=incremental_column, mode=mode
        )
        return self

    def execute(self):
        return self.execute_internal(expected_features=[])

    def execute_internal(self, *, expected_features: Sequence[Feature]):
        from chalk.sql import SnowflakeSourceImpl

        if CHALK_QUERY_LOGGING:
            chalk_logger.info(f"Executing query: {self._query}")

        if isinstance(self._source, SnowflakeSourceImpl) and (
            self._finalizer is None or self._finalizer == Finalizer.All
        ):
            return self._execute_internal_snowflake(expected_features=expected_features)
        else:
            return self._execute_internal_sql(expected_features=expected_features)

    def _execute_internal_snowflake(self, expected_features: Sequence[Feature]):
        # this import is safe because the only way we end up here is if we have a valid SnowflakeSource constructed,
        # which already gates this import
        import snowflake.connector

        from chalk.sql import SnowflakeSourceImpl

        source = typing.cast(SnowflakeSourceImpl, self._source)
        with snowflake.connector.connect(
            user=source.user,
            account=source.account_identifier,
            password=source.password,
            warehouse=source.warehouse,
            schema=source.schema,
            database=source.db,
        ) as con:
            cursor = con.cursor().execute(
                self._original_query.replace(":chalk_incremental_timestamp", "%(chalk_incremental_timestamp)s"),
                params=self._args,
            )

            # cursor.description is only available after execute(). If you need column metadata beforehand,
            # consider cursor.describe() https://docs.snowflake.com/en/user-guide/python-connector-example.html#retrieving-column-metadata
            col_names = [c.name for c in cursor.description]
            col_feature_mappings = _resolve_implicit_col_feature_mappings(
                # Note: snowflake by default capitalizes all table and column names, although it's
                # technically possible to disable this behavior by quoting things when creating your schema
                explicit_mappings={k.upper(): v for k, v in self._fields_normalized().items()},
                row_column_names=col_names,
                expected_features=expected_features,
            )

            arrows = cursor.fetch_arrow_all()

            if arrows is None:
                return DataFrame([])

            return DataFrame(
                from_arrow(arrows)
                .drop([col for col, f in zip(col_names, col_feature_mappings) if f is None])
                .rename({col: f.root_fqn for col, f in zip(col_names, col_feature_mappings) if f is not None})
            )

    def _execute_internal_sql(self, expected_features: Sequence[Feature]):
        cursor = self._session.execute(self._query)
        assert isinstance(cursor, sqlalchemy.engine.CursorResult)
        self._finalizer = self._finalizer or Finalizer.All

        if self._finalizer == Finalizer.All:
            rows = cursor.all()
            col_feature_mappings = _resolve_implicit_col_feature_mappings(
                explicit_mappings=self._fields_normalized(),
                expected_features=expected_features,
                row_column_names=list(cursor.keys()),
            )

            return _construct_features_df(col_feature_mappings, rows)

        row = None
        if self._finalizer == Finalizer.One:
            row = cursor.one()

        if self._finalizer == Finalizer.First:
            row = cursor.first()

        if self._finalizer == Finalizer.OneOrNone:
            row = cursor.one_or_none()

        col_feature_mappings = _resolve_implicit_col_feature_mappings(
            explicit_mappings=self._fields_normalized(),
            expected_features=expected_features,
            row_column_names=list(cursor.keys()),
        )

        # We only want to run feature_codecs for StringQuerys, not ChalkQuerys, as SqlAlchemy ORM mappings won't run in this case
        return _construct_features_single(col_feature_mappings, row, _coerce_raw_values=True)

    def _fields_normalized(self):
        return {k: Feature.from_root_fqn(v) if isinstance(v, str) else v for (k, v) in self._fields.items()}

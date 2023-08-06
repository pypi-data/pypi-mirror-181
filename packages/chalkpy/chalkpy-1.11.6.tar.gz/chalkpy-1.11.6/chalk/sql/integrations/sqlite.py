from os import PathLike
from typing import Any, Dict, TypeVar, Union

from sqlalchemy.engine.url import URL

from chalk.client.client_impl import ChalkConfigurationException
from chalk.sql.base.sql_source import BaseSQLSource, TableIngestMixIn

T = TypeVar("T")


def _verify_dep():
    try:
        import aiosqlite
    except ModuleNotFoundError:
        raise ChalkConfigurationException.missing_dependency("chalkpy[sqlite]")
    del aiosqlite


class SQLiteInMemorySourceImpl(BaseSQLSource, TableIngestMixIn):
    def __init__(self):
        _verify_dep()
        super(SQLiteInMemorySourceImpl, self).__init__()
        self.ingested_tables: Dict[str, Any] = {}

    def local_engine_url(self) -> Union[str, URL]:
        return "sqlite:///:memory:?check_same_thread=true"


class SQLiteFileSourceImpl(BaseSQLSource, TableIngestMixIn):
    def __init__(self, filename: Union[PathLike, str]):
        _verify_dep()
        self.filename = filename
        self.ingested_tables: Dict[str, Any] = {}
        super(SQLiteFileSourceImpl, self).__init__()

    def local_engine_url(self) -> Union[str, URL]:
        return f"sqlite:///{str(self.filename)}?check_same_thread=true"

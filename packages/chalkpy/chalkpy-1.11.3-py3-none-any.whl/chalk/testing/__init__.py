import polars.testing

from chalk.features import DataFrame


def assert_frame_equal(a: DataFrame, b: DataFrame):
    return polars.testing.assert_frame_equal(a.to_polars().collect(), b.to_polars().collect())


def _assert_frame_equal_ignore_order(a: DataFrame, b: DataFrame):
    a_polars = a.to_polars().collect()
    b_polars = b.to_polars().collect()
    return polars.testing.assert_frame_equal(
        a_polars.select(sorted(a_polars.columns)), b_polars.select(sorted(b_polars.columns))
    )

import polars
from pydantic import BaseModel

from chalk.features import DataFrame, features
from chalk.streams import KafkaSource, Windowed, stream, windowed


@features
class StoreFeatures:
    id: str
    purchases: Windowed[float] = windowed("10m", "20m")


class KafkaMessage(BaseModel):
    purchase_id: str
    store_id: str
    amount: float


source = KafkaSource(bootstrap_server="server", topic="topic")


@stream(source=source)
def fn(messages: DataFrame[KafkaMessage]) -> DataFrame[StoreFeatures.id, StoreFeatures.purchases]:
    return f"""
        select store_id as id, sum(amount) as purchases
        from {messages}
        group by 1
    """


def test_runs_sql():
    expected = DataFrame(
        polars.DataFrame(
            {
                "store_features.id": ["store1", "store2"],
                "store_features.purchases": [10, 5],
            },
        )
    )
    actual = fn(
        DataFrame(
            polars.DataFrame(
                {
                    "store_id": ["store1", "store2", "store1"],
                    "amount": [4, 5, 6],
                }
            ),
            pydantic_model=KafkaMessage,
        )
    )

    # polars.testing.assert_frame_equal(actual, expected)
    assert expected.to_pyarrow() == actual.to_pyarrow()

import pytest

from chalk import realtime
from chalk.features import DataFrame, features
from chalk.sql import TempSQLiteFileSource
from chalk.testing import assert_frame_equal

sqlite = TempSQLiteFileSource()

seed_db = """
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS friends;

CREATE TABLE users (
    id TEXT,
    name TEXT
);

CREATE TABLE friends_with (
    id INT PRIMARY KEY,
    -- maps to `u_from` feature
    ufrom TEXT,
    -- maps to `u_to` feature
    uto TEXT
);

INSERT INTO users VALUES ('0', 'Wendy'), ('1', 'Shelby');
INSERT INTO friends_with(id, ufrom, uto) VALUES (0, '0', '1'), (1, '1', '2');
"""


@pytest.fixture(scope="module")
def init_db():
    session = sqlite.raw_session()
    for statement in seed_db.split(";"):
        if statement != "":
            session.execute(statement)

    session.commit()


@features
class SQLUserFeatures:
    id: str
    name: str


@features
class SQLFriendsWithRow:
    id: int
    u_from: str
    u_to: str


@realtime
def resolve_sql_users_with_fields() -> DataFrame[SQLUserFeatures.id, SQLUserFeatures.name]:
    return sqlite.query_string(
        """
        SELECT id, name FROM users;
        """,
        fields={"id": SQLUserFeatures.id, "name": SQLUserFeatures.name},
    ).all()


@realtime
def resolve_sql_users_without_fields() -> DataFrame[SQLUserFeatures.id, SQLUserFeatures.name]:
    return sqlite.query_string(
        """
        SELECT id, name FROM users;
        """
    ).all()


@realtime
def resolve_sql_users_without_fields_all() -> DataFrame[SQLUserFeatures]:
    return sqlite.query_string(
        """
        SELECT id, name FROM users;
        """
    ).all()


@realtime
def resolve_friends_with() -> DataFrame[SQLFriendsWithRow]:
    return sqlite.query_string(
        """
        SELECT * FROM friends_with;
        """
    ).all()


def test_sql_resolver_callable(init_db):
    users = resolve_sql_users_with_fields()
    assert_frame_equal(users, DataFrame({SQLUserFeatures.id: ["0", "1"], SQLUserFeatures.name: ["Wendy", "Shelby"]}))


def test_sql_resolver_no_fields_callable(init_db):
    users = resolve_sql_users_without_fields()
    assert_frame_equal(
        users,
        DataFrame({SQLUserFeatures.id: ["0", "1"], SQLUserFeatures.name: ["Wendy", "Shelby"]}),
    )


def test_sql_resolver_no_fields_all_callable(init_db):
    users = resolve_sql_users_without_fields_all()
    assert_frame_equal(
        users,
        DataFrame({SQLUserFeatures.id: ["0", "1"], SQLUserFeatures.name: ["Wendy", "Shelby"]}),
    )


def test_sql_resolver_inexact_implicit_mappings(init_db):
    friends_with = resolve_friends_with()
    assert_frame_equal(
        friends_with,
        DataFrame([SQLFriendsWithRow(id=0, u_from="0", u_to="1"), SQLFriendsWithRow(id=1, u_from="1", u_to="2")]),
    )

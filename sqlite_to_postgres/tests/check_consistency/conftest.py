import pytest
import psycopg2
from psycopg2.extras import DictCursor

from ...conf import app_settings
from ...utils import conn_context


@pytest.fixture
def pg_conn():
    with psycopg2.connect(app_settings.postgres_dsn,
                          cursor_factory=DictCursor) as pg_conn:
        yield pg_conn


@pytest.fixture
def sqlite_conn():
    with conn_context('db.sqlite') as sqlite_conn:
        yield sqlite_conn

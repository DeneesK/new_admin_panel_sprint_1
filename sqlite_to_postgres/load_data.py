import sqlite3
import logging

import psycopg2
from psycopg2.extensions import connection as pg_connection
from psycopg2.extras import DictCursor

from conf import app_settings, LOGGING
from utils import conn_context
from extract_from_sqlite import SQLiteExtractor
from psql_saver import PostgresSaver


logging.basicConfig(**LOGGING)
logger = logging.getLogger()


def load_from_sqlite(connection: sqlite3.Connection,
                     pg_conn: pg_connection,
                     chunk_size: int = app_settings.chunk_size) -> None:
    """Основной метод загрузки данных из SQLite в Postgres"""
    logger.info('etl starts extracting data from sqlite')

    sqlite_extractor = SQLiteExtractor(connection)
    postgres_saver = PostgresSaver(pg_conn)

    data = sqlite_extractor.extract(chunk_size)

    logger.info('etl starts saving data to postgresql')
    for batch in data:
        postgres_saver.save_all_data(batch, chunk_size)


if __name__ == '__main__':
    try:
        with conn_context(app_settings.sqlite_path) \
                as sqlite_conn, \
                psycopg2.connect(app_settings.postgres_dsn,
                                 cursor_factory=DictCursor) as pg_conn:

            load_from_sqlite(sqlite_conn, pg_conn)
    except (sqlite3.DatabaseError, psycopg2.DatabaseError) as ex:
        logger.error('unable to connect to db - %s', ex)

    logger.info('etl has done successfully')

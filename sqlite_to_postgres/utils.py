import sqlite3
from contextlib import contextmanager


@contextmanager
def conn_context(sql_path: str) -> sqlite3.Connection:
    """Context manager for sqlite3 connection"""
    try:
        conn = sqlite3.connect(sql_path)
        conn.row_factory = sqlite3.Row
        yield conn
    finally:
        conn.close()

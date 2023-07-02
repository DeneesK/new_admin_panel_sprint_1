from typing import Iterable
from dataclasses import asdict

from psycopg2 import DatabaseError
from psycopg2.extensions import connection
from psycopg2.extras import execute_batch

from models import FilmWork, Person, PersonFilmwork, Genre, GenreFilmwork
from conf import logging


logger = logging.getLogger()


class PostgresSaver:
    def __init__(self, conn: connection):
        self.conn = conn

    def save_all_data(self, data: Iterable, chunk: int) -> None:
        if isinstance(data[0], FilmWork):
            self._save(data, chunk, 'film_work')
        elif isinstance(data[0], Person):
            self._save(data, chunk, 'person')
        elif isinstance(data[0], Genre):
            self._save(data, chunk, 'genre')
        elif isinstance(data[0], PersonFilmwork):
            self._save(data, chunk, 'person_film_work')
        elif isinstance(data[0], GenreFilmwork):
            self._save(data, chunk, 'genre_film_work')

    def _save(self, data, chunk, name):
        data = [tuple(asdict(f).values()) for f in data]
        curs = self.conn.cursor()
        try:
            number = len(data[0]) - 1
            insert_query = f"""INSERT INTO content.{name}
                            VALUES ({number * '%s,'}%s)
                            ON CONFLICT (id) DO NOTHING"""
            execute_batch(curs, insert_query, data, page_size=chunk)
            self.conn.commit()
        except DatabaseError as ex:
            logger.error('unable to save data - %s', ex)
            curs.close()
        self.conn.commit()
        curs.close()

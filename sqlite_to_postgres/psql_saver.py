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
            self.save_movies(data, chunk)
        elif isinstance(data[0], Person):
            self.save_persons(data, chunk)
        elif isinstance(data[0], Genre):
            self.save_genres(data, chunk)
        elif isinstance(data[0], PersonFilmwork):
            self.save_persons_movies(data, chunk)
        elif isinstance(data[0], GenreFilmwork):
            self.save_genres_movies(data, chunk)

    def save_movies(self, data: Iterable, chunk: int) -> None:
        insert_query = """INSERT INTO content.film_work VALUES (%(id)s,
            %(title)s, %(description)s, %(creation_date)s, %(rating)s,
            %(type)s, %(file_path)s, %(created_at)s, %(updated_at)s)
            ON CONFLICT (id) DO NOTHING"""
        data = [asdict(f) for f in data]
        curs = self.conn.cursor()
        try:
            execute_batch(curs, insert_query, data, page_size=chunk)
            self.conn.commit()
        except DatabaseError as ex:
            logger.error('unable to save data - %s', ex)

    def save_persons(self, data: Iterable, chunk: int) -> None:
        insert_query = """INSERT INTO content.person VALUES (%(id)s,
            %(full_name)s, %(created_at)s, %(updated_at)s)
            ON CONFLICT (id) DO NOTHING"""
        data = [asdict(f) for f in data]
        curs = self.conn.cursor()
        try:
            execute_batch(curs, insert_query, data, page_size=chunk)
            self.conn.commit()
        except DatabaseError as ex:
            logger.error('unable to save data - %s', ex)

    def save_genres(self, data: Iterable, chunk: int) -> None:
        insert_query = """INSERT INTO content.genre VALUES (%(id)s,
            %(name)s, %(description)s, %(created_at)s, %(updated_at)s)
            ON CONFLICT (id) DO NOTHING"""
        data = [asdict(f) for f in data]
        curs = self.conn.cursor()
        try:
            execute_batch(curs, insert_query, data, page_size=chunk)
            self.conn.commit()
        except DatabaseError as ex:
            logger.error('unable to save data - %s', ex)

    def save_genres_movies(self, data: Iterable, chunk: int) -> None:
        insert_query = """INSERT INTO content.genre_film_work VALUES (%(id)s,
            %(film_work_id)s, %(genre_id)s, %(created_at)s)
            ON CONFLICT (id) DO NOTHING"""
        data = [asdict(f) for f in data]
        curs = self.conn.cursor()
        try:
            execute_batch(curs, insert_query, data, page_size=chunk)
            self.conn.commit()
        except DatabaseError as ex:
            logger.error('unable to save data - %s', ex)

    def save_persons_movies(self, data: Iterable, chunk: int) -> None:
        insert_query = """INSERT INTO content.person_film_work VALUES (%(id)s,
        %(role)s, %(film_work_id)s, %(person_id)s, %(created_at)s)
        ON CONFLICT (id) DO NOTHING"""
        data = [asdict(f) for f in data]
        curs = self.conn.cursor()
        try:
            execute_batch(curs, insert_query, data, page_size=chunk)
            self.conn.commit()
        except DatabaseError as ex:
            logger.error('unable to save data - %s', ex)

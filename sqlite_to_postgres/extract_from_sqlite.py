import sqlite3
from sqlite3 import DatabaseError

from typing import Generator

from models import FilmWork, Person, Genre, PersonFilmwork, GenreFilmwork
from conf import logging


logger = logging.getLogger()


class SQLiteExtractor:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def extract_movies(self, chunk: int) -> Generator[
                                                    list[FilmWork],
                                                    None, None
                                                    ]:
        try:
            cur = self.conn.execute('SELECT * FROM film_work')
        except DatabaseError as ex:
            logger.error('unable to extract movies - %s', ex)
        while data := [FilmWork(**dict(f)) for f in cur.fetchmany(chunk)]:
            yield data

    def extract_persons(self, chunk: int) -> Generator[
                                                    list[Person],
                                                    None, None
                                                    ]:
        try:
            cur = self.conn.execute('SELECT * FROM person')
        except DatabaseError as ex:
            logger.error('unable to extract persons - %s', ex)
        while data := [Person(**dict(p)) for p in cur.fetchmany(chunk)]:
            yield data

    def extract_genres(self, chunk: int) -> Generator[
                                                    list[Genre],
                                                    None, None
                                                    ]:
        try:
            cur = self.conn.execute('SELECT * FROM genre')
        except DatabaseError as ex:
            logger.error('unable to extract genres - %s', ex)
        while data := [Genre(**dict(g)) for g in cur.fetchmany(chunk)]:
            yield data

    def extract_genres_movies(self, chunk: int) -> Generator[
                                                    list[GenreFilmwork],
                                                    None, None
                                                    ]:
        try:
            cur = self.conn.execute('SELECT * FROM genre_film_work')
        except DatabaseError as ex:
            logger.error('unable to extract from genre_film_work - %s', ex)
        while data := [GenreFilmwork(**dict(g)) for g in cur.fetchmany(chunk)]:
            yield data

    def extract_persons_movies(self, chunk: int) -> Generator[
                                                    list[PersonFilmwork],
                                                    None, None
                                                    ]:
        try:
            cur = self.conn.execute('SELECT * FROM person_film_work')
        except DatabaseError as ex:
            logger.error('unable to extract from genre_film_work - %s', ex)
        while data := [
                PersonFilmwork(**dict(p)) for p in cur.fetchmany(chunk)
                ]:
            yield data

    def extract(self, chunk: int) -> Generator[
                                        list[FilmWork] | list[Person]
                                        | list[Genre] | list[GenreFilmwork]
                                        | list[PersonFilmwork], None, None
                                        ]:
        for data in self.extract_movies(chunk):
            yield data

        for data in self.extract_persons(chunk):
            yield data

        for data in self.extract_genres(chunk):
            yield data

        for data in self.extract_genres_movies(chunk):
            yield data

        for data in self.extract_persons_movies(chunk):
            yield data

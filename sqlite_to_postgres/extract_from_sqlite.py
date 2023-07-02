import sqlite3
from sqlite3 import DatabaseError

from typing import Generator

from models import FilmWork, Person, Genre, PersonFilmwork,\
                                 GenreFilmwork, models
from conf import logging


logger = logging.getLogger()


class SQLiteExtractor:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.tables_names = self._get_all_tables_names()
        self.models = models

    def _get_all_tables_names(self) -> list[str]:
        curs = self.conn.cursor()
        try:
            names = curs.execute(
                    'SELECT name FROM sqlite_schema WHERE type=\'table\''
            ).fetchall()
        except DatabaseError as ex:
            logger.error('unable to extract from genre_film_work - %s', ex)
        finally:
            curs.close()

        tables_names = [name[0] for name in names]
        tables_names.reverse()
        return tables_names

    def _extractor(self, chunk: int) -> Generator[
                                        list[FilmWork] | list[Person]
                                        | list[Genre] | list[GenreFilmwork]
                                        | list[PersonFilmwork], None, None
                                        ]:
        curs = self.conn.cursor()
        for name in self.tables_names:
            try:
                curs.execute('SELECT * FROM {0}'.format(name))
                while data := [
                    self.models[name](**dict(r)) for r in curs.fetchmany(chunk)
                ]:
                    yield data
            except DatabaseError as ex:
                logger.error('unable to extract from genre_film_work - %s', ex)
                curs.close()
        self.conn.commit()
        curs.close()

    def extract(self, chunk: int) -> Generator[
                                        list[FilmWork] | list[Person]
                                        | list[Genre] | list[GenreFilmwork]
                                        | list[PersonFilmwork], None, None
                                        ]:
        for data in self._extractor(chunk):
            yield data

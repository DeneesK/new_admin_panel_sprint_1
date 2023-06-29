from sqlite3 import Connection as sqlite_connection

from psycopg2.extensions import connection as pg_connection

from ...conf import app_settings


def test_rows_number_equality(pg_conn: pg_connection,
                              sqlite_conn: sqlite_connection):
    sqlite_curs = sqlite_conn.cursor()
    pg_curs = pg_conn.cursor()

    sqlite_rows_number_movies = sqlite_curs.execute(
        'SELECT COUNT(*) FROM film_work'
    ).fetchone()
    pg_curs.execute(
        'SELECT COUNT(*) FROM content.film_work'
    )
    pg__rows_number_movies = pg_curs.fetchone()
    sqlite_rows_number_person = sqlite_curs.execute(
        'SELECT COUNT(*) FROM person'
    ).fetchone()
    pg_curs.execute(
        'SELECT COUNT(*) FROM content.person'
    )
    pg__rows_number_person = pg_curs.fetchone()
    sqlite_rows_number_genre = sqlite_curs.execute(
        'SELECT COUNT(*) FROM genre'
    ).fetchone()
    pg_curs.execute(
        'SELECT COUNT(*) FROM content.genre'
    )
    pg__rows_number_genre = pg_curs.fetchone()
    sqlite_rows_number_genre_film = sqlite_curs.execute(
        'SELECT COUNT(*) FROM genre_film_work'
    ).fetchone()
    pg_curs.execute(
        'SELECT COUNT(*) FROM content.genre_film_work'
    )
    pg__rows_number_genre_film = pg_curs.fetchone()

    assert sqlite_rows_number_movies[0] == pg__rows_number_movies[0]
    assert sqlite_rows_number_person[0] == pg__rows_number_person[0]
    assert sqlite_rows_number_genre[0] == pg__rows_number_genre[0]
    assert sqlite_rows_number_genre_film[0] == pg__rows_number_genre_film[0]


def test_movies_data_equality(pg_conn: pg_connection,
                              sqlite_conn: sqlite_connection):
    sqlite_curs = sqlite_conn.cursor()
    pg_curs = pg_conn.cursor()

    sqlite_movies = sqlite_curs.execute(
        'SELECT * FROM film_work').fetchmany(app_settings.chunk_size)

    pg_curs.execute('SELECT * FROM content.film_work')
    pg_movies = pg_curs.fetchmany(app_settings.chunk_size)

    for sqlite_movie, pg_movie in zip(sqlite_movies, pg_movies):
        sqlite_movie = dict(sqlite_movie)

        assert pg_movie['id'] == sqlite_movie['id']
        assert pg_movie['title'] == sqlite_movie['title']
        assert pg_movie['description'] == sqlite_movie['description']
        assert pg_movie['rating'] == sqlite_movie['rating']
        assert pg_movie['file_path'] == sqlite_movie['file_path']


def test_person_data_equality(pg_conn: pg_connection,
                              sqlite_conn: sqlite_connection):
    sqlite_curs = sqlite_conn.cursor()
    pg_curs = pg_conn.cursor()

    sqlite_persons = sqlite_curs.execute(
        'SELECT * FROM person').fetchmany(app_settings.chunk_size)

    pg_curs.execute('SELECT * FROM content.person')
    pg_persons = pg_curs.fetchmany(app_settings.chunk_size)

    for sqlite_person, pg_person in zip(sqlite_persons, pg_persons):
        sqlite_person = dict(sqlite_person)

        assert pg_person['id'] == sqlite_person['id']
        assert pg_person['full_name'] == sqlite_person['full_name']


def test_genre_data_equality(pg_conn: pg_connection,
                             sqlite_conn: sqlite_connection):
    sqlite_curs = sqlite_conn.cursor()
    pg_curs = pg_conn.cursor()

    sqlite_genres = sqlite_curs.execute(
        'SELECT * FROM genre').fetchmany(app_settings.chunk_size)

    pg_curs.execute('SELECT * FROM content.genre')
    pg_genres = pg_curs.fetchmany(app_settings.chunk_size)

    for sqlite_genre, pg_genre in zip(sqlite_genres, pg_genres):
        sqlite_genre = dict(sqlite_genre)

        assert pg_genre['id'] == sqlite_genre['id']
        assert pg_genre['name'] == sqlite_genre['name']
        assert pg_genre['description'] == sqlite_genre['description']


def test_genre_movie_data_equality(pg_conn: pg_connection,
                                   sqlite_conn: sqlite_connection):
    sqlite_curs = sqlite_conn.cursor()
    pg_curs = pg_conn.cursor()

    sqlite_g_movies = sqlite_curs.execute(
        'SELECT * FROM genre_film_work').fetchmany(app_settings.chunk_size)

    pg_curs.execute('SELECT * FROM content.genre_film_work')
    pg_g_movies = pg_curs.fetchmany(app_settings.chunk_size)

    for sqlite_g_movie, pg_g_movie in zip(sqlite_g_movies, pg_g_movies):
        sqlite_g_movie = dict(sqlite_g_movie)

        assert pg_g_movie['id'] == sqlite_g_movie['id']
        assert pg_g_movie['genre_id'] == sqlite_g_movie['genre_id']
        assert pg_g_movie['film_work_id'] == sqlite_g_movie['film_work_id']

from datetime import date, datetime
from dataclasses import dataclass
from uuid import UUID


@dataclass
class FilmWork:
    id: UUID
    title: str
    description: str
    creation_date: date | None
    file_path: str
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Person:
    id: UUID
    full_name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Genre:
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


@dataclass
class PersonFilmwork:
    id: UUID
    film_work_id: UUID
    person_id: UUID
    role: str
    created_at: datetime


@dataclass
class GenreFilmwork:
    id: UUID
    film_work_id: UUID
    genre_id: UUID
    created_at: datetime


models = {'genre': Genre,
          'genre_film_work': GenreFilmwork,
          'person_film_work': PersonFilmwork,
          'person': Person,
          'film_work': FilmWork,
          }

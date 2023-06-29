from datetime import date, datetime
from dataclasses import dataclass
from uuid import UUID


@dataclass
class BaseMixin:
    id: UUID
    created_at: datetime


@dataclass
class FilmWork(BaseMixin):
    title: str
    description: str
    creation_date: date | None
    file_path: str
    rating: float
    updated_at: datetime
    type: str


@dataclass
class Person(BaseMixin):
    full_name: str
    updated_at: datetime


@dataclass
class Genre(BaseMixin):
    name: str
    description: str
    updated_at: datetime


@dataclass
class PersonFilmwork(BaseMixin):
    role: str
    film_work_id: UUID
    person_id: UUID


@dataclass
class GenreFilmwork(BaseMixin):
    film_work_id: UUID
    genre_id: UUID

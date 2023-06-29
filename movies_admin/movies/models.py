import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(TimeStampedMixin, UUIDMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Person(TimeStampedMixin, UUIDMixin):
    full_name = models.CharField('full_name', max_length=255)

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class Filmwork(TimeStampedMixin, UUIDMixin):

    class FilmType(models.TextChoices):
        TV_SHOW = _('tv_show')
        MOVIE = _('movie')

    title = models.TextField(_('title'), blank=False)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'))
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    person = models.ManyToManyField(Person, through='PersonFilmwork')
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField(_('type'),
                            max_length=255,
                            choices=FilmType.choices,
                            default=FilmType.MOVIE)
    file_path = models.TextField(_('file_path'), blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Film')
        verbose_name_plural = _('Films')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class PersonFilmwork(UUIDMixin):
    class Role(models.TextChoices):
        DIRECTOR = _('director')
        ACTOR = _('actor')
        WRITER = _('writer')

    role = models.CharField(choices=Role.choices, max_length=9)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), choices=Role.choices, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        indexes = [
            models.Index(fields=['film_work_id', 'person_id'],
                         name='film_work_person_idx'),
        ]

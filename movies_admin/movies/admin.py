from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ('genre', )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ['full_name']


class PersonFilmworkInLine(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInLine,)
    list_display = ('title', 'type', 'creation_date', 'rating')
    list_filter = ('type',)
    search_fields = ('title', 'description',)

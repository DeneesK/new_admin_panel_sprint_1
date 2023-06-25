CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone    
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    full_name TEXT,
    created timestamp with time zone,
    modified timestamp with time zone    
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    role TEXT,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    genre_id uuid NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
    created timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    genre_id uuid NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
    created timestamp with time zone
);

CREATE UNIQUE INDEX film_work_creation_date_idx  ON content.film_work (film_work_id, creation_date)
CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id);
CREATE UNIQUE INDEX film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);
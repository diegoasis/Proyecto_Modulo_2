CREATE TABLE proyecto_modulo2.movies (
    id INT PRIMARY KEY,
    budget BIGINT,
    genres TEXT,
    keywords TEXT,
    original_language VARCHAR(10),
    original_title VARCHAR(255),
    overview TEXT,
    popularity DECIMAL(10,4),
    production_companies TEXT,
    production_countries TEXT,
    release_date DATE,
    revenue BIGINT,
    runtime FLOAT,
    spoken_languages TEXT,
    status VARCHAR(50),
    tagline TEXT,
    title VARCHAR(255),
    vote_average DECIMAL(3,1),
    vote_count INT
);

CREATE TABLE proyecto_modulo2.credits (
    movie_id INT PRIMARY KEY,
    title VARCHAR(255),
    cast_members TEXT,
    crew TEXT,
    FOREIGN KEY (movie_id)
    REFERENCES proyecto_modulo2.movies(id)
);
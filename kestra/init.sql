CREATE TABLE employees (
    id_salarie INTEGER PRIMARY KEY,
    nom TEXT,
    prenom TEXT,
    date_naissance DATE,
    bu TEXT,
    date_embauche DATE,
    salaire_brut NUMERIC,
    type_contrat TEXT,
    jours_cp INTEGER,
    adresse_domicile TEXT,
    moyen_deplacement TEXT
);

CREATE TABLE sport_activities_raw (
    id_salarie INTEGER,
    date_activite TIMESTAMP,
    type_activite TEXT,
    distance_km NUMERIC,
    duree_min INTEGER,
    calories INTEGER,
    commentaire TEXT
);

CREATE TABLE IF NOT EXISTS sport_activities_stream (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id_salarie),
    sport_type VARCHAR(50),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    distance_m FLOAT,
    moving_time_s INTEGER,
    elapsed_time_s INTEGER,
    comment TEXT,
    start_lon FLOAT,
    start_lat FLOAT,
    end_lon FLOAT,
    end_lat FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);



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


CREATE TABLE IF NOT EXISTS sport_declaration (
    id_salarie INTEGER PRIMARY KEY REFERENCES employees(id_salarie),
    sport_pratique TEXT
);

CREATE OR REPLACE VIEW vue_kpi_avantages AS
SELECT
    id_salarie,
    nom,
    prenom,
    salaire_brut,
    moyen_deplacement,
    eligible_prime_sportive,
    montant_prime_sportive,
    nb_activites_annee,
    eligible_jours_bien_etre,
    jours_bien_etre
FROM avantages_salaries;

CREATE OR REPLACE VIEW vue_activites_par_mois AS
SELECT
    DATE_TRUNC('month', date_activite) AS mois,
    type_activite,
    COUNT(*) AS nb_activites,
    SUM(distance_km) AS distance_totale_km,
    AVG(distance_km) AS distance_moyenne_km
FROM sport_activities_final
GROUP BY DATE_TRUNC('month', date_activite), type_activite
ORDER BY mois;

CREATE OR REPLACE VIEW vue_synthese_financiere AS
SELECT
    COUNT(*) FILTER (WHERE eligible_prime_sportive) AS nb_salaries_prime,
    SUM(montant_prime_sportive) AS cout_total_prime_sportive,
    COUNT(*) FILTER (WHERE eligible_jours_bien_etre) AS nb_salaries_jours_bien_etre,
    SUM(jours_bien_etre) AS total_jours_bien_etre_accordes,
    COUNT(*) AS nb_salaries_total
FROM avantages_salaries;
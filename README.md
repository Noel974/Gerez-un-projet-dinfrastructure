"# Gerez-un-projet-dinfrastructure" 
powershell -Command "[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('TON_WEBHOOK_SLACK'))"
Créer un environement virtuel python 

.venv\Scripts\activate.bat

## Installation kestra 
Installation kestra via commande 
```bash 
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/kestra-io/kestra/develop/docker-compose.yml" -OutFile "docker-compose.yml"
```
puis lancer l'installation 
```bash
docker compose up -d
```
et de faire la vérification via la commande 
```bash 
docker ps

```

pip install requests pandas openpyxl

pip freeze > requirements.txt

docker exec -it postgres_sportif psql -U kestra -d sportif -c "\dt"

-- 1. Nombre total d'employés
SELECT COUNT(*) AS nb_employees FROM employees;

-- 2. Nombre d'activités "historique" (insérées via le flow Kafka)
SELECT COUNT(*) AS nb_raw FROM sport_activities_raw;

-- 3. Nombre d'activités "streaming" (table sport_activities_stream, si utilisée)
SELECT COUNT(*) AS nb_stream FROM sport_activities_stream;

-- 4. Déclarations sportives (fichier donnee_sportif.xlsx)
SELECT COUNT(*) AS nb_declarations FROM sport_declaration;

-- 5. Table finale fusionnée
SELECT COUNT(*) AS nb_final, source FROM sport_activities_final GROUP BY source;

-- 6. Aperçu des dernières lignes fusionnées
SELECT * FROM sport_activities_final ORDER BY date_activite DESC LIMIT 10;
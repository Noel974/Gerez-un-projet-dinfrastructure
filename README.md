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

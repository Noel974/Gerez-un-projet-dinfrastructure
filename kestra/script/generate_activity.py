import requests
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

# Adresse de l'entreprise (POC)
COMPANY_ADDRESS = "1362 Avenue des Platanes, 34970 Lattes"

def geocode_address(address: str):
    """
    Géocode une adresse en utilisant Nominatim (OpenStreetMap).
    Retourne (lon, lat)
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    if not data:
        raise ValueError(f"Adresse introuvable : {address}")

    return float(data[0]["lon"]), float(data[0]["lat"])


SPORT_TYPES = ["running", "cycling", "walking"]


def get_osrm_route(start, end, profile="foot"):
    """
    Appel OSRM pour obtenir distance + durée entre deux points.
    profile: 'foot' pour marche/course, 'bike' pour vélo.
    """
    url = (
        f"http://router.project-osrm.org/route/v1/{profile}/"
        f"{start[0]},{start[1]};{end[0]},{end[1]}?overview=false"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    route = data["routes"][0]
    return route["distance"], route["duration"]


def generate_activity(employee_id: int, home_address: str):
    """
    Génère une activité sportive réaliste basée sur :
    - géocodage de l'adresse du salarié
    - géocodage de l'entreprise
    - OSRM pour distance + durée
    - Faker pour les dates + commentaires
    """

    # Sport aléatoire
    sport_type = random.choice(SPORT_TYPES)
    profile = "foot" if sport_type in ["running", "walking"] else "bike"

    # Géocodage domicile
    home_coord = geocode_address(home_address)

    # Géocodage entreprise
    company_coord = geocode_address(COMPANY_ADDRESS)

    # Distance + durée via OSRM
    distance_m, duration_s = get_osrm_route(home_coord, company_coord, profile)

    # Dates réalistes
    start_dt = fake.date_time_this_month()
    end_dt = start_dt + timedelta(seconds=duration_s)

    # Commentaire réaliste
    comment = fake.sentence(nb_words=8)

    activity = {
        "employee_id": employee_id,
        "sport_type": sport_type,
        "start_date": start_dt.isoformat(),
        "end_date": end_dt.isoformat(),
        "distance_m": round(distance_m, 2),
        "moving_time_s": int(duration_s),
        "elapsed_time_s": int(duration_s) + random.randint(10, 120),
        "comment": comment,
        "home_address": home_address,
        "home_lon": home_coord[0],
        "home_lat": home_coord[1],
        "company_lon": company_coord[0],
        "company_lat": company_coord[1],
    }

    return activity


def main():
    # Exemple : adresses RH (à remplacer par tes vraies données)
    employees = [
        {"id": 1, "adresse": "25 Rue des Oliviers, Montpellier"},
        {"id": 2, "adresse": "4 Avenue du Stade, Pérols"},
        {"id": 3, "adresse": "10 Rue du Faubourg, Lattes"},
        {"id": 4, "adresse": "12 Boulevard Victor Hugo, Montpellier"},
        {"id": 5, "adresse": "3 Rue des Aigrettes, Castelnau-le-Lez"},
    ]

    for emp in employees:
        activity = generate_activity(emp["id"], emp["adresse"])
        print(activity)


if __name__ == "__main__":
    main()

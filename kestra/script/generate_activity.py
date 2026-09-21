import requests
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

COORDS = [
    (3.9048, 43.5670),  # Lattes
    (3.8767, 43.6108),  # Montpellier centre
    (3.9333, 43.5833),  # Pérols
    (3.9000, 43.6500),  # Castelnau-le-Lez
    (3.8500, 43.6000),  # Saint-Jean-de-Védas
]

SPORT_TYPES = ["running", "cycling", "walking", "hiking"]

CALORIES_PER_MIN = {
    "running": 11,
    "cycling": 8,
    "walking": 5,
    "hiking": 7,
}


def get_osrm_route(start, end, profile="foot"):
    url = (
        f"http://router.project-osrm.org/route/v1/{profile}/"
        f"{start[0]},{start[1]};{end[0]},{end[1]}?overview=false"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    route = data["routes"][0]
    return route["distance"], route["duration"]


def generate_activity(employee_id: int, historical: bool = False):
    sport_type = random.choice(SPORT_TYPES)
    profile = "foot" if sport_type in ["running", "walking", "hiking"] else "bike"

    start = random.choice(COORDS)
    end = random.choice(COORDS)

    distance_m, duration_s = get_osrm_route(start, end, profile)

    if historical:
        start_dt = fake.date_time_between(start_date='-365d', end_date='now')
    else:
        start_dt = fake.date_time_between(start_date='-1h', end_date='now')

    end_dt = start_dt + timedelta(seconds=duration_s)

    if sport_type == "hiking":
        comment = f"Randonnée de {fake.city()}, je vous la conseille c'est top"
    else:
        comment = fake.sentence(nb_words=8)

    # Échappe les apostrophes pour éviter de casser les requêtes SQL en aval
    comment = comment.replace("'", "''")

    calories = round((duration_s / 60) * CALORIES_PER_MIN[sport_type])

    activity = {
        "employee_id": employee_id,
        "sport_type": sport_type,
        "start_date": start_dt.isoformat(),
        "end_date": end_dt.isoformat(),
        "distance_m": round(distance_m, 2),
        "distance_km": round(distance_m / 1000, 1),
        "moving_time_s": int(duration_s),
        "moving_time_min": round(duration_s / 60),
        "elapsed_time_s": int(duration_s) + random.randint(10, 120),
        "comment": comment,
        "calories": calories,
        "start_lon": start[0],
        "start_lat": start[1],
        "end_lon": end[0],
        "end_lat": end[1],
        "historical": historical,
    }

    return activity
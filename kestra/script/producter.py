import json
import time
import random
from confluent_kafka import Producer
import psycopg2
from generate_activity import generate_activity

producer_conf = {
    "bootstrap.servers": "localhost:19092",
    "client.id": "sport-activity-producer",
}

producer = Producer(producer_conf)
TOPIC = "strava.activities"


def get_real_employee_ids():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="sportif",
        user="kestra",
        password="kestra"
    )
    cur = conn.cursor()
    cur.execute("SELECT id_salarie FROM employees;")
    ids = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return ids


def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Erreur d'envoi: {err}")


def send_activity_to_redpanda(activity: dict):
    producer.produce(
        topic=TOPIC,
        value=json.dumps(activity).encode("utf-8"),
        callback=delivery_report
    )
    producer.poll(0)


def load_historical(employee_ids, nb_activites=3000):
    """Charge un historique de 12 mois, sans notification Slack (historical=True)."""
    print(f"📦 Génération de {nb_activites} activités historiques (12 derniers mois)...")
    for i in range(nb_activites):
        employee_id = random.choice(employee_ids)
        activity = generate_activity(employee_id, historical=True)
        send_activity_to_redpanda(activity)
        if i % 100 == 0:
            print(f"  {i}/{nb_activites} activités envoyées...")
    producer.flush()
    print("✅ Historique chargé.")


def simulate_live(employee_ids, nb_activites=20, delay=1):
    """Simule un flux temps réel, avec notification Slack (historical=False)."""
    print(f"📡 Simulation de {nb_activites} activités en temps réel...")
    for _ in range(nb_activites):
        employee_id = random.choice(employee_ids)
        activity = generate_activity(employee_id, historical=False)
        print(f"Envoi activité: {activity}")
        send_activity_to_redpanda(activity)
        time.sleep(delay)
    producer.flush()
    print("🏁 Simulation terminée.")


def main():
    print("🚀 Producteur Redpanda démarré…")
    employee_ids = get_real_employee_ids()
    print(f"📋 {len(employee_ids)} employés trouvés en base.")

    print("\nQue veux-tu faire ?")
    print("1 - Charger l'historique 12 mois (silencieux, pas de Slack)")
    print("2 - Simuler un flux temps réel (avec Slack)")
    choice = input("Choix (1/2) : ").strip()

    if choice == "1":
        load_historical(employee_ids, nb_activites=3000)
    elif choice == "2":
        simulate_live(employee_ids, nb_activites=20, delay=1)
    else:
        print("Choix invalide.")


if __name__ == "__main__":
    main()
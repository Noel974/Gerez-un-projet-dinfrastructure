import json
import time
from confluent_kafka import Producer
from generate_activity import generate_activity

# Configuration Redpanda / Kafka
producer_conf = {
    "bootstrap.servers": "localhost:19092",
    "client.id": "sport-activity-producer",
}

producer = Producer(producer_conf)

TOPIC = "strava.activities"


def delivery_report(err, msg):
    """Callback pour confirmer la livraison."""
    if err is not None:
        print(f"❌ Erreur d'envoi: {err}")
    else:
        print(f"✔ Activité envoyée dans {msg.topic()} [partition {msg.partition()}]")


def send_activity_to_redpanda(activity: dict):
    """Envoie une activité dans Redpanda."""
    producer.produce(
        topic=TOPIC,
        value=json.dumps(activity).encode("utf-8"),
        callback=delivery_report
    )
    producer.poll(0)


def main():
    print("🚀 Producteur Redpanda démarré…")

    # 🔥 Adresses RH réalistes (à remplacer par ton fichier RH ou PostgreSQL)
    employees = [
        {"id": 1, "adresse": "25 Rue des Oliviers, Montpellier"},
        {"id": 2, "adresse": "4 Avenue du Stade, Pérols"},
        {"id": 3, "adresse": "10 Rue du Faubourg, Lattes"},
        {"id": 4, "adresse": "12 Boulevard Victor Hugo, Montpellier"},
        {"id": 5, "adresse": "3 Rue des Aigrettes, Castelnau-le-Lez"},
        # Ajoute jusqu'à 20 employés si tu veux
    ]

    for emp in employees:
        activity = generate_activity(emp["id"], emp["adresse"])
        print(f"Envoi activité: {activity}")
        send_activity_to_redpanda(activity)
        time.sleep(1)  # simulation streaming

    producer.flush()
    print("🏁 Toutes les activités ont été envoyées.")


if __name__ == "__main__":
    main()

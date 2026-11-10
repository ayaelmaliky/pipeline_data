
import json
import re
import ipaddress
import psycopg
from getpass import getpass

from ingestion import raw
from process import extract_transforme
from process import geolocation


def toJson():
    rows = raw.toRows("data")
    data = []

    for row in rows:
        result = extract_transforme.extract(row)

        if result:
            data.append(result)

    with open("storage/data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print("Conversion de auth.log vers JSON terminée !")
    print("Nombre de lignes traitées :", len(data))

    return data


def save_to_postgresql(data):
    password = getpass("Mot de passe PostgreSQL : ")

    try:
        with psycopg.connect(
            dbname="log_analyzer",
            user="postgres",
            password=password,
            host="localhost",
            port=5432
        ) as conn:

            with conn.cursor() as cursor:

                # Supprimer les anciennes données
                cursor.execute("TRUNCATE TABLE logs RESTART IDENTITY")

                # Enregistrer les nouvelles données
                for item in data:
                    cursor.execute(
                        """
                        INSERT INTO logs
                        (month, day, event_time, message)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            item["month"],
                            item["day"],
                            item["time"],
                            item["message"]
                        )
                    )

        print("Enregistrement dans PostgreSQL réussi !")
        print("Nombre de lignes enregistrées :", len(data))

    except psycopg.Error as error:
        print("Erreur PostgreSQL :", error)


def get_ips(data):
    ips = set()

    for item in data:
        message = item["message"]

        found_ips = re.findall(
            r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            message
        )

        for ip in found_ips:
            try:
                ipaddress.ip_address(ip)
                ips.add(ip)
            except ValueError:
                pass

    return ips


def save_geolocation(data):
    ips = get_ips(data)

    password = getpass("Mot de passe PostgreSQL : ")

    try:
        with psycopg.connect(
            dbname="log_analyzer",
            user="postgres",
            password=password,
            host="localhost",
            port=5432
        ) as conn:

            with conn.cursor() as cursor:

                # Récupérer les IP déjà enregistrées
                cursor.execute(
                    "SELECT ip_address FROM ip_geolocation"
                )

                existing_ips = {
                    row[0] for row in cursor.fetchall()
                }

                count = 0
                requests_count = 0

                # Traiter 5 nouvelles IP maximum
                for ip in sorted(ips):

                    if ip in existing_ips:
                        continue

                    if not ipaddress.ip_address(ip).is_global:
                        continue

                    if requests_count >= 5:
                        break

                    requests_count += 1

                    result = geolocation.get_geolocation(ip)

                    if result and result.get("success"):
                        country = result.get("country")

                        cursor.execute(
                            """
                            INSERT INTO ip_geolocation
                            (ip_address, country)
                            VALUES (%s, %s)
                            ON CONFLICT (ip_address) DO NOTHING
                            """,
                            (ip, country)
                        )

                        count += 1
                        existing_ips.add(ip)

                print("Géolocalisation terminée !")
                print("Nombre de nouveaux IP enregistrés :", count)

    except psycopg.Error as error:
        print("Erreur PostgreSQL :", error)


if __name__ == "__main__":
    data = toJson()
    save_to_postgresql(data)
    save_geolocation(data)

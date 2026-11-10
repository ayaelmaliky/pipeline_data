import psycopg
from getpass import getpass

try:
    password = getpass("Mot de passe PostgreSQL : ")

    conn = psycopg.connect(
        dbname="log_analyzer",
        user="postgres",
        password=password,
        host="localhost",
        port=5432
    )

    print("Connexion à PostgreSQL réussie !")

    cursor = conn.cursor()
    cursor.execute("SELECT current_database(), current_user")

    result = cursor.fetchone()
    print("Base de données :", result[0])
    print("Utilisateur :", result[1])

    cursor.close()
    conn.close()

except psycopg.Error as error:
    print("Erreur de connexion :", error)
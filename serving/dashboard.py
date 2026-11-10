
import psycopg
import matplotlib.pyplot as plt
from getpass import getpass


# Connexion à PostgreSQL
def connect_db():
    password = getpass("Mot de passe PostgreSQL : ")

    conn = psycopg.connect(
        dbname="log_analyzer",
        user="postgres",
        password=password,
        host="localhost",
        port=5432
    )

    return conn


# Récupération et affichage des données
def show_dashboard():

    conn = connect_db()

    try:
        with conn.cursor() as cursor:

            # 1. Échecs par pays
            cursor.execute("""
                SELECT
                    g.country,
                    COUNT(*) AS total
                FROM logs l
                JOIN ip_geolocation g
                    ON SPLIT_PART(
                        SPLIT_PART(l.message, ' from ', 2),
                        ' ',
                        1
                    ) = g.ip_address
                WHERE l.message LIKE '%Failed password%'
                GROUP BY g.country
                ORDER BY total DESC
            """)

            countries_data = cursor.fetchall()


            # 2. Réussites par utilisateur
            cursor.execute("""
                SELECT
                    SPLIT_PART(
                        SPLIT_PART(
                            message,
                            'Accepted password for ',
                            2
                        ),
                        ' from ',
                        1
                    ) AS username,
                    COUNT(*) AS total
                FROM logs
                WHERE message LIKE '%Accepted password for %'
                GROUP BY 1
                ORDER BY total DESC
            """)

            success_data = cursor.fetchall()


            # 3. Échecs avec utilisateur invalide
            cursor.execute("""
                SELECT
                    SPLIT_PART(
                        SPLIT_PART(message, 'invalid user ', 2),
                        ' from ',
                        1
                    ) AS username,
                    COUNT(*) AS total
                FROM logs
                WHERE message LIKE '%Failed password for invalid user%'
                GROUP BY 1
                ORDER BY total DESC
                LIMIT 10
            """)

            invalid_data = cursor.fetchall()


        # Création de la fenêtre Dashboard
        fig, axes = plt.subplots(1, 3, figsize=(18, 7))

        fig.suptitle(
            "Dashboard - Analyse des logs SSH",
            fontsize=18,
            fontweight="bold"
        )


        # Graphique 1 : Échecs par pays
        countries = [row[0] for row in countries_data]
        country_totals = [row[1] for row in countries_data]

        if countries_data:
            axes[0].bar(countries, country_totals)
        else:
            axes[0].text(0.5, 0.5, "Aucune donnée disponible",
                         ha="center", va="center")

        axes[0].set_title("Échecs par pays")
        axes[0].set_xlabel("Pays")
        axes[0].set_ylabel("Nombre d'échecs")
        axes[0].tick_params(axis="x", rotation=45)


        # Graphique 2 : Réussites par utilisateur
        users = [row[0] for row in success_data]
        success_totals = [row[1] for row in success_data]

        if success_data:
            axes[1].bar(users, success_totals)
        else:
            axes[1].text(0.5, 0.5, "Aucune donnée disponible",
                         ha="center", va="center")

        axes[1].set_title("Réussites par utilisateur")
        axes[1].set_xlabel("Utilisateur")
        axes[1].set_ylabel("Nombre de réussites")
        axes[1].tick_params(axis="x", rotation=45)


        # Graphique 3 : Échecs avec utilisateur invalide
        invalid_users = [row[0] for row in invalid_data]
        invalid_totals = [row[1] for row in invalid_data]

        if invalid_data:
            axes[2].bar(invalid_users, invalid_totals)
        else:
            axes[2].text(0.5, 0.5, "Aucune donnée disponible",
                         ha="center", va="center")

        axes[2].set_title("Échecs avec utilisateur invalide")
        axes[2].set_xlabel("Utilisateur invalide")
        axes[2].set_ylabel("Nombre d'échecs")
        axes[2].tick_params(axis="x", rotation=45)


        # Ajustement et affichage
        plt.tight_layout()
        plt.show()

    finally:
        conn.close()


# Programme principal
if __name__ == "__main__":
    show_dashboard()

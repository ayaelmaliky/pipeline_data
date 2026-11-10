
                            Log Analyzer

 1. Présentation du projet

Log Analyzer est un projet réalisé en Python qui permet d'analyser les fichiers de logs d'un système Linux.

Le projet utilise le fichier `auth.log`, qui contient les informations sur les tentatives de connexion des utilisateurs. L'objectif est de traiter ces informations pour détecter les connexions réussies, les tentatives échouées et les utilisateurs invalides.

Les résultats sont ensuite enregistrés dans une base de données PostgreSQL et affichés sous forme de graphiques avec Matplotlib.

2. Objectifs du projet

Les principaux objectifs de ce projet sont :

- Lire et traiter les fichiers de logs.
- Extraire les informations importantes des lignes de logs.
- Identifier les tentatives de connexion réussies et échouées.
- Détecter les tentatives avec des utilisateurs invalides.
- Récupérer le pays associé aux adresses IP.
- Enregistrer les données dans PostgreSQL.
- Afficher les résultats dans un Dashboard.

 3. Architecture du projet

Le projet est organisé en plusieurs dossiers :

 ingestion

Ce dossier permet de lire les fichiers de logs, y compris les fichiers compressés en gzip.

 process

Ce dossier contient les fonctions qui permettent d'extraire les informations des logs et de récupérer la localisation des adresses IP.

 storage

Ce dossier permet de convertir les données en JSON et de les enregistrer dans la base de données PostgreSQL.

 serving

Ce dossier contient le Dashboard qui permet de visualiser les résultats avec Matplotlib.

 4. Technologies utilisées

Les technologies utilisées dans ce projet sont :

- Python : langage utilisé pour développer le projet.
- PostgreSQL : système de gestion de base de données.
- Psycopg : connexion entre Python et PostgreSQL.
- Matplotlib : création des graphiques.
- Requests : récupération des informations de géolocalisation.
- JSON : format utilisé pour enregistrer les données.

 5. Fonctionnement du projet

Le traitement des données se fait en plusieurs étapes :

1. Lecture des fichiers `auth.log` depuis le dossier data.
2. Extraction des informations importantes à partir des lignes de logs.
3. Récupération des adresses IP et de leur localisation.
4. Conversion des données extraites en fichier JSON.
5. Enregistrement des informations dans PostgreSQL.
6. Analyse des données et affichage des résultats dans le Dashboard.

 6. Dashboard

Le Dashboard contient trois graphiques principaux :

1. Échecs par pays

Ce graphique représente le nombre de tentatives de connexion échouées selon le pays associé à l'adresse IP.

 2. Réussites par utilisateur

Ce graphique affiche le nombre de connexions réussies pour chaque utilisateur.

 3. Échecs avec utilisateur invalide

Ce graphique représente les tentatives de connexion échouées avec des noms d'utilisateurs qui n'existent pas.

 7. Base de données

Le projet utilise PostgreSQL avec deux tables principales :

- `logs` : contient les informations extraites des fichiers de logs.
- `ip_geolocation` : contient les adresses IP et les pays correspondants.

 8. Exécution du projet

Pour lancer le projet, il faut d'abord activer l'environnement virtuel et installer les dépendances nécessaires.

Ensuite, exécuter les commandes depuis le dossier principal du projet.

Pour lancer le traitement et enregistrer les données :

```bash
python -m storage.database
```

Pour lancer le Dashboard :

```bash
python -m serving.dashboard
```

Le Dashboard affiche les trois graphiques dans une seule fenêtre.

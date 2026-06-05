"""
Script d'export de données de MongoDB en .csv
"""
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# === CONFIG PATH ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fonctions.connexion_mongodb import connect_mongodb, disconnect_mongodb
from fonctions.export_from_mongodb import export_mongodb


load_dotenv(".env") #charge le fichier .env
load_dotenv(".env.secrets") #charge le fichier .env.secrets

## PARAMÈTRES POUR L'EXPORT
env = os.getenv("ENV", "local")

if env == "docker":
    PATH_CSV = os.getenv("DOCKER_PATH_CSV")
else:
    PATH_CSV = os.getenv("LOCAL_PATH_CSV")
#ajout du DOCKER_PATH_CSV pour que cela fonctionne aussi avec Docker.

# Chargement des données d'identification
user = os.getenv("APP_MIGRATION_USER")
password = os.getenv("APP_MIGRATION_PASSWORD")
if env=="docker":
    host = os.getenv("MONGO_HOST_DOCKER")
else:
    host = os.getenv("MONGO_HOST_LOCAL")

port = os.getenv("MONGO_PORT")

DB_NAME = os.getenv("DB_NAME")
MONGO_URI = f"mongodb://{user}:{password}@{host}:{port}/{DB_NAME}?authSource={DB_NAME}"

COLLECTION_NAME = os.getenv("COLLECTION_NAME")
COLLECTION_NAME_AGE = os.getenv("COLLECTION_NAME_AGE")
COLLECTION_NAME_BILL = os.getenv("COLLECTION_NAME_BILL")
COLLECTION_NAME_DATES = os.getenv("COLLECTION_NAME_DATES")



def main():


    # 1. Connexion à MongoDB
    client = connect_mongodb(MONGO_URI)
    print("=====================================================================================")

    #2. Export de données
    export_mongodb(client, name_database=DB_NAME,name_collection=COLLECTION_NAME,filtre={}, limite=None)
    export_mongodb(client, name_database=DB_NAME,name_collection=COLLECTION_NAME_AGE,filtre={}, limite=None)
    export_mongodb(client, name_database=DB_NAME,name_collection=COLLECTION_NAME_BILL,filtre={}, limite=None)
    export_mongodb(client, name_database=DB_NAME,name_collection=COLLECTION_NAME_DATES,filtre={}, limite=None)

    print("=====================================================================================")
    
    # 3. Déconnexion
    disconnect_mongodb(MONGO_URI)
    print("Export terminé.")

if __name__ == "__main__":
    main()
"""
Script de suppression de collection
"""
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# === CONFIG PATH ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fonctions.connexion_mongodb import connect_mongodb, disconnect_mongodb
from fonctions.crud_mongodb import delete_documents


load_dotenv(".env") #charge le fichier .env
load_dotenv(".env.secrets") #charge le fichier .env

## PARAMÈTRES POUR LA MIGRATION
env = os.getenv("ENV", "local")

if env == "docker":
    PATH_CSV = os.getenv("DOCKER_PATH_CSV")
else:
    PATH_CSV = os.getenv("LOCAL_PATH_CSV")
#ajout du DOCKER_PATH_CSV pour que cela fonctionne aussi avec Docker.

# Chargement des données d'identification
user = os.getenv("ADMIN_USER")
password = os.getenv("ADMIN_PASSWORD")
if env=="docker":
    host = os.getenv("MONGO_HOST_DOCKER")
else:
    host = os.getenv("MONGO_HOST_LOCAL")

port = os.getenv("MONGO_PORT")

DB_NAME = os.getenv("DB_NAME")
MONGO_URI = f"mongodb://{user}:{password}@{host}:{port}/{DB_NAME}?authSource={DB_NAME}"

COLLECTION_NAME = os.getenv("COLLECTION_NAME")





def main():
    # 1. Connexion à MongoDB
    client = connect_mongodb(MONGO_URI)
    print("=====================================================================================")
    
    # 2. suppression de toute la collection
    delete_documents(client,name_database=DB_NAME,name_collection=COLLECTION_NAME, recherche={}, one=False)
    print("=====================================================================================")
    
    # 3. Déconnexion
    disconnect_mongodb(MONGO_URI)
    print("Suppression terminée.")

if __name__ == "__main__":
    main()
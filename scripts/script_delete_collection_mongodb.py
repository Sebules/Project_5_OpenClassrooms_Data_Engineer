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


load_dotenv() #charge le fichier .env

## PARAMÈTRES POUR LA MIGRATION
env = os.getenv("ENV", "local")

if env == "docker":
    PATH_CSV = os.getenv("DOCKER_PATH_CSV")
else:
    PATH_CSV = os.getenv("LOCAL_PATH_CSV")
#ajout du DOCKER_PATH_CSV pour que cela fonctionne aussi avec Docker.

if env == "docker":
    MONGO_URI = os.getenv("DOCKER_MONGO_URI")
else:
    MONGO_URI = os.getenv("LOCAL_MONGO_URI")
    
DB_NAME = os.getenv("DB_NAME")
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
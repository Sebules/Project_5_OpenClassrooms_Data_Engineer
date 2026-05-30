import pytest
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# === CONFIG PATH ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fonctions.export_from_mongodb import export_mongodb
from fonctions.connexion_mongodb import connect_mongodb
from fonctions.migration_to_mongodb import migrate_mongodb
from fonctions.cleaning_df import analyse_df

load_dotenv()
env = os.getenv("ENV_TEST", "local")

if env == "docker":
    PATH_CSV = os.getenv("DOCKER_PATH_CSV")
    MONGO_URI = os.getenv("DOCKER_MONGO_URI")
else:
    PATH_CSV = os.getenv("LOCAL_PATH_CSV")
    MONGO_URI = os.getenv("LOCAL_MONGO_URI")
    
COLLECTION_NAME_TEST_EXPORT = os.getenv("COLLECTION_NAME_TEST_EXPORT")
DB_NAME = os.getenv("DB_NAME")

client = connect_mongodb(MONGO_URI)
df = analyse_df(PATH_CSV)
collection, db = migrate_mongodb(df,client,DB_NAME,COLLECTION_NAME_TEST_EXPORT)


def test_export_mongodb():
    #Arrange
    filtre = {'Age':30}
    limite = 10
    
    #Act
    export_mongodb(client, DB_NAME,COLLECTION_NAME_TEST_EXPORT,filtre, limite)

    #Assert
    assert os.path.exists("donnees/export.csv")>0, "Export râté." # >0 pour vérifier que le fichier existe et qu'il n'est pas vide.


def test_delete_collection():
    #suppression de tous les documents de la collection après les tests
    collection_deleted = collection.delete_many({})
    #Assert
    assert collection_deleted.acknowledged == True
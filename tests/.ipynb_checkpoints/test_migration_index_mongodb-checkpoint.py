import pytest
import pandas as pd
import numpy as np
import os
from pathlib import Path
from pymongo import MongoClient
import sys
from dotenv import load_dotenv

# === CONFIG PATH ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  #ajouter le dossier parent du fichier courant au chemin de recherche des modules Python
from fonctions.migration_to_mongodb import migrate_mongodb
from fonctions.connexion_mongodb import connect_mongodb
from fonctions.cleaning_df import analyse_df
from fonctions.create_index_mongodb import create_index_mongodb

load_dotenv()
env = os.getenv("ENV_TEST", "local")

if env == "docker":
    PATH_CSV = os.getenv("DOCKER_PATH_CSV")
    MONGO_URI = os.getenv("DOCKER_MONGO_URI")
else:
    PATH_CSV = os.getenv("LOCAL_PATH_CSV")
    MONGO_URI = os.getenv("LOCAL_MONGO_URI")
    
COLLECTION_NAME_TEST_MIGRATION = os.getenv("COLLECTION_NAME_TEST_MIGRATION")
DB_NAME = os.getenv("DB_NAME")


client = connect_mongodb(MONGO_URI)


def test_migrate_mongodb():
    #Arrange
    df = analyse_df(PATH_CSV)
    #suppression de tous les documents qui seraient présents dans la collection avant les tests
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME_TEST_MIGRATION]
    collection.delete_many({})
    #Act
    collection, db = migrate_mongodb(df,client,DB_NAME,COLLECTION_NAME_TEST_MIGRATION)

    #Assert
    assert collection.count_documents({}) == len(df), "Vérifier la quantité de documents!"
    
def test_create_index_mongodb():
    #Arrange
    client = connect_mongodb(MONGO_URI)
    #Act
    collection = create_index_mongodb(client,DB_NAME,COLLECTION_NAME_TEST_MIGRATION,['Name','Hospital','Medical Condition','Discharge Date','Date of Admission'])

    #Assert
    indexes_names = collection.index_information().keys()

    assert any('Name' in index for index in indexes_names)
    assert any('Hospital' in index for index in indexes_names)
    assert any('Medical Condition' in index for index in indexes_names)
    assert any('Discharge Date' in index for index in indexes_names)
    assert any('Date of Admission' in index for index in indexes_names)    

    
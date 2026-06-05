import pytest
from pathlib import Path
import os
from datetime import datetime
from pymongo import MongoClient
import sys
from dotenv import load_dotenv

# === CONFIG PATH ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  #ajouter le dossier parent du fichier courant au chemin de recherche des modules Python
from fonctions.connexion_mongodb import connect_mongodb
from fonctions.cleaning_df import analyse_df
from fonctions.migration_to_mongodb import migrate_mongodb
from fonctions.crud_mongodb import (create_one_document, create_documents,
    read_one_document, read_documents, update_one_document, update_documents,delete_documents)

load_dotenv(".env") #charge le fichier .env
load_dotenv(".env.secrets") #charge le fichier .env.secrets

## PARAMÈTRES POUR LA MIGRATION
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
  
    
COLLECTION_NAME_TEST_CRUD = os.getenv("COLLECTION_NAME_TEST_CRUD")


client = connect_mongodb(MONGO_URI)
df = analyse_df(PATH_CSV)
collection, db = migrate_mongodb(df,client,DB_NAME,COLLECTION_NAME_TEST_CRUD)

def test_create_one_document():
    #Arrange
    doc= {
             'name': 'daniella smith',
             'age': 86,
             'gender': 'female',
             'blood_type': 'A-',
             'medical_condition': 'obesity',
             'date_of_admission': datetime(2022, 9, 22),
             'doctor': 'tiffany mitchell',
             'hospital': 'cook plc',
             'insurance_provider': 'aetna',
             'billing_amount': 27955.1,
             'room_number': 219,
             'admission_type': 'emergency',
             'discharge_date': datetime(2022, 10, 7),
             'medication': 'aspirin',
             'test_results': 'normal'
        }
    #Act
    doc_inserted,collection,db = create_one_document(client,DB_NAME,COLLECTION_NAME_TEST_CRUD,doc)

    #Assert
    assert doc_inserted.inserted_id is not None, "Document non créé."
    

def test_create_documents():
    # Arrange
    docs = [
    {
     'name': 'daniella marks',
     'age': 18,
     'gender': 'female',
     'blood_type': 'A-',
     'medical_condition': 'obesity',
     'date_of_admission': datetime(2023, 9, 22),
     'doctor': 'tiffany mitchell',
     'hospital': 'cook plc',
     'insurance_provider': 'aetna',
     'billing_amount': 295576.1,
     'room_number': 2151,
     'admission_type': 'emergency',
     'discharge_date': datetime(2023, 10, 17),
     'medication': 'aspirin',
     'test_results': 'normal'
    },
    {
     'name': 'matt smith',
     'age': 76,
     'gender': 'male',
     'blood_type': 'O-',
     'medical_condition': 'normal',
     'date_of_admission': datetime(2021, 9, 22),
     'doctor': 'tiffany mitchell',
     'hospital': 'cook plc',
     'insurance_provider': 'aetna',
     'billing_amount': 28955.1,
     'room_number': 219,
     'admission_type': 'emergency',
     'discharge_date': datetime(2021, 10, 7),
     'medication': 'aspirin',
     'test_results': 'normal'
    },
    {
     'name': 'christina tyher',
     'age': 86,
     'gender': 'female',
     'blood_type': 'B-',
     'medical_condition': 'obesity',
     'date_of_admission': datetime(2023, 9, 22),
     'doctor': 'tiffany mitchell',
     'hospital': 'cook plc',
     'insurance_provider': 'aetna',
     'billing_amount': 29795.1,
     'room_number': 219,
     'admission_type': 'emergency',
     'discharge_date': datetime(2023, 10, 7),
     'medication': 'aspirin',
     'test_results': 'normal'
    }
]
    #Act
    docs_inserted,collection,db,nb_documents = create_documents(client,DB_NAME,COLLECTION_NAME_TEST_CRUD,docs)

    # Assert
    assert docs_inserted.inserted_ids is not None, "Documents non créés."
    assert nb_documents!=0


def test_read_one_document():
    #Arrange
    recherche = {"Name": "Bobby JacksOn"}

    #Act
    doc_read = read_one_document(client,DB_NAME,COLLECTION_NAME_TEST_CRUD,recherche)

    #Assert
    assert doc_read is not None, "Document non lu."
    


def test_read_documents():
    #Arrange
    filtre = {'Age':16}
    champs = {'_id':0,'Name':1,'Admission Type':'Emergency'}

    #Act
    docs_read = read_documents(client,DB_NAME,COLLECTION_NAME_TEST_CRUD,filtre, champs, 10)

    #Assert
    assert docs_read is not None, "Documents non lus."

def test_update_one_document():
    #Arrange
    recherche = {"name":"christina tyher"}
    changement = {"age": 95}
    #Act
    doc_updated = update_one_document(client,DB_NAME,COLLECTION_NAME_TEST_CRUD,recherche,changement)
    #Assert
    assert doc_updated is not None, "Document non mis à jour."
    

def test_update_documents():
    #Arrange
    recherche = {
        'name': {'$in':['christina tyher','daniella marks','matt smith']
                }
    }
    changement = {'doctor':'georges mitchell'}
    #Act
    docs_updated = update_documents(client,DB_NAME,COLLECTION_NAME_TEST_CRUD,recherche,changement)
    #Assert
    assert docs_updated is not None, "Documents non mis à jour."

def test_delete_document_one():
    #Arrange
    recherche = {'name':'daniella smith'}
    #Act
    doc_deleted = delete_documents(client,DB_NAME,COLLECTION_NAME_TEST_CRUD, recherche, one=True)
    #Assert
    assert doc_deleted.acknowledged == True, "Document non supprimé."


def test_delete_documents():
    #Arrange
    recherche = {'name': {'$in': ['christina tyher','daniella marks','matt smith']}}
    #Act
    docs_deleted = delete_documents(client,DB_NAME,COLLECTION_NAME_TEST_CRUD, recherche, one=False)
    #Assert
    assert docs_deleted.acknowledged == True, "Documents non supprimés."

def test_delete_collection():
    #suppression de tous les documents de la collection après les tests
    collection_deleted = collection.delete_many({})
    #Assert
    assert collection_deleted.acknowledged == True
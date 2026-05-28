import pytest
import pandas as pd
import numpy as np
import os
from pathlib import Path
from pymongo import MongoClient
import sys

# === CONFIG PATH ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fonctions.migration_to_mongodb import migrate_mongodb
from fonctions.connexion_mongodb import connect_mongodb
from fonctions.cleaning_df import analyse_df
from fonctions.create_index_mongodb import create_index_mongodb

client = connect_mongodb('mongodb://localhost:27017/')
chemin= Path(os.getcwd())
path = chemin/'donnees/healthcare_dataset.csv'


def test_migrate_mongodb():
    #Arrange
    df = analyse_df(path)
    #suppression de tous les documents qui seraient présents dans la collection avant les tests
    db = client['datasolutech']
    collection = db['healthcare_data_test_migration']
    collection.delete_many({})
    #Act
    collection, db = migrate_mongodb(df,client,'datasolutech','healthcare_data_test_migration')

    #Assert
    assert collection.count_documents({}) == len(df), "Vérifier la quantité de documents!"
    
def test_create_index_mongodb():
    #Arrange
    client = connect_mongodb('mongodb://localhost:27017/')
    #Act
    collection = create_index_mongodb(client,"datasolutech","healthcare_data_test_migration",['Name','Hospital','Medical Condition','Discharge Date','Date of Admission'])

    #Assert
    indexes_names = collection.index_information().keys()

    assert any('Name' in index for index in indexes_names)
    assert any('Hospital' in index for index in indexes_names)
    assert any('Medical Condition' in index for index in indexes_names)
    assert any('Discharge Date' in index for index in indexes_names)
    assert any('Date of Admission' in index for index in indexes_names)    

    
import pytest
import os
from pathlib import Path
from export_from_mongodb import export_mongodb
from connexion_mongodb import connect_mongodb
from migration_to_mongodb import migrate_mongodb
from cleaning_df import analyse_df


client = connect_mongodb('mongodb://localhost:27017/')
chemin= Path(os.getcwd())
path = chemin/'donnees/healthcare_dataset.csv'
df = analyse_df(path)
collection, db = migrate_mongodb(df,client,'datasolutech','healthcare_data_test_export')


def test_export_mongodb():
    #Arrange
    filtre = {'Age':30}
    limite = 10
    
    #Act
    export_mongodb(client, 'datasolutech','healthcare_data_test_export',filtre, limite)

    #Assert
    assert os.path.exists("export.csv")>0, "Export râté." # >0 pour vérifier que le fichier existe et qu'il n'est pas vide.


def test_delete_collection():
    #suppression de tous les documents de la collection après les tests
    collection_deleted = collection.delete_many({})
    #Assert
    assert collection_deleted.acknowledged == True
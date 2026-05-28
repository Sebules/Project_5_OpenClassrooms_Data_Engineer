import pytest
from pymongo import MongoClient
from create_index_mongodb import create_index_mongodb
from connexion_mongodb import connect_mongodb




def test_create_index_mongodb():
    #Arrange
    client = connect_mongodb('mongodb://localhost:27017/')
    #Act
    collection = create_index_mongodb(,client,"datasolutech","healthcare_data_test",['Name','Hospital','Medical Condition','Discharge Date','Date of Admission']

    #Assert
    indexes_names = collection.index_informations().keys()

    assert any('Name' in index for index in indexes_names)
    assert any('Hospital' in index for index in indexes_names)
    assert any('Medical Condition' in index for index in indexes_names)
    assert any('Discharge Date' in index for index in indexes_names)
    assert any('Date of Admission' in index for index in indexes_names)
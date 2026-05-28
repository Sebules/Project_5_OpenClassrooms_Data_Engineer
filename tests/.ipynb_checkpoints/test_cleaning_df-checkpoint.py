import pytest
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
# === CONFIG PATH ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fonctions.cleaning_df import (analyse_df, clean_columns_name, clean_columns_content,
                        convert_type_date, convert_type_integer, convert_type_float)

chemin= Path(os.getcwd())
path = chemin/'donnees/healthcare_dataset_test.csv'


def test_analyse_df():
    #Arrange
    # c'est path
    #Act
    df = analyse_df(path)
    #Assert
    assert df.shape[0]>0, "le dataframe est vide"
    assert list(df.columns[df.isna().all()]) ==[], "Certaines colonnes sont entièrement nulles"
    assert df.duplicated().sum() == 0, "Certaines lignes sont en doublon"

def test_clean_columns_name():
    #Arrange
    df = analyse_df(path)
    
    expected_columns = [col.strip().lower().replace(" ","_") for col in df.columns]

    #Act
    df = clean_columns_name(df)
    #Assert
    assert list(df.columns) == expected_columns

def test_clean_columns_content():
    #Arrange
    df = analyse_df(path)
    liste = ['Name','Doctor']
    
    #Act
    df = clean_columns_content(df,liste)

    #Assert
    assert all(df[col].str.islower().all() for col in liste), "Dans ces colonnes, les valeurs ne sont pas en minuscules"


def test_convert_type_date():
    #Arrange
    df = analyse_df(path)
    liste = ['Date of Admission','Discharge Date']
    
    #Act
    df = convert_type_date(df,liste)

    #Assert
    assert all(df[col].dtype == 'datetime64[ns]' for col in liste)
    
def test_convert_type_integer():
    #Arrange
    df = analyse_df(path)
    liste = ['Age','Room Number']
    
    #Act
    df = convert_type_integer(df,liste)

    #Assert
    assert all(df[col].dtype == 'Int64' for col in liste)

def test_convert_type_float():
    #Arrange
    df = analyse_df(path)
    liste = ['Billing Amount']
    
    #Act
    df = convert_type_float(df,liste)

    #Assert
    assert all(df[col].dtype == 'Float64' for col in liste)

def test_age_negatif():
    #Arrange
    df = analyse_df(path)
    #Act
    nb_age_negatif = len(df[df['Age']<0])
    #Assert
    assert nb_age_negatif == 0, "Vérifier les âges."

def test_billing_negatif():
    #Arrange
    df = analyse_df(path)
    #Act
    nb_billing_negatif = len(df[df['Billing Amount']<0])
    #Assert
    assert nb_billing_negatif == 0, "Vérifier les factures."    

def test_dates_incoherence():
    #Arrange
    df = analyse_df(path)
    #Act
    nb_dates_incoherence = len(df[df['Date of Admission']>df['Discharge Date']])
    #Assert
    assert nb_dates_incoherence == 0, "Vérifier la cohérence des dates." 


def main():
    test_analyse_df()
    test_clean_columns_name()
    test_clean_columns_content()
    test_convert_type_date()
    test_convert_type_integer()
    test_convert_type_float()
    test_age_negatif()
    test_billing_negatif()
    test_dates_incoherence()

if __name__ == "__main__":
    print("Tous les tests cleaning sont OK!")
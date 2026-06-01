import pytest
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# === CONFIG PATH ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  #ajouter le dossier parent du fichier courant au chemin de recherche des modules Python
from fonctions.cleaning_df import (analyse_df, clean_columns_name, clean_columns_content,
                        convert_type_date, convert_type_integer, convert_type_float,
                        age_negatif, billing_negatif, dates_incoherence)

load_dotenv()
env = os.getenv("ENV_TEST", "local")

if env == "docker":
    PATH_CSV = os.getenv("DOCKER_PATH_CSV")
    MONGO_URI = os.getenv("DOCKER_MONGO_URI")
else:
    PATH_CSV = os.getenv("LOCAL_PATH_CSV")
    MONGO_URI = os.getenv("LOCAL_MONGO_URI")



def test_analyse_df():
    #Arrange
    # c'est path
    #Act
    df = analyse_df(PATH_CSV)
    #Assert
    assert df.shape[0]>0, "le dataframe est vide"
    assert list(df.columns[df.isna().all()]) ==[], "Certaines colonnes sont entièrement nulles"
    assert df.duplicated().sum() == 0, "Certaines lignes sont en doublon"

def test_clean_columns_name():
    #Arrange
    df = analyse_df(PATH_CSV)
    
    expected_columns = [col.strip().lower().replace(" ","_") for col in df.columns]

    #Act
    df = clean_columns_name(df)
    #Assert
    assert list(df.columns) == expected_columns

def test_clean_columns_content():
    #Arrange
    df = analyse_df(PATH_CSV)
    liste = ['Name','Doctor']
    
    #Act
    df = clean_columns_content(df,liste)

    #Assert
    assert all(df[col].str.islower().all() for col in liste), "Dans ces colonnes, les valeurs ne sont pas en minuscules"


def test_convert_type_date():
    #Arrange
    df = analyse_df(PATH_CSV)
    liste = ['Date of Admission','Discharge Date']
    
    #Act
    df = convert_type_date(df,liste)

    #Assert
    assert all(pd.api.types.is_datetime64_any_dtype(df[col]) for col in liste)
    # avec df[col].dtype == 'datetime64[ns]' : le test échouait dans Docker car, dans Docker, c'est 'datetime64[us]' ; d'où pd.api.types.is_datetime64_any_dtype(df[col]) pour prendre tous les types possibles. 
def test_convert_type_integer():
    #Arrange
    df = analyse_df(PATH_CSV)
    liste = ['Age','Room Number']
    
    #Act
    df = convert_type_integer(df,liste)

    #Assert
    assert all(df[col].dtype == 'Int64' for col in liste)

def test_convert_type_float():
    #Arrange
    df = analyse_df(PATH_CSV)
    liste = ['Billing Amount']
    
    #Act
    df = convert_type_float(df,liste)

    #Assert
    assert all(df[col].dtype == 'Float64' for col in liste)

def test_age_negatif():
    #Arrange
    df = analyse_df(PATH_CSV)
    #Act
    df,nb_age_negatif, df_age_negatif = age_negatif(df,'Age')
    if not df_age_negatif.empty:
        print(df_age_negatif.head())
        print(df_age_negatif.info())
    #Assert
    assert df[df['Age']<0].empty, "Des lignes d'âge négatif sont encore présentes."

def test_billing_negatif():
    #Arrange
    df = analyse_df(PATH_CSV)
    #Act
    df,nb_billing_negatif,df_billing_negatif = billing_negatif(df, 'Billing Amount')
    if not df_billing_negatif.empty:
        print(df_billing_negatif.head())
        print(df_billing_negatif.info())
    #Assert
    assert df[df['Billing Amount']<0].empty, "Des lignes avec des factures négatives sont encore présentes." 

def test_dates_incoherence():
    #Arrange
    df = analyse_df(PATH_CSV)
    #Act
    df, nb_dates_incoherence, df_dates_incoherence = dates_incoherence(df,'Date of Admission','Discharge Date')
    if not df_dates_incoherence.empty:
        print(df_dates_incoherence.head())
        print(dfdates_incoherence.info())
        
    #Assert
    assert df[df['Date of Admission']>df['Discharge Date']].empty, "Des lignes avec des dates non cohérentes sont encore présentes." 


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
    main()
    print("Tous les tests cleaning sont OK!")
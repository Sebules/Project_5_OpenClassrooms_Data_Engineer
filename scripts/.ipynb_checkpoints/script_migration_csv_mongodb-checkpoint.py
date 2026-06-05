"""
Script d'automatisation de la migration d'un dataset CSV vers MongoDB.

Étapes :
1. Lecture et vérification du fichier CSV
2. Nettoyage et conversion des données
3. Connexion à MongoDB
4. Migration des données et vérification post-migration
5. Création des index
6. Déconnexion
"""
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# === CONFIG PATH ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fonctions.parser_liste_env import parser_liste_env
from fonctions.cleaning_df import (analyse_df, clean_columns_name, clean_columns_content,
                                    convert_type_date, convert_type_float, convert_type_integer,
                                    age_negatif, billing_negatif, dates_incoherence)
from fonctions.connexion_mongodb import connect_mongodb, disconnect_mongodb
from fonctions.migration_to_mongodb import migrate_mongodb
from fonctions.create_index_mongodb import create_index_mongodb

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
  

COLLECTION_NAME = os.getenv("COLLECTION_NAME")
COLLECTION_NAME_AGE = os.getenv("COLLECTION_NAME_AGE")
COLLECTION_NAME_BILL = os.getenv("COLLECTION_NAME_BILL")
COLLECTION_NAME_DATES = os.getenv("COLLECTION_NAME_DATES")

## Colonnes pour le nettoyage   
COLONNES_TEXTE = parser_liste_env("COLONNES_TEXTE") # sert à créer une liste car .getenv renvoie un string
COLONNES_DATE = parser_liste_env("COLONNES_DATE")
COLONNES_FLOAT = parser_liste_env("COLONNES_FLOAT")
COLONNES_INT = parser_liste_env("COLONNES_INT")

# Colonnes pour la cohérence des données
COLONNE_AGE = os.getenv("COLONNE_AGE")
COLONNE_BILL = os.getenv("COLONNE_BILL")
COLONNE_DATE_1 = os.getenv("COLONNE_DATE_1")
COLONNE_DATE_2 = os.getenv("COLONNE_DATE_2")

## Index à créer dans MongoDB
INDEXES = parser_liste_env("INDEXES")


def read_and_check_csv(path_csv:str):
    """Fonction dédiée à la lecture et la vérification du fichier CSV"""
    print(f'Lecture du fichier au chemin: {path_csv}')
    if not os.path.exists(path_csv):
        raise FileNotFoundError(f"Le fichier au chemin {path_csv} est introuvable.") 
        #raise sert à lever une erreur si pas de fichier. https://docs.python.org/3/library/exceptions.html,
        #https://docs.python.org/3/reference/simple_stmts.html#raise, le script s'arrêtera.
    
    df = analyse_df(path_csv) #cette fonction supprime les colonnes entièrement vides et les lignes en doublon

    if df.empty:
        raise ValueError("Le dataset est vide.")

    print("Fichier lu et vérifié")
    
    return df


def clean_and_convert_df(df):
    """Fonction dédiée au nettoyage et convertir des données"""
    df = clean_columns_name(df)
    df = clean_columns_content(df,COLONNES_TEXTE)
    df = convert_type_date(df,COLONNES_DATE)
    df = convert_type_float(df,COLONNES_FLOAT)
    df = convert_type_integer(df, COLONNES_INT)
    df,_,df_age_negatif = age_negatif(df, COLONNE_AGE)
    df,_,df_billing_negatif = billing_negatif(df, COLONNE_BILL)
    df,_,df_dates_incoherence = dates_incoherence(df,COLONNE_DATE_1,COLONNE_DATE_2)
        
    print("Nettoyage et conversion terminés!")
    print("\nAperçu dataframe nettoyé.")
    print(df.head())
    print(df.info())
    if not df_age_negatif.empty:
        print("\nAperçu des lignes avec un âge négatif.")
        print(df_age_negatif.head())
        print(df_age_negatif.info())
    if not df_billing_negatif.empty:
        print("_\nAperçu des lignes avec une facture négative.")
        print(df_billing_negatif.head())
        print(df_billing_negatif.info())
    if not df_dates_incoherence.empty:
        print("\nAperçu des lignes présentant des dates d'admission et de sortie incohérentes.")
        print(df_dates_incoherence.head())
        print(df_dates_incoherence.info())
    return df, df_age_negatif, df_billing_negatif, df_dates_incoherence


def demander_confirmation(message):
    """Fonction de demande à l'utilisateur une confirmation y/n"""
    reponse = input(f"{message} (y/n) : ").strip().lower()
    return reponse == "y"

## Fonction  Connexion à MongoDB

def main():

    # 1. Lecture et vérification du fichier CSV
    df = read_and_check_csv(PATH_CSV)

    ## Demande de confirmation
    message = """
    Voulez-vous lancer le nettoyage et la conversion des données?
    """
    if not env=="docker":
        if not demander_confirmation(message):
            print("Migration annulée!")
            return
        print("=====================================================================================")
    # 2. Nettoyage et conversion des données
    df,df_age_negatif,df_billing_negatif, df_dates_incoherence = clean_and_convert_df(df)

    ## Demande de confirmation
    message = """
    Regarder les informations du DataFrame et les premières lignes.
    Regarder le retour obtenu sur les âges, les factures et les dates.
    Voulez-vous lancer la migration?
    """
    if not env=="docker":
        if not demander_confirmation(message):
            print("Migration annulée!")
            return
        print("=====================================================================================")
    # 3. Connexion à MongoDB
    client = connect_mongodb(MONGO_URI)
    print("=====================================================================================")
    
    # 4. Migration des données et vérification post-migration
    collection,db = migrate_mongodb(df,client, DB_NAME, COLLECTION_NAME)
    collection_age,db = migrate_mongodb(df_age_negatif,client, DB_NAME, COLLECTION_NAME_AGE)
    collection_billing,db = migrate_mongodb(df_billing_negatif,client, DB_NAME, COLLECTION_NAME_BILL)
    collection_dates,db = migrate_mongodb(df_dates_incoherence,client, DB_NAME, COLLECTION_NAME_DATES)
    print("=====================================================================================")
    # 5. Création des index
    collection = create_index_mongodb(client, DB_NAME, COLLECTION_NAME,INDEXES)
    collection_age = create_index_mongodb(client, DB_NAME, COLLECTION_NAME_AGE,INDEXES)
    collection_billing = create_index_mongodb(client, DB_NAME, COLLECTION_NAME_BILL,INDEXES)
    collection_dates = create_index_mongodb(client, DB_NAME, COLLECTION_NAME_DATES,INDEXES)
    # 6. Déconnexion
    disconnect_mongodb(MONGO_URI)
    print("Migration terminée.")

if __name__ == "__main__":
    main()
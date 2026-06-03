import pandas as pd
from pymongo import MongoClient
from fonctions.crud_mongodb import create_documents
import os
import sys
from dotenv import load_dotenv

# === CONFIG PATH ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  #ajouter le dossier parent du fichier courant au chemin de recherche des modules Python

def migrate_mongodb (df:pd.DataFrame,client, name_database:str,name_collection:str):
    if not df.empty:    
        documents = df.to_dict(orient="records") 
        # orient = "records" permet de transformer chaque ligne du dataframe en un dictionnaire distinct. Pratique pour MongoDB    

        _,collection,db, nb_documents =create_documents(client,name_database,name_collection,documents)
        #collection.insert_many(documents) 
        # sert à insérer les documents dans la collection.
    
        csv_count = len(df)
                
        print(f'il y a : {nb_documents} documents dans la collection {name_collection} de la database {name_database}.')
        if csv_count == nb_documents:
            print('le nombre de lignes du dataframe correspond au nombre de documents dans la collection.\n')
        else:
            print('le nombre de lignes du dataframe ne correspond pas au nombre de documents dans la collection!!!\n')
    else:
        print(f"Le dataset est vide, pas de migration dans la collection {name_collection}.\n")
        db = client[name_database]
        collection = db[name_collection]
        

    return collection, db
import pandas as pd
from pymongo import MongoClient

def migrate_mongodb (df:pd.DataFrame,client, name_database:str,name_collection:str):
    try:
        db=client[name_database] #Création de la database dans le client MongoDB si elle n'existe pas déjà
        collection = db[name_collection] #Création de la collection dans la database si elle n'existe pas déjà
    except Exception as e:
        print(e)
        
    documents = df.to_dict(orient="records") 
    # orient = "records" permet de transformer chaque ligne du dataframe en un dictionnaire distinct. Pratique pour MongoDB    

    collection.insert_many(documents) 
    # sert à insérer les documents dans la collection.

    csv_count = len(df)
    mongo_count = collection.count_documents({})
    
    print(f'il y a : {mongo_count} documents dans la collection {name_collection} de la database {name_database}')
    if csv_count == mongo_count:
        print('le nombre de lignes du dataframe correspond au nombre de documents dans la collection')
    else:
        print('le nombre de lignes du dataframe ne correspond pas au nombre de documents dans la collection!!!')

    return collection, db
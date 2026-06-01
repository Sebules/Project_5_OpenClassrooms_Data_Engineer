import pandas as pd
from pymongo import MongoClient


def export_mongodb(client, name_database:str,name_collection:str,filtre:dict, limite:int|None):
    db=client[name_database]
    collection = db[name_collection]
    
    if limite is not None:
        docs_read = collection.find(filtre,{"_id": 0},limit= limite)
        data = list(docs_read)  
    else:
        docs_read = collection.find(filtre,{"_id": 0})
        data = list(docs_read)
    # Conversion en DataFrame
    df = pd.DataFrame(data)

    # Export CSV
    df.to_csv(f"/donnees/export_{name_collection}.csv", index=False, encoding="utf-8")

    print(f"L'export de la collection {name_collection} de la database {name_database} est réussi!")

    
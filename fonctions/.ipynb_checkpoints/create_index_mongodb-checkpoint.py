from pymongo import MongoClient

def create_index_mongodb (client, name_database:str,name_collection:str, liste_index:list):
    
    db=client[name_database]
    collection = db[name_collection]

    try:
        for index in liste_index:
            collection.create_index(index)
    except Exception as e:
        print(e)

    return collection

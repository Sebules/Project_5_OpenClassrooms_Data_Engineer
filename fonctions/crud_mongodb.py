from pymongo import MongoClient

## CREATE
def create_one_document(client,name_database:str,name_collection:str,doc:dict):
    db=client[name_database]
    collection = db[name_collection]
    
    doc_inserted = collection.insert_one(doc)
    print(f"Le document avec l'id {doc_inserted.inserted_id} a été inséré dans la collection {name_collection}.")
    return doc_inserted

def create_documents(client,name_database:str,name_collection:str,docs:list):
    db=client[name_database]
    collection = db[name_collection]
    
    docs_inserted = collection.insert_many(docs)
    print(f"Les documents avec les ids {docs_inserted.inserted_ids} ont été insérés dans la collection {name_collection}.")
    return docs_inserted


## READ

def read_one_document(client,name_database:str,name_collection:str,recherche:dict):
    db=client[name_database]
    collection = db[name_collection]

    doc_read = collection.find_one(recherche)
    print(f'Le document recherché a pour id {doc_read["_id"]}.')
    return doc_read

def read_documents(client,name_database:str,name_collection:str,filtre:dict, champs:dict, limite:int|None):
    db=client[name_database]
    collection = db[name_collection]

    if limite is not None:
        for doc in collection.find(filtre,champs,limit= limite):
            print(doc)
            
        docs_read = [doc for doc in collection.find(filtre,champs,limit= limite)]
    else:
        for doc in collection.find(filtre,champs):
            print(doc)
            
        docs_read = [doc for doc in collection.find(filtre,champs)]
        
    docs_id =[doc.get("_id") for doc in docs_read]
    
    print(f'Les documents recherchés ont pour ids {docs_id}.')
    return docs_read


## UPDATE

def update_one_document(client,name_database:str,name_collection:str,recherche:dict,changement:dict):
    db=client[name_database]
    collection = db[name_collection]

    doc_updated = collection.update_one(recherche,{"$set":changement})
    print(f'Document correspondant : {doc_updated.matched_count}, modifié : {doc_updated.modified_count}.')
    return doc_updated

def update_documents(client,name_database:str,name_collection:str,recherche:dict,changement:dict):
    db=client[name_database]
    collection = db[name_collection]

    docs_updated = collection.update_many(recherche,{"$set":changement})
        
    print(f'Documents correspondants : {docs_updated.matched_count}, modifiés : {docs_updated.modified_count}.')
    return docs_updated


## DELETE

def delete_documents(client,name_database:str,name_collection:str, recherche:dict, one=True):
    db=client[name_database]
    collection = db[name_collection]

    if one==True:
        doc_read = collection.find_one(recherche)
        _id = doc_read["_id"]
        doc_deleted = collection.delete_one(recherche)
        print('Le document supprimé avait pour id:',_id)
        return doc_deleted
    else:
        docs_read = []
        for doc in collection.find(recherche):
            print(doc)
        
        docs_read = [doc for doc in collection.find(recherche)]
            
        docs_id =[doc["_id"] for doc in docs_read]
        
        docs_deleted = collection.delete_many(recherche)
        print("Documents supprimés :", docs_deleted.deleted_count)
        print('Les documents supprimés avaient pour id:',docs_id)
        return docs_deleted
        
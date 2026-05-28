from pymongo import MongoClient

def connect_mongodb (uri):
    
    # Connexion à MongoDB
    client = MongoClient(uri)

    try:
        # Tester la connection
        client.admin.command('ping')
        print("Connecté à MongoDB!")
    except Exception as e:
        print(e)
    return client

def disconnect_mongodb(uri):
    client = MongoClient(uri)
    client.close()
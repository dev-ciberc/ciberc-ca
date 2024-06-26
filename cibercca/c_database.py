from pymongo import MongoClient
import certifi
import yaml

with open("./inventory/dbconnect.yaml", "r") as file:
    config = yaml.safe_load(file)
    
uri = config['database']['mongodbUri']
ca = certifi.where()

def db_conecction():
    try:
        client = MongoClient(uri, tlsCAFile=ca)
        db = client["db_cibercca"] 
        print("You successfully connected to MongoDB!")
    except ConnectionError:
        print("Connection error with Database")
    return db

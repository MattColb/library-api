import pymongo
import datetime
import certifi
import json
from bson import ObjectId
import os
from dotenv import load_dotenv

def mongo_connect():
    mongo = os.getenv("MONGO")# Mongo URL
    client = pymongo.MongoClient(mongo, tlsCAFile=certifi.where())
    db = client["bais3400"]  # Mongo collection
    db_connection = db["recommendations"]  # Mongo document

    return db_connection, client


def get_all_recommendations():
    conn, client = mongo_connect()

    all_recommendations = conn.find()  # get all recommendations

    print("--------------------")

    for doc in all_recommendations:
        print(doc)

    print("--------------------")

    client.close()

    return all_recommendations


def get_recommendations_by_name(name):
    conn, client = mongo_connect()

    results = conn.find({"name":name})

    #Handling the return in here so that you don't have to deal with it in the main.
    ret = ""
    for r in results:
        ret = ret + f"ObjectID: {r['_id']}\n{r['name']}'s favorite book was {r['title']} as of {r['date_added']}\nHere is other information:{r['other']}\n" + "\n"

    client.close()

    return ret

def get_recommendation_by_id(id):
    
    conn, client = mongo_connect()

    
    result = conn.find_one({"_id":ObjectId(id)})

    client.close()
    
    return result


def insert_recommendation(name, title, other):
    new_recommendation = {
        "name": name,
        "title": title,
        "date_added": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "other":other
    }

    conn, client = mongo_connect()

    result = conn.insert_one(new_recommendation)
    id = result.inserted_id
    client.close()

    return id

def main():
    #get_all_recommendations()

    get_recommendation_by_id("65a5778354a7d432fc515c07")

    #result = insert_recommendation("Matt Colbert", "Testing2", {"Testing1":"FunctionalityA"})
    #print(result)


if __name__ == "__main__":
    main()

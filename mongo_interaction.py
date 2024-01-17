import pymongo
import datetime
import certifi
import json
from bson import ObjectId
from bson.json_util import dumps, loads
import os
from dotenv import load_dotenv

"""
TODO:
Make sure that the delete returns are something that is handled well.

"""

def mongo_connect():
    mongo = os.getenv("MONGO")# Mongo URL
    client = pymongo.MongoClient(mongo, tlsCAFile=certifi.where())
    db = client["bais3400"]  # Mongo collection
    db_connection = db["recommendations"]  # Mongo document

    return db_connection, client


def get_all_recommendations():
    conn, client = mongo_connect()

    all_recommendations = conn.find()  # get all recommendations
    ret = []

    for r in all_recommendations:
        ret.append(r)

    client.close()

    return dumps(ret)


def get_recommendations_by_name(name):
    conn, client = mongo_connect()

    results = conn.find({"name":name})

    #Handling the return in here so that you don't have to deal with it in the main.
    ret = []
    for r in results:
        ret.append(r)

    client.close()

    return dumps(ret)

def get_recommendation_by_id(id):
    
    conn, client = mongo_connect()

    
    result = conn.find_one({"_id":ObjectId(id)})

    client.close()
    
    return dumps(result)


def put_by_id(id, info):
    conn, client = mongo_connect()

    filter = {"_id":ObjectId(id)}

    info["date_added"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    updates = {"$set":info}

    if "_id" in info.keys():
        return False

    result = conn.update_one(filter, updates)

    client.close()
    
    return f"Successfully updated ID: {id}"


def delete_by_id(id):
    conn, client = mongo_connect()

    result = conn.delete_one({"_id":ObjectId(id)})

    client.close()

    if result.deleted_count > 0:
        return f"Successfully deleted the ID: {id}"
    else:
        return "The ID was not successfully deleted."
    

def name_title_check(info):
    if info.get("name", False) and info.get("title", False):
        return True
    else:
        return False

def insert_recommendation(info):
    #Error checking: Making sure there is a 'name' and 'title'. Also that '_id' and 'date_added' are not touched. Won't continue if errors
    if not name_title_check(info):
        return False
    if info.get("_id", False):
        return False
    if info.get("date_added", False):
        return False

    #Adds date to their information
    info["date_added"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn, client = mongo_connect()

    #Pulls out id and returns it to user
    result = conn.insert_one(info)
    id = result.inserted_id
    client.close()

    return id

def main():
    print(get_all_recommendations())
    #print(type(get_all_recommendations()))

    #print(get_recommendation_by_id("65a5778354a7d432fc515c07"))

    #print(get_recommendations_by_name("Matt Colbert"))

    #result = insert_recommendation("Matt Colbert", "Testing2", {"Testing1":"FunctionalityA"})
    #print(result)


if __name__ == "__main__":
    main()

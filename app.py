from flask import Flask, request, jsonify
import mongo_interaction

app = Flask("__name__")


@app.route("/", methods=['GET'])
def home():
    if request.method == "GET":
        try:
            return "BAIS:3400 API for student learning materials recommendations"
        except:
            return "Error", 400
    else:
        return "Method is not available", 405


#Adjust the post requests so that if it is invalid, it wont
@app.route("/material", methods=["GET", "POST"])
def material():
    if request.method == "POST":
        try:
            info = request.get_json()
            id = mongo_interaction.insert_recommendation(info)
            if id == False:
                return "Please ensure that you have a 'title' and 'name' in your json to insert into the database.\nAlso, make sure that you are not changing 'date_added' and '_id'"
            return f"Your book is now in the database with ID: {id}.\nYou can search for it with a GET request by either your name or id."
        except:
            return f"Error", 400
    elif request.method == "GET":
        ret = mongo_interaction.get_all_recommendations()
        return ret
    else:
        return "Method is not available", 405


@app.route("/material/<id>", methods = ["GET", "PUT", "DELETE"])
def id_material(id):
    if request.method == "GET":
        try:
            ret = mongo_interaction.get_recommendation_by_id(id)
            return ret
        except:
            "Error", 400
    
    #Updates it and returns that the id has been updated
    elif request.method == "PUT":
        info = request.get_json()
        result = mongo_interaction.put_by_id(id, info)
        if not result:
            return "Please do not change the '_id'."
        return result
    
    elif request.method == "DELETE":
        try:
            ret = mongo_interaction.delete_by_id(id)
            return ret
        except:
            return "Error", 400
    else:
        return "Method is not available", 405


@app.route("/material/search", methods=["GET"])
def test():
    if request.method == "GET":
        try:
            #Checks if id is in args list
            if request.args.get("id", False):
                id = request.args.get("id", "")
                ret = mongo_interaction.get_recommendation_by_id(id)
                return ret
            #Checks if name is in args list
            elif request.args.get("name", False):
                name = request.args.get("name", "")
                results = mongo_interaction.get_recommendations_by_name(name)
                return results
            #Makes them search by either name or id if it is not in the list.
            else:
                return "Please search by either the name or id."
        except:
            return f"Error", 400
    else:
        return "Method not currently available", 405


if __name__ == "__main__":
    app.run()


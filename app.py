from flask import Flask, request, jsonify
import mongo_interaction

app = Flask("__name__")

# Used for extracting info from the call
def extract_info(info):
    name = info['name']
    title = info['title']
    other = {k:v for k,v in info.items() if k not in ['name', 'title']}
    return name, title, other

@app.route("/", methods=['POST', "GET"])
def test():
    if request.method == "POST":
        try:
            info = request.get_json()
            name, title, other = extract_info(info)
            id = mongo_interaction.insert_recommendation(name, title, other)
            return f"Your book is now in the database with ID: {id}. You can search for it with a GET request by either your name or id."
        except:
            return f"Error", 400
        
    elif request.method == "GET":
        try:
            info = request.get_json()
            if info.get("id", False):
                id = info['id']
                result = mongo_interaction.get_recommendation_by_id(id)
                ret = f"ObjectID: {id}\n{result['name']}'s favorite book was {result['title']} as of {result['date_added']}\nHere is other information:{result['other']}"
                return ret
            elif info.get("name", False):
                name = info["name"]
                results = mongo_interaction.get_recommendations_by_name(name)
                return results
            else:
                return "Please search by either the name or id."
        except:
            return f"Error", 400
        
    else:
        return "Method not currently available", 405

if __name__ == "__main__":
    app.run()


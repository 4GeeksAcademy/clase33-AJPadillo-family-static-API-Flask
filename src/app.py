"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Predefined members
John = {
    "id": 1,
    "first_name": "John",
    "last_name": jackson_family.last_name,
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}

Jane = {
    "id": 2,
    "first_name": "Jane",
    "last_name": jackson_family.last_name,
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

Jimmy = {
    "id": 3,
    "first_name": "Jimmy",
    "last_name": jackson_family.last_name,
    "age": 5,
    "lucky_numbers": [1]
}

jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return jsonify({"endpoints": [str(rule) for rule in app.url_map.iter_rules()]}), 200

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"msg": "Member not found"}), 404

@app.route('/member', methods=['POST'])
def add_member():
    request_body = request.get_json()
    if "id" not in request_body:
        request_body["id"] = jackson_family._generateId()  # Generate ID if not provided
    new_member = {
        "id": request_body["id"],
        "first_name": request_body["first_name"],
        "last_name": jackson_family.last_name,
        "age": request_body["age"],
        "lucky_numbers": request_body["lucky_numbers"]
    }
    jackson_family.add_member(new_member)
    return jsonify(new_member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_one_member(id):
    result = jackson_family.delete_member(id)
    if result:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"msg": "Member not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

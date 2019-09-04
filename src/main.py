"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
from models import Contact

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/contact', methods=['GET', 'POST'])
def get_contact():
    if request.method == 'POST':
        body = request.get_json()
        user1 = Contact(
            full_name=body['full_name'],
            email=body['email'],
            address=body['address'],
            phone=body['phone'],
            agenda_slug=body['agenda_slug'])

        db.session.add(user1)
        db.session.commit()
        return jsonify(user1.serialize()), 200
    if request.method == 'GET':
        people_query = Contact.query.all()
        all_people = list(map(lambda x: x.serialize(), people_query))
        people_array = []

        for one_people in all_people:
            people_array.append(one_people)
        return jsonify(people_array), 200

@app.route('/contact/<contact_id>', methods=['GET', 'PUT'])
def get_specific_contact(contact_id):
    if request.method == 'PUT':
        user1 = Contact.query.get(contact_id)

        if user1 is None:
            raise APIException('User not found', status_code=404)

        body = request.get_json()

        if "full_name" in body:
            user1.full_name = body["full_name"]
        if "email" in body:
            user1.email = body["email"]
        if "phone" in body:
            user1.phone = body["phone"]
        if "address" in body:
            user1.address = body["address"]
        if "agenda_slug" in body:
            user1.agenda_slug = body["agenda_slug"]

        db.session.add(user1)
        db.session.commit()
        return jsonify(user1.serialize()), 200

    if request.method == 'GET':
        user1 = Contact.query.get(contact_id)
        print("USER: " + user1.full_name)
        return jsonify(user1), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)

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
        user1 = Contact(
            first_name="Jorge",
            email="jorgesolo_my_super@email.com",
            address="4445 W Main Ave",
            last_name="Sairf",
            phone="843-333-5678")

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
    user1 = Contact.query.get(contact_id)

    if user1 is None:
        raise APIException('User not found', status_code=404)

    body = request.get_json()

    if "first_name" in body:
        user1.first_name = body["first_name"]
    if "last_name" in body:
        user1.last_name = body["last_name"]



if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)

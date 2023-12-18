from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Contact, contact_schema, contacts_schema

api = Blueprint('api',__name__, url_prefix='/api')


#Creating
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):

    print(request.json)
    name = request.json['name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    car_make=request.json['car_make']
    car_model=request.json['car_model']
    car_year=request.json['car_year']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')




    contact = Contact(name, email, phone_number, address, car_make, car_model, car_year, user_token = user_token )
    print(contact)
    db.session.add(contact)
    db.session.commit()

    response = contact_schema.dump(contact)
    return jsonify(response)
#Retrieving all 
@api.route('/cars/', methods=['GET'])
@token_required
def get_all_cars(current_user_token):
    a_user=current_user_token.token
    contacts=Contact.query.filter_by(user_token=a_user).all()
    response=contacts_schema.dump(contacts)
    return jsonify(response)


#Retrieving single
@api.route('cars/<id>',methods=['GET'])
@token_required
def get_single_car(current_user_token,id):
    contact=Contact.query.get(id)
    response=contact_schema.dump(contact)
    return jsonify(response)

#Updating
@api.route('/cars/<id>', methods=['POST','PUT'])
@token_required
def update_car(current_user_token, id):
    contact=Contact.query.get(id)
    contact.name = request.json['name']
    contact.email = request.json['email']
    contact.phone_number = request.json['phone_number']
    contact.address = request.json['address']
    contact.car_make = request.json['car_make']
    contact.car_model  =request.json['car_model']
    contact.car_year = request.json['car_year']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

#Deleting car
@api.route('/cars/<id>', methods=['DELETE'])
@token_required
def delete_car(current_user_token,id):
    contact= Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response= contact_schema.dump(contact)
    return jsonify(response)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import logging

# Configura il logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Client(db.Model):
    __tablename__ = 'clients'
    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the CRM System'})

@app.route('/clients', methods=['POST'])
def add_client():
    data = request.get_json()
    app.logger.debug(f"Received data: {data}")  # Log per debug
    try:
        new_client = Client(name=data['name'], email=data['email'], phone=data.get('phone'))
        db.session.add(new_client)
        db.session.commit()
        app.logger.debug(f"Client added: {new_client}")
        return jsonify({'message': 'Client added successfully'}), 201
    except Exception as e:
        app.logger.error(f"Error adding client: {e}")
        return jsonify({'message': 'Failed to add client'}), 500

@app.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    clients_list = [{'client_id': client.client_id, 'name': client.name, 'email': client.email, 'phone': client.phone, 'created_at': client.created_at} for client in clients]
    return jsonify({'clients': clients_list}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

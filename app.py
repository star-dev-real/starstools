from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import random
import string

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

CONTACTS_FILE = 'contacts.json'
if not os.path.exists(CONTACTS_FILE):
    with open(CONTACTS_FILE, 'w') as f:
        json.dump([], f)

def get_contacts():
    try:
        with open(CONTACTS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(contacts, f, indent=2)

@app.route('/api/v1/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        required_fields = ['name', 'email', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        contact_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        contacts = get_contacts()
        contacts.append({
            "id": contact_id,
            "name": data['name'],
            "email": data['email'],
            "message": data['message']
        })
        save_contacts(contacts)

        return jsonify({
            "message": "Contact saved successfully",
            "id": contact_id
        }), 200

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Contact API"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8088)
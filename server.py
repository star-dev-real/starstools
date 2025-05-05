from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Simple in-memory storage for messages (in a real app, use a database)
messages = []

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        if not all([name, email, message]):
            return jsonify({"status": "error", "message": "All fields are required"}), 400
        
        # Store the message (in memory - will be lost when server restarts)
        messages.append({
            "name": name,
            "email": email,
            "message": message
        })
        
        print(f"New message received from {name} ({email}): {message}")
        
        return jsonify({
            "status": "success",
            "message": f"Thank you for your message {name}! We will be with you shortly."
        })
        
    except Exception as e:
        print(f"Error processing contact form: {str(e)}")
        return jsonify({"status": "error", "message": "An error occurred"}), 500

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify({"messages": messages})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
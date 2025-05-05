from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows your Vercel frontend to access the API

messages = []

@app.route('/api/submit_contact', methods=['POST'])
def submit_contact():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        if not all([name, email, message]):
            return jsonify({"status": "error", "message": "All fields are required"}), 400
        
        messages.append({"name": name, "email": email, "message": message})
        print(f"New message from {name} ({email})")
        
        return jsonify({
            "status": "success",
            "message": f"Thank you, {name}! We'll contact you soon."
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

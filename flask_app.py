from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  

messages = []

@app.route('/api/submit_contact', methods=['POST'])
def submit_contact():
    """Handle contact form submissions from your Vercel frontend"""
    try:
        data = request.json

        if not all(k in data for k in ['name', 'email', 'message']):
            return jsonify({
                "status": "error",
                "message": "All fields (name, email, message) are required"
            }), 400

        messages.append({
            "name": data['name'],
            "email": data['email'],
            "message": data['message']
        })

        print(f"New contact submission from {data['name']} ({data['email']})")

        return jsonify({
            "status": "success",
            "message": f"Thank you {data['name']}! We'll contact you soon."
        })

    except Exception as e:
        print(f"Error processing contact form: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "An internal server error occurred"
        }), 500

@app.route('/')
def health_check():
    """Basic route to verify server is running"""
    return jsonify({
        "status": "running",
        "service": "Soul's Tools Backend",
        "domain": "redskink.onpella.app"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="8080")  

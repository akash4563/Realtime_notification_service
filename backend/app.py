from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase-key.json")  # Replace with your actual file name
firebase_admin.initialize_app(cred)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Real-Time Notification Service'}), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({'error': 'Token is required'}), 400

    # Save token to database (mocked here)
    print(f"Registered token: {token}")

    return jsonify({'message': 'Token registered successfully'}), 200

@app.route('/send', methods=['POST'])
def send_notification():
    data = request.get_json()
    token = data.get('token')
    title = data.get('title')
    body = data.get('body')

    if not all([token, title, body]):
        return jsonify({'error': 'Token, title, and body are required'}), 400

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    try:
        response = messaging.send(message)
        return jsonify({'message': 'Notification sent', 'response': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Listen on all interfaces so mobile devices can access it
    app.run(host='0.0.0.0', port=5000, debug=True)

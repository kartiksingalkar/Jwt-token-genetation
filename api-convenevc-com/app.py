from flask import Flask, request, jsonify
import os
# from dotenv import load_dotenv
# from flask_cors import CORS
import requests

app = Flask(__name__)

# CORS(app)
# load_dotenv()

# Constants
CONSTANT_ROOM_NAME = "ApiTestRoom"
token = None  # Initialize JWT token as None

# API route to generate member and moderator URLs
@app.route('/generate_urls', methods=['POST'])
def generate_urls():
    data = request.json
    room_name = data.get("RoomName")

    # Generate member URL
    member_url = f"https://next.convenevc.com/{room_name}"

    global token
    if token is None:
        # Get JWT token from external service
        jwt_service_url = "https://jwt.convenevc.com/generate-jwt"
        response = requests.get(jwt_service_url)
        token_data = response.json()
        token = token_data.get("token")

    # Generate moderator URL with obtained JWT token
    moderator_url = f"https://next.convenevc.com/{room_name}?jwt={token}"

    return jsonify({"member_url": member_url, "moderator_url": moderator_url})

# API route to get JWT token from external service
@app.route('/generate-jwt', methods=['GET'])
def get_token():
    global token
    if token is None:
        # Get JWT token from external service
        jwt_service_url = "https://jwt.convenevc.com/generate-jwt"
        response = requests.get(jwt_service_url)
        token_data = response.json()
        token = token_data.get("token")

    return jsonify({"token": token})

# API route to get moderator URL with constant room name and JWT token
@app.route('/get_moderator_url', methods=['GET'])
def get_moderator_url():
    global token
    if token is None:
        # Get JWT token from external service
        jwt_service_url = "https://jwt.convenevc.com/generate-jwt"
        response = requests.get(jwt_service_url)
        token_data = response.json()
        token = token_data.get("token")

    return jsonify({"moderator_url": f"https://next.convenevc.com/{CONSTANT_ROOM_NAME}?jwt={token}"})

if __name__ == '__main__':
    app.run(host="localhost", port=int("5000"), debug=True)


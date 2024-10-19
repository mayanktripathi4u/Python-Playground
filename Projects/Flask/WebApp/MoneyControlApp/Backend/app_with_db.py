from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def index():
    response = {
        "status": "success",
        "message": "Message: Welcome to Home Page",
        "title": "🏠 Home Page",
        "payload": {},
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug = True, port = 5002)
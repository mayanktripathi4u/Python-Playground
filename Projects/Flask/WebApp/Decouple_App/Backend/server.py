from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/channels')
def channel():
    print("Called from Frontend.")
    data = {"channel" : ["channel-1", "channel-2", "channel-3"]}
    response = jsonify(data)
    print(response)
    return response

if __name__ == "__main__":
    app.run(debug = True)
from flask import Flask, request, jsonify
from flask_cors import CORS
from semantic_intent_model import predict_intent_semantic

app = Flask(__name__)

# FULL CORS FIX
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response


@app.route('/predict_intent', methods=['POST'])
def predict_intent_api():
    data = request.json
    message = data.get('message', '')
    intent = predict_intent_semantic(message)

    print("MESSAGE:", message)
    print("PREDICTED:", intent)

    return jsonify({'intent': intent})


if __name__ == '__main__':
    app.run(debug=True)

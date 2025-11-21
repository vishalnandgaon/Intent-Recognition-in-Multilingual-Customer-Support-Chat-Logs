
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
sys.path.append('../nlp')
from intent_model import predict_intent

app = Flask(__name__)
CORS(app)
@app.route('/predict_intent', methods=['POST'])
def predict_intent_api():
    data = request.json
    message = data.get('message', '')
    intent = predict_intent(message)
    return jsonify({'intent': intent})

if __name__ == '__main__':
    app.run(debug=True)

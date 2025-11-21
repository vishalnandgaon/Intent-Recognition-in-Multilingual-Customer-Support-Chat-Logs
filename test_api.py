import requests

url = "http://127.0.0.1:5000/predict_intent"
data = {"message": "Hello, I need help with my order."}

response = requests.post(url, json=data)
print("Response:", response.json())
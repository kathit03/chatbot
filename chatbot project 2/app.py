from flask import Flask, request, jsonify
import json
import random

app = Flask(__name__)

def load_responses(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data["intents"]

def get_random_response(intent):
    return random.choice(intent["responses"])

def get_response(input_text, intents):
    for intent in intents:
        for pattern in intent["patterns"]:
            if input_text.lower() in pattern.lower():
                return get_random_response(intent)
    return "I'm sorry, I don't understand that."

json_file_path = "intents.json"
intents = load_responses(json_file_path)

@app.route('/', methods=['GET'])
def chatbot():
    user_input = request.json.get('input')
    response = get_response(user_input, intents)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)

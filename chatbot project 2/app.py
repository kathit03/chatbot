from flask import Flask, request, jsonify
import json
import random
import openai
from flask import render_template
from flask_wtf.csrf import CSRFProtect


# Set your OpenAI API key here
openai.api_key = "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"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your actual secret key
csrf = CSRFProtect(app)
exit_phrase = ["bye", "see you", "good night", "good bye", "cya", "talk to you later"]
exit_response = ["Bye!", "See you soon!", "Leaving so soon", "Thanks for visiting us!"]

def load_responses():
    with open("intents.json", "r") as json_file:
        data = json.load(json_file)
    return data["intents"]

def get_random_response(intent):
    return random.choice(intent["responses"])

def get_response_from_json(input_text, intents):
    for intent in intents:
        for pattern in intent["patterns"]:
            if input_text.lower() in pattern.lower():
                return get_random_response(intent)
    return None

def get_response_from_chatgpt(input_text):
    prompt = f"User: {input_text}\nChatGPT: "
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use the GPT-3.5 engine
        prompt=prompt,
        temperature=0.6,  # Controls randomness of responses
        max_tokens=4000   # Limit the response length
    )
    return response.choices[0].text.strip()

@app.route("/", methods=["POST"])
def chat():
    user_input = request.json.get("user_input")
    intents = load_responses()
    
    if user_input.lower() in exit_phrase:
        response = random.choice(exit_response)
    else:
        response_json = get_response_from_json(user_input, intents)
        if response_json:
            response = response_json
        else:
            response_gpt = get_response_from_chatgpt(user_input)
            response = response_gpt
    
    # Generate and include the CSRF token in the JSON response
    csrf_token = csrf.generate_csrf()
    response_data = {"response": response, "csrf_token": csrf_token}
    
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)

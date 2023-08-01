import json
import random

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

def main():
    json_file_path = "intents.json"
    intents = load_responses(json_file_path)

    print("Chatbot: Hi! I'm your chatbot. Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        response = get_response(user_input, intents)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()

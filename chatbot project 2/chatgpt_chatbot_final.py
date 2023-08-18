import json
import random
import openai

openai.api_key = "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"

exit_phrase = ["bye", "see you", "good night", "goodbye", "cya", "talk to you later","good bye"]
exit_response = ["Bye!", "See you soon!", "Leaving so soon", "Thanks for visiting us!"]

def load_responses(file_path):
    with open(file_path, "r") as json_file:
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
        engine="text-davinci-003", 
        prompt=prompt,
        temperature=0.6, 
        max_tokens=2500
    )
    return response.choices[0].text.strip()

def main():
    json_file_path = "intents.json"
    intents = load_responses(json_file_path)

    print("Collabera's AI: Hi! I'm your chat assistant.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in exit_phrase:
            response = random.choice(exit_response)
            print("Collabera's AI:", response)
            break
        
        response_json = get_response_from_json(user_input, intents)
        if response_json:
            print("Collabera's AI:", response_json)
        else:
            response_gpt = get_response_from_chatgpt(user_input)
            print("Collabera's AI:", response_gpt)

if __name__ == "__main__":
    main()

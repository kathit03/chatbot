import random
import openai

openai.api_key = "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"

exit_phrase = ["bye", "see you", "good night", "goodbye", "cya", "talk to you later", "good bye"]
exit_response = ["Bye!", "See you soon!", "Leaving so soon", "Thanks for visiting us!"]

def load_responses(file_path):
    intents = []
    with open(file_path, "r") as txt_file:
        lines = txt_file.read().split("\n\n")
        for block in lines:
            intent = {"Patterns": [], "Responses": []}
            lines_in_block = block.split("\n")
            for line in lines_in_block:
                key_value = line.split(": ", 1)
                if len(key_value) == 2:
                    key = key_value[0]
                    value = key_value[1]
                    if key == "Intent":
                        intent["Intent"] = value
                    elif key == "Patterns":
                        intent["Patterns"] = value.split(", ")
                    elif key == "Responses":
                        intent["Responses"] = value.split(", ")
            if intent.get("Intent"):
                intents.append(intent)
    return intents


def get_random_response(intent):
    return random.choice(intent["Responses"])

def get_response_from_text(input_text, intents):
    for intent in intents:
        for pattern in intent["Patterns"]:
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
    txt_file_path = r"C:\Users\kathi\OneDrive\Desktop\chatbot project 2\intents1.txt"
    intents = load_responses(txt_file_path)

    print("Collabera's AI: Hi! I'm your chat assistant.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in exit_phrase:
            response = random.choice(exit_response)
            print("Collabera's AI:", response)
            break

        response_text = get_response_from_text(user_input, intents)
        if response_text:
            print("Collabera's AI:", response_text)
        else:
            response_gpt = get_response_from_chatgpt(user_input)
            print("Collabera's AI:", response_gpt)

if __name__ == "__main__":
    main()

import os
import openai
import json

openai.api_key = "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"

# Read the messages from the JSON file
with open("intents.json", "r") as json_file:
    messages = json.load(json_file)

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,  # Pass the messages read from the JSON file as a list
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

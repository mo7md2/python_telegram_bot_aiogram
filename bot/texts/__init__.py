import json


with open("bot/texts/buttons.json", "r", encoding="utf8") as file:
    button_texts = json.load(file)

with open("bot/texts/messages.json", "r", encoding="utf8") as file:
    message_texts = json.load(file)

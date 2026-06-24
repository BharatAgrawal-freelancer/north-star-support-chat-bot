import json
import random

from chatbot.intent_classifier import predict_intent

with open("data/intents.json", "r") as file:
    intents = json.load(file)["intents"]


def get_response(message):

    intent = predict_intent(message)

    if intent is None:
        return {
            "intent": "fallback",
            "response": (
                "I didn't understand that. "
                "I can help with order tracking, returns, "
                "product recommendations, or live support."
            )
        }

    for item in intents:

        if item["tag"] == intent:

            return {
                "intent": intent,
                "response": random.choice(item["responses"])
            }

    return {
        "intent": "fallback",
        "response": (
            "I didn't understand that. "
            "I can help with order tracking, returns, "
            "product recommendations, or live support."
        )
    }
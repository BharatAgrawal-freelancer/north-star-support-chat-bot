import json
import os


BASE_DIR = os.path.dirname(__file__)

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "activities.json"
)

with open(DATA_PATH, "r") as file:
    ACTIVITIES = json.load(file)["activities"]


def detect_activity(user_message):

    message = user_message.lower()

    for activity in ACTIVITIES:

        if activity["activity"].lower() in message:

            return activity

    return None


def get_recommendation(activity_name, weather):

    activity_name = activity_name.lower()
    weather = weather.lower()

    for activity in ACTIVITIES:

        if activity["activity"].lower() == activity_name:

            return (
                activity["weather"]
                .get(weather, {})
                .get("recommendations")
            )

    return None
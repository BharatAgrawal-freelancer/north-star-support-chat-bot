import json

with open("data/categories.json", "r") as file:
    CATEGORIES = json.load(file)["categories"]


def detect_category(user_message):

    message = user_message.lower()

    for category in CATEGORIES:

        for tag in category["tags"]:

            if tag.lower() in message:
                return category

    return None


def find_best_subcategory(category, user_requirement):

    requirement = user_requirement.lower()

    best_match = None
    best_score = 0

    for subcategory in category["subcategories"]:

        score = 0

        text = (
            subcategory["name"] +
            " " +
            subcategory["description"]
        ).lower()

        words = requirement.split()

        for word in words:

            if word in text:
                score += 1

        if score > best_score:

            best_score = score
            best_match = subcategory

    return best_match
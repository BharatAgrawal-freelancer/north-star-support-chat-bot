from services.recommendation_service import get_recommendation


def ask_activity():

    return (
    "I'd be happy to recommend the right outdoor gear.\n\n"
    "To get started, please select your planned activity:\n\n"
    "• Hiking\n"
    "• Camping\n"
    "• Climbing"
)


def ask_weather():

    return (
        "What weather conditions do you expect?\n\n"
        "- Cold\n"
        "- Warm\n"
        "- Rainy"
    )


def handle_recommendation(activity, weather):

    gear = get_recommendation(activity, weather)

    if not gear:

        return (
            "Sorry, I couldn't find recommendations for that combination."
        )

    items = "\n".join(
        f"• {item}" for item in gear
    )

    return (
      "Based on your selected activity and expected weather,\n\n"
    f"{items}\n\n"
    "I've returned you to the main menu.\n"
    "How else can I assist you today?"
    )
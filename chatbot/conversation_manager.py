from chatbot.response_engine import get_response

from chatbot.order_flow import handle_order_tracking

from chatbot.recommendation_flow import (
    ask_activity,
    ask_weather,
    handle_recommendation
)

from services.recommendation_service import detect_activity


conversation_state = "MAIN_MENU"
selected_activity = None


def process_message(user_message):

    global conversation_state
    global selected_activity

    # -----------------------------
    # ORDER FLOW
    # -----------------------------
    if conversation_state == "WAITING_FOR_ORDER_ID":

        conversation_state = "MAIN_MENU"

        return handle_order_tracking(user_message)

    # -----------------------------
    # ACTIVITY
    # -----------------------------
    if conversation_state == "WAITING_FOR_ACTIVITY":

        activity = detect_activity(user_message)

        if not activity:

           return (
    "I'd be happy to recommend the right outdoor gear.\n\n"
    "To get started, please select your planned activity:\n\n"
    "• Hiking\n"
    "• Camping\n"
    "• Climbing"
)

        selected_activity = activity["activity"]

        conversation_state = "WAITING_FOR_WEATHER"

        return ask_weather()

    # -----------------------------
    # WEATHER
    # -----------------------------
    if conversation_state == "WAITING_FOR_WEATHER":

        conversation_state = "MAIN_MENU"

        return handle_recommendation(
            selected_activity,
            user_message
        )

    # -----------------------------
    # NORMAL INTENT DETECTION
    # -----------------------------
    result = get_response(user_message)

    # ORDER TRACKING
    if result["intent"] == "order_tracking":

        conversation_state = "WAITING_FOR_ORDER_ID"

        return result["response"]

    # PRODUCT RECOMMENDATION
    if result["intent"] in (
    "general_recommendation",
    "specific_recommendation"
):

        conversation_state = "WAITING_FOR_ACTIVITY"

        return ask_activity()

    return result["response"]
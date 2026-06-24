from chatbot.response_engine import get_response
from services.order_service import get_order

from services.recommendation_service import (
    detect_category,
    find_best_subcategory
)

conversation_state = "MAIN_MENU"
selected_category = None


def process_message(user_message):

    global conversation_state
    global selected_category

    print("\n" + "=" * 50)
    print("NEW MESSAGE:", user_message)
    print("CURRENT STATE:", conversation_state)
    print("SELECTED CATEGORY:", selected_category)
    print("=" * 50)

    # -----------------------------
    # ORDER TRACKING FLOW
    # -----------------------------
    if conversation_state == "WAITING_FOR_ORDER_ID":

        print("INSIDE ORDER TRACKING FLOW")

        order = get_order(user_message)

        print("ORDER FOUND:", order)

        if order:

            conversation_state = "MAIN_MENU"

            status = order["status"]
            notes = order["active_notes"]

            print("STATE RESET TO:", conversation_state)

            if status == "Delivered":

                return (
                    f"Order #{order['order_id']} has been delivered.\n\n"
                    "Did you receive the package successfully?"
                )

            return (
                f"Order #{order['order_id']} status: {status}\n"
                f"Update: {notes}"
            )

        return (
            "I couldn't find that order number. "
            "Please verify it and try again."
        )

    # -----------------------------
    # PRODUCT RECOMMENDATION FLOW
    # -----------------------------
    if conversation_state == "WAITING_FOR_REQUIREMENTS":

        print("INSIDE REQUIREMENTS FLOW")

        recommendation = find_best_subcategory(
            selected_category,
            user_message
        )

        print("RECOMMENDATION RESULT:")
        print(recommendation)

        conversation_state = "MAIN_MENU"

        print("STATE RESET TO:", conversation_state)

        if recommendation:

            return (
                f"Based on your requirements, "
                f"I recommend our "
                f"{recommendation['name']} category.\n\n"
                f"{recommendation['description']}"
            )

        return (
            "I couldn't find an exact match.\n"
            "Could you provide a little more detail?"
        )

    # -----------------------------
    # NORMAL INTENT DETECTION
    # -----------------------------
    print("RUNNING INTENT DETECTION")

    result = get_response(user_message)

    print("INTENT RESULT:")
    print(result)

    # ORDER TRACKING
    if result["intent"] == "order_tracking":

        conversation_state = "WAITING_FOR_ORDER_ID"

        print("STATE CHANGED TO:", conversation_state)

        return result["response"]

    # PRODUCT RECOMMENDATION
    if result["intent"] == "specific_recommendation":

        category = detect_category(user_message)

        print("CATEGORY DETECTED:")
        print(category)

        if category:

            selected_category = category

            conversation_state = "WAITING_FOR_REQUIREMENTS"

            print("SELECTED CATEGORY SET:")
            print(selected_category["name"])

            print("STATE CHANGED TO:")
            print(conversation_state)

            return (
                f"Sure. I'd be happy to help with "
                f"{category['name']}.\n\n"
                f"Could you tell me more about your requirements?"
            )

        return (
            "What type of outdoor product are you looking for?\n\n"
            "Examples:\n"
            "- Tent\n"
            "- Backpack\n"
            "- Sleeping Bag\n"
            "- Hiking Jacket"
        )

    return result["response"]
from services.order_service import get_order


def handle_order_tracking(order_id):

    order = get_order(order_id)

    if order:

        if order["status"] == "Delivered":
            return (
                f"Order #{order['order_id']} has been delivered.\n\n"
                "Did you receive the package successfully?"
            )

        return (
            f"Order #{order['order_id']} status: {order['status']}\n"
            f"Update: {order['active_notes']}"
        )

    return (
        "Sorry, I couldn't find an order with that number.\n\n"
        "Please check your order number and try again later if needed.\n"
        "I've returned you to the main menu. How else can I help you today?"
    )
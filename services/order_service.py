import json

with open("data/orders.json", "r") as file:
    ORDERS = json.load(file)

def get_order(order_id):

    for order in ORDERS["orders"]:

        if order["order_id"] == str(order_id):
            return order

    return None
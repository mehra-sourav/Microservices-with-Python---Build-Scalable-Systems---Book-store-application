import requests
from flask import session
from . import ORDER_API_URL


class OrderClient:
    @staticmethod
    def get_order():
        headers = {
            'Authorization': session['user_api_key']
        }

        order_url = f"{ORDER_API_URL}/api/order/"
        response = requests.get(order_url, headers=headers)

        return response.json()

    @staticmethod
    def add_to_cart(book_id, quantity=1):
        headers = {
            'Authorization': session['user_api_key']
        }

        add_item_payload = {
            "book_id": book_id,
            "quantity": quantity
        }

        add_item_url = f"{ORDER_API_URL}/api/order/add-item"
        response = requests.post(add_item_url, data=add_item_payload, headers=headers)

        return response.json()

    @staticmethod
    def checkout():
        headers = {
            'Authorization': session['user_api_key']
        }

        checkout_url = f"{ORDER_API_URL}/api/order/checkout"
        response = requests.post(checkout_url, headers=headers)

        return response.json()

    @staticmethod
    def get_order_from_session():
        default_order = {
            "items": {}
        }
        return session.get('order', default_order)


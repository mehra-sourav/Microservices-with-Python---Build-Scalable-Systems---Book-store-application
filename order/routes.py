from flask import Blueprint, jsonify, make_response, request
from models import Order, OrderItem, db
import requests

order_blueprint = Blueprint('order_api_routes', __name__, url_prefix="/api/order")

USER_API_URL = "http://127.0.0.1:5001/api/user"


def get_user(api_key):
    headers = {
        'Authorization': api_key
    }

    # Making request to get user from USER API
    response = requests.get(USER_API_URL, headers=headers)

    print("GETUSER",response)
    # Unsuccessful response
    if response.status_code != 200:
        return {
            'message': 'Not Authorized!!'
        }

    # Successful response
    user = response.json()
    # print("user",user)

    return user


@order_blueprint.route('/', methods=["GET"])
def get_open_order():
    api_key = request.headers.get('Authorization')

    if not api_key:
        result = {
            "message": "Not logged in!!"
        }
        return make_response(jsonify(result), 401)

    response = get_user(api_key)
    user = response.get('user')

    if not user:
        result = {
            "message": "Not logged in!!"
        }
        return make_response(jsonify(result), 401)

    open_order = Order.query.filter_by(user_id=user['id'], is_open=1).first()

    if open_order:
        result = {
            "message": "Returning open order",
            "result": open_order.serialize()
        }
    else:
        result = {
            "message": "No open orders"
        }

    return make_response(jsonify(result), 200)


@order_blueprint.route('/all', methods=["GET"])
def get_all_orders():
    all_orders = Order.query.all()
    result = [order.serialize() for order in all_orders]
    response = {
        "message": "Returning all orders",
        "result": result
    }
    return make_response(jsonify(response), 200)


@order_blueprint.route('/add-item', methods=["POST"])
def add_order_item():
    api_key = request.headers.get('Authorization')

    if not api_key:
        result = {
            "message": "Not logged in!!"
        }
        return make_response(jsonify(result), 401)

    response = get_user(api_key)
    print('add item resp',response)
    # No user logged in or invalid api_key
    if not response.get('user'):
        result = {
            "message": "Not logged in!!"
        }
        return make_response(jsonify(result), 401)

    user = response.get('user')

    book_id = int(request.form['book_id'])
    quantity = int(request.form['quantity'])
    user_id = user['id']

    open_order = Order.query.filter_by(user_id=user_id, is_open=1).first()

    # If an open order already exists, then modify the quantity or add the new item in the items list
    if open_order:
        # Find the order item in the order item list and modify it if found in list
        # for item in open_order.order_items:
        item = [i for i in open_order.order_items if i.book_id == book_id]
        # If the item already exist within open_order.order_items
        if len(item) > 0:
            item = item[0]
            item.quantity += quantity
        # Otherwise, add item open_order.order_items
        else:
            order_item = OrderItem(book_id, quantity)
            open_order.order_items.append(order_item)
    # Else create a new open order and add the order item in it
    else:
        open_order = Order()
        open_order.is_open = True
        open_order.user_id = user_id

        order_item = OrderItem(book_id, quantity)
        open_order.order_items = [order_item]

    db.session.add(open_order)
    db.session.commit()

    res = {
        "message": "Item added successfully to the order",
        "result": open_order.serialize()
    }

    return make_response(jsonify(res), 200)


@order_blueprint.route('/checkout', methods=["POST"])
def checkout_order():
    api_key = request.headers.get('Authorization')

    if not api_key:
        result = {
            "message": "Not logged in!!"
        }
        return make_response(jsonify(result), 401)

    response = get_user(api_key)
    user = response.get('user')

    if not user:
        result = {
            "message": "Not logged in!!"
        }
        return make_response(jsonify(result), 401)

    open_order = Order.query.filter_by(user_id=user['id'], is_open=1).first()

    if open_order:
        open_order.is_open = False

        db.session.add(open_order)
        db.session.commit()

        result = {
            "message": "Order has been checked out",
            "result": open_order.serialize()
        }
    else:
        result = {
            "message": "No open orders"
        }

    return make_response(jsonify(result), 200)





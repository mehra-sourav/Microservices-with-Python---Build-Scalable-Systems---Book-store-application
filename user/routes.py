from flask import Blueprint, jsonify, request, make_response
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user

user_blueprint = Blueprint("user_api_routes",__name__,url_prefix='/api/user')

@user_blueprint.route('/all', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    result = [user.serialize() for user in all_users]
    response = {
        "message": "Returning all users",
        "result": result
    }
    return jsonify(response)


@user_blueprint.route('/create', methods=['POST'])
def create_user():
    try:
        user = User()
        user.username = request.form["username"]
        user.password = generate_password_hash(request.form["password"],
                                               method="sha256")

        # Should be set to false in production. Here it's set to true only for testing
        user.is_admin = True

        db.session.add(user)
        db.session.commit()
        response = {
            "message": "Used created successfully!",
            "result": user.serialize()
        }
    except Exception as e:
        print('Error-->', e)
        response = {
            "message": "Error while creating user!"
        }
    return jsonify(response)


@user_blueprint.route('/login', methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    # If no user with the given username exists
    if not user:
        response = {"message": "username or password doesn't exist"}
        # We won't lose the additional headers (status code here) when using make_response
        return make_response(jsonify(response), 401)

    # Else check the provided password against the user's saved hashed password
    if check_password_hash(user.password, password):
        user.update_api_key()
        # Saving changes to database
        db.session.commit()
        login_user(user)
        response = {
            "message": "User has been logged in!",
            "api_key": user.api_key
        }
        return make_response(jsonify(response), 200)

    response = {"message": "Access denied!!"}
    return make_response(jsonify(response), 401)


@user_blueprint.route('/logout', methods=["POST"])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return make_response(jsonify({"message": "User logged out!"}), 200)

    return make_response(jsonify({"message": "No user logged in!"}), 401)


@user_blueprint.route('/<username>/exists', methods=["GET"])
def user_exists(username):
    user = User.query.filter_by(username=username).first()

    # If no user with the given username exists
    if user:
        return make_response(jsonify({"result": True}), 200)

    return make_response(jsonify({"result": False}), 404)


@user_blueprint.route('/', methods=["GET"])
def get_current_user():
    if current_user.is_authenticated:
        return make_response(jsonify({"user": current_user.serialize()}), 200)

    return make_response(jsonify({"message": "No user logged in!"}), 401)





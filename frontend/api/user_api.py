import requests
from flask import session
from . import USER_API_URL


class UserClient:
    @staticmethod
    def login_user(form):
        api_key = None
        login_payload = {
            "username": form.username.data,
            "password": form.password.data
        }

        login_url = f"{USER_API_URL}/api/user/login"

        response = requests.post(login_url, data=login_payload)

        if response:
            api_key = response.json().get('api_key')
            user = response.json().get('user')

        return api_key, user

    @staticmethod
    def get_user():
        headers = {
            'Authorization': session['user_api_key']
        }

        get_user_url = f"{USER_API_URL}/api/user/"

        response = requests.get(get_user_url, headers)
        # response = requests.get(get_user_url)
        user = response.json().get('user', None)

        return user

    @staticmethod
    def create_user(form):
        user = None
        create_user_payload = {
            'username': form.username.data,
            'password': form.password.data
        }

        create_user_url = f"{USER_API_URL}/api/user/create"

        response = requests.post(create_user_url, data=create_user_payload)

        if response:
            user = response.json()

        return user

    @staticmethod
    def user_exists(username):
        user_exists_url = f"{USER_API_URL}/api/user/{username}/exists"
        response = requests.get(user_exists_url)
        return response.status_code == 200





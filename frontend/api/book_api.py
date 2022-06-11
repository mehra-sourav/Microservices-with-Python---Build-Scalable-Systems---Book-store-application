import requests
from . import BOOK_API_URL


class BookClient:
    @staticmethod
    def get_books():
        url = f"{BOOK_API_URL}/api/book/all"
        response = requests.get(url)
        result = response.json()['result']
        return result

    @staticmethod
    def get_book(slug):
        url = f"{BOOK_API_URL}/api/book/{slug}"
        response = requests.get(url)
        return response.json()



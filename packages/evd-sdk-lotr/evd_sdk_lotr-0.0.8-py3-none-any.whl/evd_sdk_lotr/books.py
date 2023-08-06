import requests

class Books():
    base_url = "https://the-one-api.dev/v2/book"

    def __init__(self, api_key: str):
        self.api_key = api_key

    """
    Lists of all "The Lord of the Rings" Books
    """

    def get_books(self):
        try:
            url = f"{self.base_url}"
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }
            books = requests.request("GET", url, headers=headers).json()
            return books

        except Exception as e:
            return e

    """
    Request one specific Lord of the Rings book by ID
    """

    def get_book_by_id(self, id):
        try:
            url = f"{self.base_url}/{id}"
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }
            book = requests.request("GET", url, headers=headers).json()["docs"][0]
            return book
        except Exception as e:
            return e

    """
    Request all chapters of one specific book
    """

    def get_all_chapters_of_book(self, id):
        try:
            url = f"{self.base_url}/{id}/chapter"
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }
            book_chapters = requests.request("GET", url, headers=headers).json()['docs']
            return book_chapters
        except Exception as e:
            return e

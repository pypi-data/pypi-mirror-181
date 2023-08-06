import requests
from evd_sdk_lotr.settings import BASE_URL

class Quotes():
    base_url = f"{BASE_URL}/quote"

    def __init__(self, api_key: str):
        self.api_key = api_key

    """
    List of all movie quotes
    """

    def get_all_movie_quotes(self):
        try:
            url = f"{self.base_url}"
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }

            quotes = requests.request("GET", url, headers=headers).json()['docs']
            return quotes

        except Exception as e:
            return e

    """
    Request one specific movie quote
    """

    def get_one_movie_quote_by_id(self, id):
        try:
            url = f"{self.base_url}/{id}"
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }

            quote = requests.request("GET", url, headers=headers).json()['docs'][0]
            return quote

        except Exception as e:
            return e

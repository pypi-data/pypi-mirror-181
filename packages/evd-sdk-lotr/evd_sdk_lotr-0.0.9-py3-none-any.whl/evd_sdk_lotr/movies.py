import requests
from evd_sdk_lotr.settings import BASE_URL

class Movies():
    base_url = f"{BASE_URL}/movie"

    def __init__(self, api_key: str):
        self.api_key = api_key

    """
    List of all movies including "The Lord of the Rings" and the "The Hobbit" trilogies
    """

    def get_movies(self):
            try:
                url = f"{self.base_url}"
                headers = {
                    'Accept': 'application/json',
                    'Authorization': f"Bearer {self.api_key}"
                }

                movies = requests.request("GET", url, headers=headers).json()['docs']
                return movies

            except Exception as e:
                return e

    """
    Request one specific movie by id
    """

    def get_movie_by_id(self, id):
        try:
            url = f"{self.base_url}/{id}"
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }

            movie = requests.request("GET", url, headers=headers).json()['docs'][0]
            return movie

        except Exception as e:
            return e

    """
    Request all movie quotes for one specific movie (only working for LOTR Trilogy)
    """

    def get_all_quotes_by_movie(self, id):
        try:
            url = f"{self.base_url}/{id}/quote"
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }

            movie_quotes = requests.request("GET", url, headers=headers).json()['docs']
            return movie_quotes

        except Exception as e:
            return e

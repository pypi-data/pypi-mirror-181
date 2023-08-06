import requests
from evd_sdk_lotr.settings import BASE_URL

class Characters():
    base_url = f"{BASE_URL}/character"

    def __init__(self, api_key: str):
        self.api_key = api_key

    """
    Lists of all characters including metadata like name, gender, realm, race and more
    """

    def get_all_characters(self):
        try:
            url = f"{self.base_url}"
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }

            characters = requests.request("GET", url, headers=headers).json()["docs"]
            return characters

        except Exception as e:
            return e

    """
    Request one specific character by id
    """

    def get_character_by_id(self, id):
        try:
            url = f"{self.base_url}/{id}"
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }

            character = requests.request("GET", url, headers=headers).json()['docs'][0]
            return character

        except Exception as e:
            return e

    """
    Request all movie quotes of one specific character
    """

    def get_quotes_by_character_id(self, id):
        try:
            url = f"{self.base_url}/{id}/quote"
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }

            character_quotes = requests.request("GET", url, headers=headers).json()['docs']
            return character_quotes

        except Exception as e:
            return e

    """
    Request character by name
    """

    def get_character_by_name(self, name):
        try:
            url = f"{self.base_url}?name={name}"
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }

            characters = requests.request("GET", url, headers=headers).json()["docs"][0]
            return characters

        except Exception as e:
            return e

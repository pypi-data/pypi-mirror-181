import requests

class Characters():
    base_url = "https://the-one-api.dev/v2/character"

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

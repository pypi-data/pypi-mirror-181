import requests

class Chapters():
    base_url = "https://the-one-api.dev/v2/chapter"

    def __init__(self, api_key: str):
        self.api_key = api_key

    """
    Lists of all book chapters
    """
    def get_all_book_chapters(self):
        try:
            url = f"{self.base_url}"
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }

            chapters = requests.request("GET", url, headers=headers).json()['docs']
            return chapters

        except Exception as e:
            return e


    """
    Request one specific book chapter
    """

    def get_book_chapter_by_id(self, id):
        try:
            url = f"{self.base_url}/{id}"
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }

            chapter = requests.request("GET", url, headers=headers).json()
            return chapter

        except Exception as e:
            return e

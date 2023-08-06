import requests
from evd_sdk_lotr.settings import BASE_URL

class Chapters():
    base_url = f"{BASE_URL}/chapter"

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

    """
    Request book chapter by name
    """

    def get_book_chapter_by_name(self, chapterName):
        try:
            url = f"{self.base_url}?chapterName={chapterName}"
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }

            chapter = requests.request("GET", url, headers=headers).json()['docs'][0]
            return {chapterName: chapter}

        except Exception as e:
            return e

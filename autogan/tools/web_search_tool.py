import time
import re
import requests
from typing import Optional, Dict
from urllib.parse import quote
from bs4 import BeautifulSoup
from autogan.utils.response import ResponseFuncType


class WebSearch:
    def __init__(self, google_search_config: Dict):
        """A class for google search

        :param search_config: JSON format of email_config {"cx": "", "key": ""}
        """
        self._cx = google_search_config["cx"]
        self._key = google_search_config["key"]

    def get_search_detail(self, keyword: str, start: int, agent_name: str, gen: str, response_func: ResponseFuncType)\
            -> Optional[str]:
        """Obtain the main text content of a search result page

        :param keyword: Search keywords
        :param start: Search result index offset
        :param agent_name:
        :param gen: Used to distinguish agent replies, deep thoughts, context compression, general summaries, clue summaries
            - main: agent replies
            - idea: deep thoughts
            - messages_summary: context compression
            - text_summary: general summaries
            - clue_summary: clue summaries
        :param response_func: Used to return results to the interface or terminal.

        :return: The main content of the page
        """

        result = self.google_search(keyword, start, 1)

        if result is None:
            return None

        url = result[0]["link"]

        response_func(agent_name, gen, "", False, 0, url, 0, None)

        # Obtain the main content of the URL page
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        main_text = soup.get_text()

        # Remove extra line breaks
        s = re.sub('\n+', '\n', main_text)

        if s:
            return s
        else:
            return None

    def google_search(self, keyword: str, start: int, num: int) -> Optional[list]:
        """Call Google web search interface

        :param keyword: Search keywords
        :param start: Search result index offset
        :param num: Get the number of results

        :return:
            --result_list: Search results list
            --is_success: Successful or not
        """

        # 接口参数
        url = "https://www.googleapis.com/customsearch/v1"

        params = {
            'q': quote(keyword),
            'start': start,
            'num': num,
            'cx': self._cx,
            'key': self._key,
        }

        loop = 3
        for i in range(loop):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()  # If the response status is not 200, throw an exception
                data = response.json()  # Parse the returned json data

                if 'items' not in data:
                    raise ValueError("The return value is empty.")

                # Extract the title, link, and snippet fields from each object in the items field.
                results = []
                for item in data['items']:
                    result = {
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'snippet': item.get('snippet', '')
                    }
                    results.append(result)

                return results
            except requests.HTTPError as http_err:
                time.sleep(5)
                if i == loop - 1:
                    print(f'HTTP error occurred: {http_err}')
                    return None
            except Exception as e:
                time.sleep(5)
                if i == loop - 1:
                    return None

import json
from typing import Optional, Dict

import requests

from autogan.oai.audio_config_utils import AudioSpeechRequestConfig


class ImageRequest:
    def __init__(
            self,
            prompt: str,
    ):
        self.openai = self._openai(prompt)

    @staticmethod
    def _openai(prompt: str):
        data = {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": "1024x1024",
            "quality": "hd",
            "n": 1
        }
        return data

    def openai_to_json(self):
        return json.dumps(self.openai)


def openai_image(api_key: Dict, request_config: AudioSpeechRequestConfig,
                 request_data: ImageRequest) -> Optional[dict]:
    url = "https://api.openai.com/v1/images/generations" if api_key["api_type"] == "openai" else api_key["url"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key['api_key']}",
    }
    data = request_data.openai_to_json()

    response = requests.post(url, headers=headers, data=data, timeout=request_config.request_timeout)
    for _ in range(request_config.max_retries):
        if response.status_code == 200:
            return response.json()
        else:
            response = requests.post(url, headers=headers, data=data, timeout=request_config.request_timeout)
    return None

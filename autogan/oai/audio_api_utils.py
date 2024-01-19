import json
from typing import Optional, Dict

import requests

from autogan.oai.audio_config_utils import AudioSpeechRequestConfig


class AudioSpeechRequest:
    def __init__(
            self,
            input_value: str,
            model: Optional[str] = None,
            voice: Optional[str] = None,
            speed: Optional[float] = None,
            response_format: Optional[str] = None,
    ):
        self.response_format = response_format if response_format else "mp3"
        self.openai = self._openai(input_value, self.response_format, model, voice, speed)

    @staticmethod
    def _openai(input_value: str, response_format: str, model: Optional[str] = None, voice: Optional[str] = None,
                speed: Optional[float] = None):
        data = {
            "model": model if model else "tts-1",
            "response_format": response_format,
            "input": input_value,
            "voice": voice if voice else "onyx",
            "speed": speed if speed else 1.0
        }
        return data

    def openai_to_json(self):
        return json.dumps(self.openai)


def openai_audio_speech(api_key: Dict, request_config: AudioSpeechRequestConfig,
                        request_data: AudioSpeechRequest) -> Optional[bytes]:
    print(api_key['api_key'])
    url = "https://api.openai.com/v1/audio/speech" if api_key["api_type"] == "openai" else api_key["url"]
    print(url)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key['api_key']}",
    }

    data = request_data.openai_to_json()

    response = requests.post(url, headers=headers, data=data, timeout=request_config.request_timeout)
    for _ in range(request_config.max_retries):
        if response.status_code == 200:
            return response.content
        else:
            response = requests.post(url, headers=headers, data=data, timeout=request_config.request_timeout)
    return None

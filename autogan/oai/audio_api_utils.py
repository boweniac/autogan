import json
import os
import time
import uuid
from typing import Optional, Dict

import requests


def openai_audio_speech(model: str, input: str, voice: str, api_key: Dict, request_timeout: int, max_retries: int, work_dir: str, file_name: str, response_format: Optional[str] = "mp3",
                            speed: Optional[float] = 1.0) -> bool:
    url = "https://api.openai.com/v1/audio/speech"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key['api_key']}",
    }

    data = {
        "model": model,
        "input": input,
        "voice": voice,
        "response_format": response_format,
        "speed": speed
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=request_timeout)
    for _ in range(max_retries):
        print(f"response.status_code: {response.status_code}")
        print(f"response.content: {response.content}")
        if response.status_code == 200:
            with open(f"{work_dir}{file_name}.{response_format}", 'wb') as f:
                f.write(response.content)
            return True
        else:
            response = requests.post(url, headers=headers, data=json.dumps(data),timeout=request_timeout)
    return False

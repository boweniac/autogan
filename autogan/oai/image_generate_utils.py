import concurrent.futures
import time
import uuid
from typing import Optional

from apps.web_demo.backend.utils.aliyun.aliyun_oss import bucket
from autogan import dict_from_json
from autogan.oai.audio_config_utils import AudioSpeechConfig
from autogan.oai.image_api_utils import ImageRequest, openai_image
from autogan.utils.audio_utils import audio_to_lip


def generate_image(request: ImageRequest) \
        -> Optional[str]:
    """
    """
    image_config_dict = dict_from_json("Image")
    image_config = AudioSpeechConfig(image_config_dict)

    loop = image_config.len_of_api_key_list

    for i in range(loop):
        api_key = image_config.api_key(i)
        try:
            content = openai_image(api_key, image_config.request_config, request)
            print(f"content: {content}")
            if content and "data" in content and len(content["data"]) >= 1 and "url" in content["data"][0]:
                return content["data"][0]["url"]
            else:
                raise ValueError("Failed to generate image")
        except Exception as e:
            if i == loop - 1:
                print(f"audio generate Exception: {e}")
                return None

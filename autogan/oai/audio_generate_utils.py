import concurrent.futures
import time
import uuid
from typing import Optional

from apps.web_demo.backend.utils.aliyun.aliyun_oss import bucket
from autogan import dict_from_json
from autogan.oai.audio_api_utils import openai_audio_speech, AudioSpeechRequest
from autogan.oai.audio_config_utils import AudioSpeechConfig
from autogan.utils.audio_utils import audio_to_lip


def generate_audio(request: AudioSpeechRequest) \
        -> tuple[Optional[str], Optional[str]]:
    """
    """
    audio_speech_config_dict = dict_from_json("AUDIO_SPEECH")
    audio_speech_config = AudioSpeechConfig(audio_speech_config_dict)

    loop = audio_speech_config.len_of_api_key_list

    file_name = create_time_based_uuid()

    for i in range(loop):
        api_key = audio_speech_config.api_key(i)
        try:
            content = openai_audio_speech(api_key, audio_speech_config.request_config, request)
            if content:
                absolute_work_dir = audio_speech_config.request_config.work_dir
                response_format = request.response_format
                with open(f"{absolute_work_dir}{file_name}.{response_format}", 'wb') as f:
                    f.write(content)
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future_put_object_from_file = executor.submit(bucket.put_object_from_file,
                                                                  f"{file_name}.{response_format}",
                                                                  f"{absolute_work_dir}{file_name}.{response_format}")
                    future_audio_to_lip = executor.submit(audio_to_lip,
                                                          absolute_work_dir,
                                                          file_name,
                                                          response_format)

                    future_put_object_from_file.result()  # this will wait until upload_file is done
                    lips_data = future_audio_to_lip.result()  # this will wait until analyze_file is done
                if lips_data:
                    return f"{file_name}.{response_format}", lips_data
            else:
                raise ValueError("Failed to generate audio")
        except Exception as e:
            if i == loop - 1:
                print(f"audio generate Exception: {e}")
                return None, None


def create_time_based_uuid():
    # 获取当前时间的时间戳
    timestamp = time.time()

    # 创建一个基于时间戳的UUID
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(timestamp)))

import concurrent.futures
import os
import time
import uuid
from typing import Optional, List

from apps.web_demo.backend.util.aliyun_oss import bucket
from autogan import dict_from_json
from autogan.oai.audio_api_utils import openai_audio_speech
from autogan.oai.chat_api_utils import chat_completions, process_response
from autogan.oai.config_utils import LLMConfig, AgentConfig
from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.protocol.response_protocol import ResponseProtocol
from autogan.utils.audio_utils import audio_to_lip


def generate_audio(llm_config: str, model: str, input: str, voice: str, response_format: Optional[str] = "mp3",
                   speed: Optional[float] = 1.0) \
        -> tuple[Optional[str], Optional[str]]:
    """Call the LLM interface

    Currently, only the chatgpt model of openai (including azure) is adapted.

    :param llm_config: LLM configuration.
    :param messages:
    :param agent_name:
    :param gen: Used to distinguish agent replies, deep thoughts, context compression, general summaries, clue summaries
        - main: agent replies
        - idea: deep thoughts
        - messages_summary: context compression
        - text_summary: general summaries
        - clue_summary: clue summaries
    :param response_proxy: Used to return results to the interface or terminal.
    :param stream_mode:
    """

    # When a certain configuration in the configuration list fails to request,
    # continue to try the next configuration until all configurations in the list are attempted.
    llm_config_dict = dict_from_json(llm_config)
    llm_config = AgentConfig(llm_config_dict).main_model_config

    loop = llm_config.len_of_api_key_list
    request_timeout = llm_config.request_timeout
    max_retries = llm_config.max_retries
    file_name = create_time_based_uuid()

    work_dir = os.getcwd() + "/extensions/"
    os.makedirs("extensions", exist_ok=True)

    for i in range(loop):
        api_key = llm_config.next_api_key
        if api_key["api_type"] == "openai":
            try:
                is_success = openai_audio_speech(model, input, voice, api_key, request_timeout,
                                                max_retries, work_dir, file_name, response_format, speed)

                if is_success:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future_put_object_from_file = executor.submit(bucket.put_object_from_file, f"{file_name}.{response_format}", f"{work_dir}{file_name}.{response_format}")
                        future_audio_to_lip = executor.submit(audio_to_lip, work_dir, file_name, response_format)

                        future_put_object_from_file.result()  # this will wait until upload_file is done
                        lips_data = future_audio_to_lip.result()  # this will wait until analyze_file is done

                    # bucket.put_object_from_file(file_name, f"{work_dir}{file_name}.{response_format}")
                    # lips_data = audio_to_lip(work_dir, file_name, response_format)
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

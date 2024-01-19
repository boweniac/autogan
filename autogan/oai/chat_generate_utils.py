import time
from typing import Optional
from autogan.oai.chat_api_utils import chat_completions, process_response, ChatCompletionsRequest
from autogan.oai.chat_config_utils import LLMConfig
from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.oai.conv_holder import ConvHolder


def generate_chat_completion(llm_config: LLMConfig, request_data: ChatCompletionsRequest, conv_info: ConvHolder,
                             content_type: str) \
        -> tuple[Optional[str], Optional[int]]:
    """Call the LLM interface

    Currently, only the chatgpt model of openai (including azure) is adapted.

    :param llm_config: LLM configuration.
    :param request_data:
    :param conv_info:
    :param content_type:
    """

    # When a certain configuration in the configuration list fails to request,
    # continue to try the next configuration until all configurations in the list are attempted.
    loop = llm_config.len_of_api_key_list
    for i in range(loop):
        time.sleep(llm_config.request_config.request_interval_time)
        print(f"llm_config: {llm_config}")
        api_key = llm_config.next_api_key
        print(f"api_key: {api_key}")
        try:
            completion_content = ""
            completion_tokens = 0
            index = 1
            for message in chat_completions(api_key, llm_config.request_config, request_data):
                if conv_info.response_proxy.need_to_stop():
                    break
                else:
                    content, tokens = process_response(message, request_data.stream_mode)
                    if content:
                        completion_content += content
                        completion_tokens = tokens
                        conv_info.response(index,
                                           content_type,
                                           content,
                                           completion_tokens,
                                           message)
                        index += 1

            if completion_content:
                if completion_tokens == 0:
                    completion_tokens = count_text_tokens(completion_content, api_key['model'])
                conv_info.response(index,
                                   content_type,
                                   '[DONE]',
                                   completion_tokens,
                                   None)
                return completion_content, completion_tokens
            else:
                raise ValueError("The return value is empty.")
        except Exception as e:
            if i == loop - 1:
                print(f"generate_chat_completion Exception: {e}")
                return None, None


async def a_generate_chat_completion(llm_config: LLMConfig, request_data: ChatCompletionsRequest, conv_info: ConvHolder,
                                     content_type: str) \
        -> tuple[Optional[str], Optional[int]]:
    """Call the LLM interface

    Currently, only the chatgpt model of openai (including azure) is adapted.

    :param llm_config: LLM configuration.
    :param request_data:
    :param conv_info:
    :param content_type:
    """

    # When a certain configuration in the configuration list fails to request,
    # continue to try the next configuration until all configurations in the list are attempted.
    loop = llm_config.len_of_api_key_list
    for i in range(loop):
        time.sleep(llm_config.request_config.request_interval_time)
        api_key = llm_config.next_api_key
        try:
            completion_content = ""
            completion_tokens = 0
            index = 1
            for message in chat_completions(api_key, llm_config.request_config, request_data):
                if conv_info.response_proxy.need_to_stop():
                    break
                else:
                    content, tokens = process_response(message, request_data.stream_mode)
                    if content:
                        completion_content += content
                        completion_tokens = tokens
                        await conv_info.a_response(index,
                                                   content_type,
                                                   content,
                                                   completion_tokens,
                                                   message)
                        index += 1

            if completion_content:
                if completion_tokens == 0:
                    completion_tokens = count_text_tokens(completion_content, api_key['model'])
                await conv_info.a_response(index,
                                           content_type,
                                           '[DONE]',
                                           completion_tokens,
                                           None)
                return completion_content, completion_tokens
            elif not conv_info.response_proxy.need_to_stop():
                raise ValueError("The return value is empty.")
            else:
                return None, None
        except Exception as e:
            if i == loop - 1:
                print(f"generate_chat_completion Exception: {e}")
                return None, None


def generate_chat_completion_internal(llm_config: LLMConfig, request_data: ChatCompletionsRequest) \
        -> tuple[Optional[str], Optional[int]]:
    """Call the LLM interface

    Currently, only the chatgpt model of openai (including azure) is adapted.

    :param llm_config: LLM configuration.
    :param request_data:
    """

    # When a certain configuration in the configuration list fails to request,
    # continue to try the next configuration until all configurations in the list are attempted.
    loop = llm_config.len_of_api_key_list
    for i in range(loop):
        time.sleep(llm_config.request_config.request_interval_time)
        api_key = llm_config.next_api_key
        try:
            message = chat_completions(api_key, llm_config.request_config, request_data)
            content, tokens = process_response(message, False)
            if content:
                if tokens == 0:
                    tokens = count_text_tokens(tokens, api_key['model'])
                return content, tokens
            else:
                raise ValueError("The return value is empty.")
        except Exception as e:
            if i == loop - 1:
                print(f"generate_chat_completion Exception: {e}")
                return None, None

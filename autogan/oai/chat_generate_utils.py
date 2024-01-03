import time
from typing import Optional, List
from autogan.oai.chat_api_utils import chat_completions, process_response
from autogan.oai.config_utils import LLMConfig
from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.protocol.response_protocol import ResponseProtocol


def generate_chat_completion(llm_config: LLMConfig, messages: List, agent_name: str, gen: str,
                             response_proxy: ResponseProtocol, stream_mode: Optional[bool] = None,
                             msg_id: Optional[int] = None, task_id: Optional[int] = None) \
        -> tuple[Optional[str], Optional[int]]:
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
    loop = llm_config.len_of_api_key_list
    for i in range(loop):
        time.sleep(llm_config.request_interval_time)
        api_key = llm_config.next_api_key
        try:
            completion_content = ""
            completion_tokens = 0
            index = 1
            for message in chat_completions(messages, api_key, llm_config.request_timeout,
                                            llm_config.max_retries, stream_mode):
                if response_proxy.need_to_stop():
                    break
                else:
                    content, tokens = process_response(message, stream_mode)
                    if content:
                        completion_content += content
                        completion_tokens = tokens
                        response_proxy.send(agent_name, gen, api_key["model"], stream_mode, index, content,
                                            completion_tokens, message, msg_id, task_id)
                        index += 1

            if completion_content:
                if completion_tokens == 0:
                    completion_tokens = count_text_tokens(completion_content, api_key['model'])
                response_proxy.send(agent_name, gen, api_key["model"], stream_mode, index, '[DONE]', completion_tokens, None, msg_id, task_id)
                return completion_content, completion_tokens
            else:
                raise ValueError("The return value is empty.")
        except Exception as e:
            if i == loop - 1:
                print(f"generate_chat_completion Exception: {e}")
                return None, None


async def a_generate_chat_completion(llm_config: LLMConfig, messages: List, agent_name: str, gen: str,
                                     response_proxy: ResponseProtocol, stream_mode: Optional[bool] = None,
                                     msg_id: Optional[int] = None, task_id: Optional[int] = None) \
        -> tuple[Optional[str], Optional[int]]:
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
    loop = llm_config.len_of_api_key_list
    for i in range(loop):
        time.sleep(llm_config.request_interval_time)
        api_key = llm_config.next_api_key
        try:
            completion_content = ""
            completion_tokens = 0
            index = 1
            for message in chat_completions(messages, api_key, llm_config.request_timeout,
                                            llm_config.max_retries, stream_mode):
                if response_proxy.need_to_stop():
                    break
                else:
                    content, tokens = process_response(message, stream_mode)
                    if content:
                        completion_content += content
                        completion_tokens = tokens
                        await response_proxy.a_send(agent_name, gen, api_key["model"], stream_mode, index, content,
                                                    completion_tokens, message, msg_id, task_id)
                        index += 1

            if completion_content:
                if completion_tokens == 0:
                    completion_tokens = count_text_tokens(completion_content, api_key['model'])
                return completion_content, completion_tokens
            elif not response_proxy.need_to_stop():
                raise ValueError("The return value is empty.")
            else:
                return None, None
        except Exception as e:
            if i == loop - 1:
                print(f"generate_chat_completion Exception: {e}")
                return None, None


def generate_chat_completion_internal(llm_config: LLMConfig, messages: List) \
        -> tuple[Optional[str], Optional[int]]:
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
    loop = llm_config.len_of_api_key_list
    for i in range(loop):
        time.sleep(llm_config.request_interval_time)
        api_key = llm_config.next_api_key
        try:
            message = chat_completions(messages, api_key, llm_config.request_timeout,
                                       llm_config.max_retries, False)
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

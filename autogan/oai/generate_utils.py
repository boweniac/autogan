import time
from typing import Optional, List
from autogan.oai.openai_utils import chat_completions
from autogan.oai.config_utils import LLMConfig
from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.utils.response import ResponseFuncType


def generate_chat_completion(llm_config: LLMConfig, messages: List, agent_name: str, gen: str,
                             response_func: ResponseFuncType, stream_mode: Optional[bool] = None)\
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
    :param response_func: Used to return results to the interface or terminal.
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
                content = ""
                if stream_mode:
                    if (message and "choices" in message and "delta" in message["choices"][0]
                            and "content" in message["choices"][0]["delta"]
                            and message["choices"][0]["delta"]["content"]):
                        content = message["choices"][0]["delta"]["content"]
                        completion_content += content
                else:
                    if (message and "choices" in message and "message" in message["choices"][0]
                            and "content" in message["choices"][0]["message"]
                            and message["choices"][0]["message"]["content"]):
                        content = message["choices"][0]["message"]["content"]
                        completion_content = content
                    if message and "usage" in message and "completion_tokens" in message["usage"]:
                        completion_tokens = message["usage"]["completion_tokens"]
                response_func(agent_name, gen, api_key["model"], stream_mode, index, content, completion_tokens, message)
                if content:
                    index += 1

            if completion_content:
                if completion_tokens == 0:
                    completion_tokens = count_text_tokens(completion_content, api_key['model'])
                return completion_content, completion_tokens
            else:
                raise ValueError("The return value is empty.")
        except Exception as e:
            if i == loop - 1:
                print(f"generate_chat_completion Exception: {e}")
                return None, None

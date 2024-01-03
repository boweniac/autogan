import json
import requests
from typing import Dict, Optional
from openai import OpenAI, AzureOpenAI
from autogan.utils.response import obj_to_dict


def chat_completions(messages: list, api_key: Dict, request_timeout: int, max_retries: int,
                     stream_mode: Optional[bool] = None):
    """OpenAI interface and OpenAI like interface call

        :param messages:
        :param api_key: LLM configuration.
        :param request_timeout:
        :param max_retries:
        :param stream_mode:
    """
    if api_key["api_type"] == "openai" or api_key["api_type"] == "azure":
        return openai_chat_completions(messages, api_key, request_timeout, max_retries, stream_mode)
    else:
        return openai_like_chat_completions(messages, api_key, request_timeout, max_retries, stream_mode)


def process_response(message: dict, stream_mode: Optional[bool] = None):
    content = ""
    tokens = 0
    if stream_mode:
        if (message and "choices" in message and "delta" in message["choices"][0]
                and "content" in message["choices"][0]["delta"]
                and message["choices"][0]["delta"]["content"]):
            content = message["choices"][0]["delta"]["content"]
    else:
        if (message and "choices" in message and "message" in message["choices"][0]
                and "content" in message["choices"][0]["message"]
                and message["choices"][0]["message"]["content"]):
            content = message["choices"][0]["message"]["content"]
        if message and "usage" in message and "completion_tokens" in message["usage"]:
            tokens = message["usage"]["completion_tokens"]

    return content, tokens


def openai_chat_completions(messages: list, api_key: Dict, request_timeout: int, max_retries: int,
                            stream_mode: Optional[bool] = None):
    if stream_mode is None:
        stream_mode = False
    if api_key["api_type"] == "openai":
        client = OpenAI(
            api_key=api_key["api_key"],
            timeout=request_timeout,
            max_retries=max_retries
        )
    else:
        client = AzureOpenAI(
            api_key=api_key["api_key"],
            api_version=api_key["api_version"],
            azure_endpoint=api_key["api_base"],
            timeout=request_timeout,
            max_retries=max_retries
        )

    completion = client.chat.completions.create(
        model=api_key["model"],
        messages=messages,
        stream=stream_mode,
        temperature=0.1
    )

    if completion:
        if stream_mode:
            response = completion
        else:
            response = [completion]

        for message in response:
            yield obj_to_dict(message)
    else:
        yield None


def openai_like_chat_completions(messages: list, api_key: Dict, request_timeout: int, max_retries: int,
                                 stream_mode: Optional[bool] = None):
    headers = {
        "Content-Type": "application/json",
    }
    if "Authorization" in api_key:
        headers['Authorization'] = api_key["Authorization"]

    data = {
        "model": api_key["model"],
        "messages": messages,
        "temperature": 0.1,
        "stream": stream_mode
    }

    if stream_mode:
        with requests.post(api_key["url"], headers=headers, data=json.dumps(data), timeout=request_timeout,
                           stream=True) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            line_str = line_str[6:]
                            if line_str != "[DONE]":
                                yield json.loads(line_str)
                        else:
                            print(f"err_data: {line_str}")
            return None
    else:
        response = requests.post(api_key["url"], headers=headers, data=json.dumps(data), timeout=request_timeout)
        for _ in range(max_retries):
            if response.status_code == 200:
                yield response.json()
                return
            else:
                response = requests.post(api_key["url"], headers=headers, data=json.dumps(data),
                                         timeout=request_timeout)
        return None

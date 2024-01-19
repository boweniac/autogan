import json
import requests
from typing import Dict, Optional

from openai import OpenAI, AzureOpenAI

from autogan.oai.chat_config_utils import LLMRequestConfig
from autogan.utils.response import obj_to_dict


class ChatCompletionsRequest:
    def __init__(
            self,
            messages: list[Dict],
            stream_mode: bool,
            temperature: Optional[float] = None,
    ):
        self.messages = messages
        self.stream_mode = stream_mode
        self.temperature = temperature if temperature else 0.1

    def openai(self, model: str):
        data = {
            "model": model,
            "messages": self.messages,
            "stream": self.stream_mode,
            "temperature": self.temperature
        }
        return data

    def openai_to_json(self, model: str):
        return json.dumps(self.openai(model))


def chat_completions(api_key: Dict, request_config: LLMRequestConfig, request_data: ChatCompletionsRequest):
    """OpenAI interface and OpenAI like interface call

        :param api_key: LLM configuration.
        :param request_config: request configuration.
        :param request_data:
    """
    if api_key["api_type"] == "openai" or api_key["api_type"] == "azure":
        return openai_chat_completions(api_key, request_config, request_data)
    else:
        return openai_like_chat_completions(api_key, request_config, request_data)


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


def openai_chat_completions(api_key: Dict, request_config: LLMRequestConfig, request_data: ChatCompletionsRequest):
    if api_key["api_type"] == "openai":
        client = OpenAI(
            api_key=api_key["api_key"],
            timeout=request_config.request_timeout,
            max_retries=request_config.max_retries
        )
    else:
        client = AzureOpenAI(
            api_key=api_key["api_key"],
            api_version=api_key["api_version"],
            azure_endpoint=api_key["api_base"],
            timeout=request_config.request_timeout,
            max_retries=request_config.max_retries
        )

    completion = client.chat.completions.create(
        model=api_key["model"],
        messages=request_data.messages,
        stream=request_data.stream_mode,
        temperature=request_data.temperature
    )

    if completion:
        if request_data.stream_mode:
            response = completion
        else:
            response = [completion]

        for message in response:
            yield obj_to_dict(message)
    else:
        yield None


def openai_like_chat_completions(api_key: Dict, request_config: LLMRequestConfig, request_data: ChatCompletionsRequest):
    headers = {
        "Content-Type": "application/json",
    }
    if "Authorization" in api_key:
        headers['Authorization'] = api_key["Authorization"]

    data = request_data.openai_to_json(api_key["model"])
    print(f"request_data: {data}")
    if request_data.stream_mode:
        with requests.post(api_key["url"], headers=headers, data=data,
                           timeout=request_config.request_timeout,
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
        response = requests.post(api_key["url"], headers=headers, data=data,
                                 timeout=request_config.request_timeout)
        for _ in range(request_config.max_retries):
            if response.status_code == 200:
                yield response.json()
                return
            else:
                response = requests.post(api_key["url"], headers=headers, data=data,
                                         timeout=request_config.request_timeout)
        return None

from typing import Optional
from autogan.oai.chat_api_utils import ChatCompletionsRequest
from autogan.oai.chat_config_utils import LLMConfig
from autogan.utils.environment_utils import environment_info
from autogan.oai.chat_generate_utils import generate_chat_completion_internal


def compressed_texts(lang: str, texts: list, summary_model_config: LLMConfig, focus: str, safe_size: int) -> tuple[
    Optional[str], Optional[int]]:
    total_tokens = 0
    total_text = ""
    values = []
    for st in texts:
        print(f"st: {st}")
        content, tokens = generate_text_focus(lang, st, focus, summary_model_config)
        print(f"content1: {content}")
        print(f"contentType: {type(content)}")
        print(f"tokens1: {tokens}")
        print(f"tokensType: {type(tokens)}")
        if content:
            values.append((content, tokens))
            total_tokens += tokens
            total_text += content
    print(f"total_text: {total_text}")
    print(f"total_tokens: {total_tokens}")
    print(f"safe_size: {safe_size}")
    while total_tokens > safe_size:
        total_tokens = 0
        total_text = ""
        data = []
        t = 0
        x = ""
        for v in values:
            t += v[1]
            x += v[0]
            if t > safe_size:
                content, tokens = generate_text_focus(lang, x, focus, summary_model_config)
                if content:
                    data.append((content, tokens))
                    total_tokens += tokens
                    total_text += content
                t = 0
                x = ""
        content, tokens = generate_text_focus(lang, x, focus, summary_model_config)
        if content:
            data.append((content, tokens))
            total_tokens += tokens
            total_text += content

        values = data

    return total_text, total_tokens


def generate_text_focus(lang: str, text: str, focus: str, summary_model_config: LLMConfig) -> tuple[str, int]:
    info = environment_info()
    if lang == "CN":
        system_prompt = """# 角色
你是一个善于实时发现真相的特工

## 技能
能够从用户发送的信息中找到有助于推断问题答案的内容。

## 约束条件
- 请注意，如果信息的内容没有有价值的信息，请省略其他礼貌用语，只输出一个单词:None。
- 请帮我过滤掉信息中涉及政治、地缘政治、暴力、性等敏感内容。"""
        chat_messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user',
                                                                        'content': f'需要推断的问题是:{focus}\n\n当前时间是:\n{info}\n\n信息内容是:\n\n{text}'}]
    else:
        system_prompt = """# role
You are an agent who is good at discovering the truth in real-time

## Skills
capable of finding content that helps infer the answer to the question from the information sent by users

## Constraints
- Please note that if the content of the information has no extractable value, please omit other polite expressions and output only one word: None.
- please help me filter out sensitive content related to politics, geopolitics, violence, and sex in the information."""
        chat_messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user',
                                                                        'content': f'The current question is:{focus}\n\nEnvironmental information:\n{info}\n\nMaterial content:\n\n{text}'}]
    print(f"chat_messages: {chat_messages}")
    request_data = ChatCompletionsRequest(chat_messages, False)
    return generate_chat_completion_internal(summary_model_config, request_data)

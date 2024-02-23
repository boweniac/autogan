from typing import Optional

from autogan.utils.environment_utils import environment_info


class CompressedTextPrompts:
    def __init__(self, lang: str):
        """该类用于构建深思提示词，深思过程和提示词模板可通过 consider_prompts 变量进行设置

        :param lang: 语言"""

        self._lang = lang

    def summary(self, text: str, safe_size: Optional[int]) -> tuple[str, str]:
        system_prompt = {
            "CN": f"""# 角色
我希望你是一个文章过滤和提炼器。

## 技能
对用户发送的文章进行过滤和提炼。

## 要求
{"- 请确保你的摘要不超过 max_tokens 的限制。" if safe_size else ""}
- 当文章没有值得提炼的内容时，请省略其他礼貌用语，只输出一个词：None。
- 如果文章可以被提炼，那么请帮我从文章中过滤出与政治、地缘政治、暴力和性有关的敏感内容，并从文章中提取主要内容。
- 请注意，提取的内容的描述视角和章节结构应尽可能与原文一致，并尽量保留细节以供后续推理。请省略其他礼貌用语，只输出提炼的内容。""",
            "EN": f"""# Role
I want you to be an article filter and refiner.

## Skills
Filter and refine the articles sent by users.

## Requirements
{"- Please make sure your summary does not exceed the limit of max_tokens." if safe_size else ""}
- When the article has no content worth refining, please omit other polite language and only output one word: None.
- If the article can be refined, please help me filter out sensitive content related to politics, geopolitics, violence, and sex from the article, and extract the main content from the article.
- Please note that the description perspective and chapter structure of the extracted content should be as consistent as possible with the original text, and try to retain details for subsequent reasoning. Please omit other polite language and only output the refined content."""
        }
        chat_prompt = {
            "CN": f"""{"max_tokens: "+str(safe_size) if safe_size else ""}
文章内容:\n{text}""",
            "EN": f"""{"max_tokens: "+str(safe_size) if safe_size else ""}
Article content:\n{text}"""
        }

        return system_prompt[self._lang], chat_prompt[self._lang]

    def clue(self, text: str, focus: str) -> tuple[str, str]:
        info = environment_info()

        system_prompt = {
            "CN": f"""# 角色
我希望你是一个善于发现实时真相的探员。

## 技能
能从用户发送的资料中帮我找到有助于推断出问题答案的内容。

## 要求
- 当资料中没有值得提取的内容时，请省略其他礼貌用语，只输出一个词：None。
- 如果文章可以被提炼，那么请帮我从文章中过滤出与政治、地缘政治、暴力和性有关的敏感内容，并从文章中提取主要内容。
- 回复内容中除了你的推理结果，还需要包含 url (如有)和相关原文的摘要。""",
            "EN": f"""# Role
I hope you are a detective who is good at discovering the truth in real-time..

## Skills
Able to help me find content from the information sent by users that can help infer the answer to the question.

## Requirements
- When there is no content worth extracting in the information, please omit other polite expressions and only output one word: None.
- If the article can be refined, please help me filter out sensitive content related to politics, geopolitics, violence, and sex from the article, and extract the main content from the article.
- In addition to your reasoning results, the response content also needs to include the url (if any) and a summary of the relevant original text."""
        }
        chat_prompt = {
            "CN": f"""当前的问题是: {focus}

环境信息: {info}

资料内容:\n{text}""",
            "EN": f"""The current question is: {focus}

Environmental information: {info}

Material content:\n{text}"""
        }

        return system_prompt[self._lang], chat_prompt[self._lang]

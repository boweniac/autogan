import math
import re
from typing import Optional, List

from autogan.oai.chat_api_utils import ChatCompletionsRequest
from autogan.oai.chat_config_utils import LLMConfig
from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.prompt.utils.compressed_text_prompts import CompressedTextPrompts
from autogan.utils.environment_utils import environment_info
from autogan.oai.chat_generate_utils import generate_chat_completion_internal


def compressed_text_universal(lang: str, text: str,
                              summary_model_config: LLMConfig,
                              focus: Optional[str] = None,
                              safe_size: Optional[int] = None) -> tuple[Optional[str], Optional[int]]:
    """Compress the text, generating either a regular summary or a cue summary.
    压缩文本，可生成普通摘要或线索摘要。

    First, the long text is sliced, and then a summary is generated for each slice.
    首先将长文本切片，然后逐切片的生成摘要。

    If the value of the focus parameter is not None, then the attention will be focused on the focus area while generating the summary.
    如 focus 参数的值不为 None 则在生成摘要时注意力集中于 focus。

    If the value of the safe_size parameter is not None and the length of the initial compression result exceeds the safe_size, the summary will be further compressed, with the compressed size expected to stay within the range of the safe_size.
    如 safe_size 参数的值不为 None 且初次压缩结果长度超过 safe_size，则会对摘要进一步压缩，压缩后的大小被期望保持在 safe_size 范围之内。

    :param text: Text to be compressed.
        待压缩的文本。
    :param summary_model_config: LLM configuration used for text compression.
        用于压缩文本的 LLM 配置。
    :param focus: The focus direction when compressing text.
        压缩文本时的专注方向。
    :param safe_size: The target size of the text after compression, if not provided there is no limit.
        文本压缩后的目标尺寸，如果为空则不做限制。

    :return:
        --compressed_text: The text after compression.
            压缩后的文本。
        --total_tokens: Total tokens after compression.
            压缩后的整体tokens。
    """

    compressed_text = ""
    total_tokens = 0

    split_texts = split_text(text, summary_model_config.request_config.max_messages_tokens, summary_model_config.model)

    for st in split_texts:
        if focus:
            content, tokens = generate_text_clues(lang, st, focus, summary_model_config)
        else:
            content, tokens = generate_text_summary(lang, st, summary_model_config)

        if content != "None":
            compressed_text += content + "\n"
            total_tokens += tokens

    if compressed_text:
        if safe_size and safe_size < total_tokens:
            return compressed_text_into_safe_size(lang, compressed_text, safe_size, summary_model_config)
        else:
            return compressed_text, total_tokens
    else:
        return None, None


def compressed_text_into_safe_size(lang: str, text: str, safe_size: int, summary_model_config: LLMConfig) \
        -> tuple[Optional[str], Optional[int]]:
    """Compress the text to a safe size
    压缩文本至安全尺寸

    First, the long text is sliced, and then a summary is generated for each slice.
    首先将长文本切片，然后逐切片的生成摘要。

    the summary will be further compressed, with the compressed size expected to stay within the range of the safe_size.
    压缩后的大小被期望保持在 safe_size 范围之内。

    :param text: Text to be compressed.
        待压缩的文本。
    :param safe_size: The target size of the text after compression.
        文本压缩后的目标尺寸。
    :param summary_model_config: LLM configuration used for text compression.
        用于压缩文本的 LLM 配置。


    :return:
        --compressed_text: The text after compression.
            压缩后的文本。
        --total_tokens: Total tokens after compression.
            压缩后的整体tokens。
    """

    compressed_text = ""
    total_tokens = 0

    split_texts = split_text(text, summary_model_config.request_config.max_messages_tokens, summary_model_config.model)

    # Calculate the approximate size of the text slices proportionally
    split_safe_size = int(safe_size / len(split_texts))

    for st in split_texts:
        content, tokens = generate_text_summary(lang, st, summary_model_config, split_safe_size)

        if content:
            compressed_text += content + "\n"
            total_tokens += tokens

    if compressed_text:
        return compressed_text, total_tokens
    else:
        return None, None


def generate_text_summary(lang: str, text: str, summary_model_config: LLMConfig, safe_size: Optional[int] = None) \
        -> tuple[str, int]:
    """Generate a general summary of the text
    生成文本普通摘要

    :param text: Text to be compressed.
        待压缩的文本。
    :param summary_model_config: LLM configuration used for text compression.
        用于压缩文本的 LLM 配置。
    :param safe_size: The target size of the text after compression, if not provided there is no limit.
        文本压缩后的目标尺寸，如果为空则不做限制。

    :return:
        --compressed_text: The text after compression.
            压缩后的文本。
        --total_tokens: Total tokens after compression.
            压缩后的整体tokens。
    """
    compressed_text_prompts = CompressedTextPrompts(lang)
    system_prompt, chat_prompt = compressed_text_prompts.summary(text, safe_size)

    chat_messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': chat_prompt}]
    request_data = ChatCompletionsRequest(chat_messages, False)
    return generate_chat_completion_internal(summary_model_config, request_data)


def generate_text_clues(lang: str, text: str, focus: str, summary_model_config: LLMConfig) -> tuple[str, int]:
    """Generate a clue summary of the text
    生成文本线索摘要

    :param text: Text to be compressed.
        待压缩的文本。
    :param focus: The focus direction when compressing text.
        压缩文本时的专注方向。
    :param summary_model_config: LLM configuration used for text compression.
        用于压缩文本的 LLM 配置。

    :return:
        --compressed_text: The text after compression.
            压缩后的文本。
        --total_tokens: Total tokens after compression.
            压缩后的整体tokens。
    """
    compressed_text_prompts = CompressedTextPrompts(lang)
    system_prompt, chat_prompt = compressed_text_prompts.clue(text, focus)

    chat_messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user',
                                                                    'content': chat_prompt}]

    request_data = ChatCompletionsRequest(chat_messages, False)
    return generate_chat_completion_internal(summary_model_config, request_data)


def split_text(text: str, split_size: int, model: Optional[str] = None) -> List[str]:
    """Split the long text and store the text slices in a list
    将长文本拆分，并将文本切片存储至列表
    """

    split_texts = []

    count_tokens = count_text_tokens(text, model)

    # Calculate the approximate size of the text slices proportionally
    max_size = len(text) / (math.ceil(count_tokens / split_size) + 1)

    parts = split_paragraphs(text)

    current_size = 0
    current_text = ''
    for part in parts:
        part_size = len(part)
        if part_size > max_size:
            sentences = split_paragraph_into_sentences(part)
            for sentence in sentences:
                sentence_size = len(sentence)
                if current_size + sentence_size > max_size:
                    if current_text:
                        split_texts.append(current_text.strip())
                    current_size = 0
                    current_text = ''
                current_size += sentence_size
                current_text += sentence + ' '
        else:
            if current_size + part_size > max_size:
                if current_text:
                    split_texts.append(current_text.strip())
                current_size = 0
                current_text = ''
            current_size += part_size
            current_text += part + ' '

    if current_text:
        split_texts.append(current_text.strip())
    return split_texts


def split_paragraphs(text) -> List[str]:
    """Split the text into paragraphs and code blocks
    将文本按段落和代码块拆分
    """

    pattern = re.compile(
        r'(```.*?```)|([^`]\S.*\n?)',  # matches either a code block or a non-empty line
        re.DOTALL | re.MULTILINE
    )

    parts = pattern.findall(text)
    # The result is a list of tuples, where each tuple contains the matched code block and the matched line of text.
    # We use a list comprehension to combine these into a single list.
    # We also add a replace method to remove any single backticks that might have been included in the text lines.
    parts = [(code or text).strip("`") for code, text in parts]

    return parts


def split_paragraph_into_sentences(paragraph) -> List[str]:
    """Split the paragraphs into sentences
    将段落拆分成句子
    """
    sentence_ends = re.compile(r'[。？！]')
    sentences = sentence_ends.split(paragraph)
    sentences = [s for s in sentences if len(s) > 0]
    return sentences

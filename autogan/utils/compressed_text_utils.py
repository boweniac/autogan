import math
import re
from typing import Optional, List
from autogan.oai.config_utils import LLMConfig
from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.utils.environment_utils import environment_info
from autogan.oai.generate_utils import generate_chat_completion
from autogan.utils.response import ResponseFuncType


def compressed_text_universal(text: str, summary_model_config: LLMConfig, agent_name: str,
                              response_func: ResponseFuncType, stream_mode: Optional[bool] = None,
                              focus: Optional[str] = None, safe_size: Optional[int] = None) \
        -> tuple[Optional[str], Optional[int]]:
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
    :param agent_name:
    :param response_func: Used to return results to the interface or terminal.
        用于向接口或终端返回结果
    :param stream_mode:
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

    split_texts = split_text(text, summary_model_config.max_messages_tokens, summary_model_config.model)

    for st in split_texts:
        if focus:
            content, tokens = generate_text_clues(st, focus, summary_model_config, agent_name, response_func,
                                                  stream_mode)
        else:
            content, tokens = generate_text_summary(st, summary_model_config, agent_name, response_func, stream_mode)

        if content:
            compressed_text += content + "\n"
            total_tokens += tokens

    if compressed_text:
        if safe_size and safe_size < total_tokens:
            return compressed_text_into_safe_size(compressed_text, safe_size, summary_model_config, agent_name,
                                                  response_func, stream_mode)
        else:
            return compressed_text, total_tokens
    else:
        return None, None


def compressed_text_into_safe_size(text: str, safe_size: int, summary_model_config: LLMConfig, agent_name: str,
                                   response_func: ResponseFuncType, stream_mode: Optional[bool] = None) \
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
    :param agent_name:
    :param response_func: Used to return results to the interface or terminal.
        用于向接口或终端返回结果
    :param stream_mode:


    :return:
        --compressed_text: The text after compression.
            压缩后的文本。
        --total_tokens: Total tokens after compression.
            压缩后的整体tokens。
    """

    compressed_text = ""
    total_tokens = 0

    split_texts = split_text(text, summary_model_config.max_messages_tokens, summary_model_config.model)

    # Calculate the approximate size of the text slices proportionally
    split_safe_size = int(safe_size / len(split_texts))

    for st in split_texts:
        content, tokens = generate_text_summary(st, summary_model_config, agent_name, response_func, stream_mode,
                                                split_safe_size)

        if content:
            compressed_text += content + "\n"
            total_tokens += tokens

    if compressed_text:
        return compressed_text, total_tokens
    else:
        return None, None


def generate_text_summary(text: str, summary_model_config: LLMConfig, agent_name: str, response_func: ResponseFuncType,
                          stream_mode: Optional[bool] = None, safe_size: Optional[int] = None) \
        -> tuple[str, int]:
    """Generate a general summary of the text
    生成文本普通摘要

    :param text: Text to be compressed.
        待压缩的文本。
    :param summary_model_config: LLM configuration used for text compression.
        用于压缩文本的 LLM 配置。
    :param agent_name:
    :param response_func: Used to return results to the interface or terminal.
        用于向接口或终端返回结果
    :param stream_mode:
    :param safe_size: The target size of the text after compression, if not provided there is no limit.
        文本压缩后的目标尺寸，如果为空则不做限制。

    :return:
        --compressed_text: The text after compression.
            压缩后的文本。
        --total_tokens: Total tokens after compression.
            压缩后的整体tokens。
    """

    if safe_size:
        system_prompt = """I hope you are an article filter and refiner, filtering and refining the articles sent by users. Please ensure that your summary does not exceed the limit of max_tokens.
When the content of the article is not enough to refine, please omit other polite language and only output one word: None.
If the article can be refined, please help me filter out sensitive content related to politics, geopolitics, violence, and sex from the article, and extract the main content from the article.
Please note that the description perspective and chapter structure of the extracted content should be as consistent as possible with the original text, and try to retain details for subsequent reasoning. Please omit other polite language and only output the refined content."""
        chat_prompt = f"max_tokens: {safe_size}\n\nArticle content:\n{text}"
    #        system_prompt = """我希望你是一个文章过滤与提炼器，过滤和提炼用户发送的文章，请确保您的总结不超过 max_tokens 的限制.
    # 当文章内容不足以提炼时，请省略其他客套用语，仅输出一个单词：None。
    # 如果文章可以精炼请帮我滤掉文章中与政治、地缘政治、暴力、性等有关的敏感内容,并从文章中提炼出主要内容.
    # 注意提炼出的内容其描述视角和章节结构尽量与原文一致，并尽可能的保留细节以用于后续推理，请省略其他客套用语，仅输出提炼好的内容。"""
    #        chat_prompt = f"max_tokens: {safe_size}\n\n文章内容：\n\n{text}"
    else:
        system_prompt = """I hope you can serve as an article filter and refiner, filtering and refining the articles sent by users. If the content of the article is insufficient for refinement, please omit other polite phrases and output only one word: None.
If the article can be refined, please help me filter out sensitive content related to politics, geopolitics, violence, and sex from the article, and extract the main content from the article.
Please note that the perspective and chapter structure of the extracted content should be as consistent with the original as possible, and retain as many details as possible for subsequent reasoning. Please omit other polite phrases and only output the refined content."""
        chat_prompt = f"Article content:\n{text}"
        # system_prompt = """我希望你是一个文章过滤与提炼器，过滤和提炼用户发送的文章。当文章内容不足以提炼时，请省略其他客套用语，仅输出一个单词：None。
        #                  如果文章可以精炼请帮我滤掉文章中与政治、地缘政治、暴力、性等有关的敏感内容，并从文章中提炼出主要内容。
        #                  注意提炼出的内容其描述视角和章节结构尽量与原文一致，并尽可能的保留细节以用于后续推理。请省略其他客套用语，仅输出提炼好的内容。"""
        # chat_prompt = f"文章内容：\n{text}"

    chat_messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': chat_prompt}]

    return generate_chat_completion(summary_model_config, chat_messages, agent_name, "text_summary", response_func,
                                    stream_mode)


def generate_text_clues(text: str, focus: str, summary_model_config: LLMConfig, agent_name: str,
                        response_func: ResponseFuncType, stream_mode: Optional[bool] = None) -> tuple[str, int]:
    """Generate a clue summary of the text
    生成文本线索摘要

    :param text: Text to be compressed.
        待压缩的文本。
    :param focus: The focus direction when compressing text.
        压缩文本时的专注方向。
    :param summary_model_config: LLM configuration used for text compression.
        用于压缩文本的 LLM 配置。
    :param agent_name:
    :param response_func: Used to return results to the interface or terminal.
        用于向接口或终端返回结果
    :param stream_mode:

    :return:
        --compressed_text: The text after compression.
            压缩后的文本。
        --total_tokens: Total tokens after compression.
            压缩后的整体tokens。
    """

    info = environment_info()
    system_prompt = """I hope you are an agent who is good at discovering the truth in real-time, capable of finding content that helps infer the answer to the question from the information sent by users. 
Please note that if the content of the information has no extractable value, please omit other polite expressions and output only one word: None. Also, please help me filter out sensitive content related to politics, geopolitics, violence, and sex in the information."""
    # system_prompt = """我希望你是一个善于发现实时真相的探员, 能从用户发送的资料中帮我找到有助于推断出问题答案的内容。
    #                     需要注意的是，如果资料内容没有可提取的价值，请省略其他客套用语，仅输出一个单词：None。另外还请帮我过滤掉资料中与政治、地缘政治、暴力、性等有关的敏感内容。"""
    chat_messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user',
                                                                    'content': f'The current question is:{focus}\n\nEnvironmental information:\n{info}\n\nMaterial content:\n\n{text}'}]
    # chat_messages = [{'role': 'user', 'content': f'当前的问题是：{focus}\n\n环境信息：\n{info}\n\n资料内容：\n\n{text}'}]

    return generate_chat_completion(summary_model_config, chat_messages, agent_name, "clue_summary", response_func,
                                    stream_mode)


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

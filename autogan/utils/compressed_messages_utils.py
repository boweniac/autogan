import json
from typing import Dict, Optional, List

from autogan.oai.chat_api_utils import ChatCompletionsRequest
from autogan.oai.chat_generate_utils import generate_chat_completion_internal
from autogan.oai.chat_config_utils import LLMConfig


def compressed_messages(messages: List[Dict], focus: str, summary_model_config: LLMConfig,
                        safe_size: Optional[int] = 4096) -> tuple[Optional[list], Optional[list], Optional[int]]:
    """Compress Conversation Context
    压缩会话上下文

    The content to be compressed is divided into: recent original conversation content, and distant content that needs to be compressed.
    待压缩的会话内容会被分为：近期的原始会话内容、远期需要压缩的会话内容。

    When compressing distant conversation records, attention is focused on the 'focus'
    在压缩远期会话记录时，会将注意力集中于 focus

    **Recent Original Conversation Content:**
    近期原始会话内容:

    First, traverse the 'messages' in reverse order, extract the recent conversation records, until the cumulative tokens of the conversation records exceed 50% of the 'safe_size'
    先反向遍历 messages，提取近期的会话记录，直至会话记录的累计 tokens 超过 safe_size 的 50%

    If the tokens of the first recent conversation record exceed 50% of the 'safe_size', then directly extract the first recent conversation record
    如近期第一条会话记录的 tokens 就超过了 safe_size 的 50% 则直接提取近期第一条会话记录

    **Distant Compressed Conversation Content:**
    远期压缩会话内容:

    The remaining conversation records will be compressed as distant conversation records. The size after compression is expected to be within the range of ('safe_size' - cumulative original conversation tokens)
    剩余的会话记录将作为远期会话记录进行压缩，压缩后的大小被期望保持在 (safe_size - 累计原始会话 tokens) 范围之内

    If the value of 'safe_size' - cumulative original conversation tokens is less than 0, then the size after compression is expected to be 1024 tokens
    如 safe_size - 累计原始会话 tokens 的值小于 0 则压缩后的大小被期望保持在 1024 tokens

    Note: The compression process does not treat messages from the 'system' role specially, and they should be excluded from 'messages'.
    注意：压缩过程并未对 system 角色的消息进行特殊处理，应将其排除在 messages 之外。

    :param messages: The conversation content to be compressed, excluding 'system message' and 'focus message'. It should include 'role', 'content', 'tokens' fields.
        待压缩的会话内容，应排除掉 system message 和 focus message。需包含 'role'，'content'，'tokens' 字段。
    :param focus: The focus direction when compressing distant conversation records
        压缩远期会话记录时的专注方向
    :param summary_model_config: The LLM model configuration used to compress distant conversation records
        用于压缩远期会话记录的 LLM 模型配置
    :param safe_size: 'max_messages_tokens' of 'agent main model' minus the tokens of 'system message' and 'focus message'. When 'safe_size' is less than 0, it will be forcibly defined as 1024
        agent main model 的 max_messages_tokens 减去 system message 和 focus message 的 tokens，当 safe_size 小于 0 时，将被强制定义为 1024

    :return:
        --conversation_messages: The compressed conversation records, the difference from 'request_messages' is that the 'tokens' field of each message is retained
            压缩后的会话记录，与 request_messages 的区别是保留了每条消息的 tokens 字段
        --request_messages: The message content requested to 'llm', removed the 'tokens' field of each message
            用于向 llm 请求的消息内容，去掉了每条消息的 tokens 字段
        --total_tokens: The total tokens after compression
            压缩后的整体tokens
    """
    conversation_messages = []
    request_messages = []
    total_tokens = 0

    if len(messages) == 0:
        return None, None, None

    if safe_size < 0:
        safe_size = 1024
    # Reverse traverse the message to extract recent original conversation content.
    i = 0
    for message in reversed(messages):
        tokens = message["tokens"]
        if total_tokens + tokens > int(safe_size * 0.5) and i != 0:
            break
        message_copy = message.copy()
        message_copy.pop('tokens', None)
        conversation_messages.insert(0, message)
        request_messages.insert(0, message_copy)
        total_tokens += tokens
        i -= 1
    # Compress the remaining messages as distant conversation records.
    if len(messages) > (i * -1):
        compressed_size = safe_size - total_tokens
        if compressed_size <= 0:
            compressed_size = 1024

        # 压缩剩余 messages
        content, tokens = generate_messages_summary(messages[:i], focus, summary_model_config, compressed_size)

        if content:
            conversation_messages.insert(
                0,
                {'role': 'assistant', 'content': f'Earlier historical conversation records: {content}',
                 'tokens': tokens}
            )
            request_messages.insert(
                0,
                {'role': 'assistant', 'content': f'Earlier historical conversation records: {content}'}
            )
            total_tokens += tokens
    if conversation_messages and request_messages:
        return conversation_messages, request_messages, total_tokens
    else:
        return None, None, None


def generate_messages_summary(messages: List[Dict], focus: str, summary_model_config: LLMConfig,
                              summary_size: int) -> tuple[str, int]:
    """Generate message summary
    生成消息摘要

    First, traverse the content of messages in reverse order, extract the long-term conversation records to be compressed, until the cumulative tokens of the long-term conversation records to be compressed exceed the value of max_messages_tokens in summary_model_config
    先反向遍历 messages 中的内容，提取出待压缩的远期会话记录，直至待压缩远期会话记录的累计 tokens 超过 summary_model_config 中 max_messages_tokens 的值

    If the tokens of the first record of the long-term conversation to be compressed exceed max_messages_tokens, then directly extract the first conversation record
    如待压缩远期会话的第一条记录，其 tokens 就超过了 max_messages_tokens， 则直接提取第一条会话记录

    Then compress the extracted long-term conversation records. The size after compression is expected to be kept within the range of summary_size
    之后对提取出的远期会话记录进行压缩，压缩后的大小被期望保持在 summary_size 范围之内

    :param messages: Messages to be compressed
        待压缩的消息
    :param focus: The focus direction when generating a summary
        生成摘要时的专注方向
    :param summary_model_config: The LLM model configuration for compressing long-term conversation records
        用于压缩远期会话记录的 LLM 模型配置
    :param summary_size:

    :return:
        --content: Compressed content
            压缩后的内容
        --tokens: tokens of compressed content
            压缩内容的tokens
    """
    system_prompt = """# role
You are a professional conference secretary, skilled in summarizing conference content.

## Skills
### Skills 1: Targeted Summary
Each meeting has a core topic. When summarizing the content, attention should be focused on the core topic.

### Skills 2: Content Compression
Each meeting summary has a word limit. The summarized content needs to be compressed to within max_tokens.

## Constraints
- This is a serious professional meeting, please only output the summarized conference content.
- Do not greet or interact with others, for example, do not reply: hello, I understand, etc."""
    # system_prompt = "请根据以下的历史信息，进行简洁的总结。请确保您的总结不超过 max_tokens 的限制。并且在总结时，请将你的关注点集中在用户最新发送的消息上。"

    summary_messages = []
    total_tokens = 0
    # 反向遍历 message 提取内容
    for index, message in enumerate(reversed(messages)):
        tokens = message["tokens"]
        if total_tokens + tokens > summary_model_config.request_config.max_messages_tokens and index != 0:
            break
        message_copy = message.copy()
        message_copy.pop('tokens', None)
        summary_messages.insert(0, message_copy)
        total_tokens += tokens
    # 设置用户提示词
    user_prompt = f"""The following are the conference-related content and requirements, please help me to summarize.
    
# core topic
{focus}

# max_tokens
{summary_size}

# conference content
{json.dumps(summary_messages)}"""

    chat_messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_prompt}]
    request_data = ChatCompletionsRequest(chat_messages, False)
    return generate_chat_completion_internal(summary_model_config, request_data)

from typing import Protocol, Optional


class ResponseProtocol(Protocol):
    req_msg_id: Optional[int]
    conv_turns: Optional[int]

    def send(self, msg_id: int, task_id: int, requester_name: str, index: int, content_type: str, content: str, completion_tokens: int, response: any):
        """default response function
        默认响应函数提供终端打印支持
        The default response function provides terminal printing support.

        :param agent_name:
        :param gen: Used to distinguish agent replies, deep thoughts, context compression, general summaries, clue summaries
            用于区分 agent 回复、深思、压缩上下文、普通摘要、线索摘要
            - main: agent replies
            - idea: deep thoughts
            - messages_summary: context compression
            - text_summary: general summaries
            - clue_summary: clue summaries
            - system:
            - tool:
            - tool_call:
        :param model:
        :param stream_mode:
        :param index: response sequence
        :param content: completion content
            生成内容
        :param tokens: completion tokens
            生成内容的 tokens
        :param response: Respond to raw data
            响应原始数据
        :return:
        """
        pass

    async def a_send(self, msg_id: int, task_id: int, requester_name: str, index: int, content_type: str, content: str, completion_tokens: int, response: any):
        """default response function
        默认响应函数提供终端打印支持
        The default response function provides terminal printing support.

        :param msg_id:
        :param agent_name:
        :param gen: Used to distinguish agent replies, deep thoughts, context compression, general summaries, clue summaries
            用于区分 agent 回复、深思、压缩上下文、普通摘要、线索摘要
            - main: agent replies
            - idea: deep thoughts
            - messages_summary: context compression
            - text_summary: general summaries
            - clue_summary: clue summaries
            - system:
            - tool:
            - tool_call:
        :param model:
        :param stream_mode:
        :param index: response sequence
        :param content: completion content
            生成内容
        :param tokens: completion tokens
            生成内容的 tokens
        :param response: Respond to raw data
            响应原始数据
        :return:
        """
        pass

    def need_to_stop(self):
        pass

import asyncio
from queue import Queue
from threading import Condition
from threading import Event

from google.protobuf import message as _message
from typing import Optional
from fastapi import Request
from autogan.protocol.response_protocol import ResponseProtocol

try:
    from termcolor import colored
except ImportError:
    def colored(x, *args, **kwargs):
        return x


class GrpcResponse(ResponseProtocol):
    def __init__(
            self,
            reply: Queue,
            stop_event: Event
    ):
        self.conv_turns: int = 0
        self.req_msg_id: Optional[int] = None
        self._reply = reply
        self._stop_event = stop_event

    def send(self, agent_name: str, gen: str, model: str, stream_mode: bool, index: int,
                     content: Optional[str], tokens: Optional[int], response: any, msg_id: Optional[int], task_id: Optional[int]):
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
        # await asyncio.sleep(0)
        print(content)
        text = ""
        # if content:
        #     if gen == "main":
        #         if index == 1:
        #             text += f"{agent_name}: "
        #         text += content
        #     elif gen == "user":
        #         if index == 1:
        #             text += f"{agent_name}: "
        #         text += content
        #     elif gen == "idea" or gen == "tool_call":
        #         if index == 1:
        #             text += f"{agent_name}: "
        #         text += content
        #     elif gen == "system":
        #         text += f"{agent_name}: {content}"
        #     elif gen == "tool":
        #         text += f"{agent_name}: {content}"
        #     elif gen == "search":
        #         text += f"url: {content}"
        text = f'data: {{"agent_name": "{agent_name}", "role": "{gen}", "content": "{content}", "tokens": "{tokens}", "msg_id": "{msg_id}", "task_id": "{task_id}"}}\n\n'

        self._reply.put(text)

    def need_to_stop(self):
        return self._stop_event.is_set()


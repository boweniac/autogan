import asyncio
from typing import Optional
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from autogan.protocol.response_protocol import ResponseProtocol

try:
    from termcolor import colored
except ImportError:
    def colored(x, *args, **kwargs):
        return x


class WebsocketResponse(ResponseProtocol):
    def __init__(
            self,
            websocket: WebSocket,
    ):
        self.conv_turns: int = 0
        self.req_msg_id: Optional[int] = None
        self._websocket = websocket
        self.disconnected = False

    async def a_send(self, agent_name: str, gen: str, model: str, stream_mode: bool, index: int,
                     content: Optional[str], tokens: Optional[int], response: any, msg_id: Optional[int],
                     task_id: Optional[int]):
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
        if stream_mode:
            end = ""
        else:
            end = "\n"
        print(content)
        if content:
            try:
                if gen == "main":
                    if index == 1:
                        await self._websocket.send_text(f"\n{agent_name}: ")
                    await self._websocket.send_text(content)
                elif gen == "idea" or gen == "tool_call":
                    if index == 1:
                        await self._websocket.send_text(f"\n{agent_name}: ")
                    await self._websocket.send_text(content)
                elif gen == "system":
                    await self._websocket.send_text(f"\n{agent_name}: {content}")
                elif gen == "tool":
                    await self._websocket.send_text(f"\n{agent_name}: {content}")
                elif gen == "search":
                    await self._websocket.send_text(f"\nurl: {content}")
            except WebSocketDisconnect:
                self.disconnected = True

    def need_to_stop(self):
        return self.disconnected

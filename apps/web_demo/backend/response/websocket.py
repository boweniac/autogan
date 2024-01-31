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

    async def a_send(self, msg_id: int, task_id: int, requester_name: str, index: int, content_type: str, content_tag: str,
                     content: str, completion_tokens: int, response: any):
        """default response function
        默认响应函数提供终端打印支持
        The default response function provides terminal printing support.

        :param msg_id:
        :param task_id:
        :param requester_name:
        :param index: response sequence
        :param content_type:
        :param content: completion content
        :param completion_tokens: completion tokens
        :param response: Respond to raw data
        :return:
        """
        print(content)
        if content:
            try:
                if content_type == "main":
                    if index == 1:
                        await self._websocket.send_text(f"\n{requester_name}: ")
                    await self._websocket.send_text(content)
                elif content_type == "idea" or content_type == "tool_call":
                    if index == 1:
                        await self._websocket.send_text(f"\n{requester_name}: ")
                    await self._websocket.send_text(content)
                elif content_type == "system":
                    await self._websocket.send_text(f"\n{requester_name}: {content}")
                elif content_type == "tool":
                    await self._websocket.send_text(f"\n{requester_name}: {content}")
                elif content_type == "search":
                    await self._websocket.send_text(f"\nurl: {content}")
            except WebSocketDisconnect:
                self.disconnected = True

    def need_to_stop(self):
        return self.disconnected

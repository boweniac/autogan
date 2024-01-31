import asyncio
from asyncio import Queue
from typing import Optional

from autogan.protocol.response_protocol import ResponseProtocol

try:
    from termcolor import colored
except ImportError:
    def colored(x, *args, **kwargs):
        return x


class StreamResponse(ResponseProtocol):
    def __init__(
            self,
            data_queue: Queue
    ):
        self.conv_turns: int = 0
        self.req_msg_id: Optional[int] = None
        self._data_queue = data_queue
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
        await asyncio.sleep(0)
        text = ""
        if content:
            if content_type == "main":
                if index == 1:
                    text += f"{requester_name}: "
                text += content
            elif content_type == "idea" or content_type == "tool_call":
                if index == 1:
                    text += f"{requester_name}: "
                text += content
            elif content_type == "system":
                text += f"{requester_name}: {content}"
            elif content_type == "tool":
                text += f"{requester_name}: {content}"
            elif content_type == "search":
                text += f"url: {content}"
        text = 'data: {"text":"' + text + '"}\n\n'
        await self._data_queue.put(text)

    async def a_receive(self):
        while True:
            if not self._data_queue.empty():
                data = await self._data_queue.get()
                print(data)
                yield data
            else:
                await asyncio.sleep(0.1)  # 简短休眠以避免 CPU 过载

    def need_to_stop(self):
        return self.disconnected

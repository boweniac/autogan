import json
from queue import Queue
from threading import Event
from typing import Optional

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

    def send(self, msg_id: int, task_id: int, requester_name: str, index: int, content_type: str, content_tag: str,
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
        data = {
            "agent_name": requester_name,
            "content_type": content_type,
            "content_tag": content_tag,
            "content": content,
            "tokens": completion_tokens,
            "msg_id": msg_id,
            "task_id": task_id,
            "index": index
        }
        text = f'data: {json.dumps(data, ensure_ascii=False)}\n\n'

        self._reply.put(text)

    def need_to_stop(self):
        return self._stop_event.is_set()

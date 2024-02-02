import re
from typing import Optional
from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.protocol.response_protocol import ResponseProtocol
from autogan.utils.uuid_utils import SnowflakeIdGenerator


class ConvHolder:
    def __init__(
            self,
            conversation_id: int,
            task_id: int,
            response_proxy: ResponseProtocol,
            snowflake_id_generator: SnowflakeIdGenerator
    ):
        self.conversation_id = conversation_id
        self.task_id = task_id
        self.response_proxy = response_proxy
        self.snowflake_id_generator = snowflake_id_generator
        self.msg_id: Optional[int] = None
        self.requester_name: Optional[str] = None
        self.requester_type: Optional[str] = None
        self.content: Optional[str] = None
        self.completion_tokens: Optional[int] = None
        self.responder_name: Optional[str] = None

    def init_message(self, requester_name: str, requester_type: str):
        self.msg_id = self.snowflake_id_generator.next_id()
        self.requester_name = requester_name
        self.requester_type = requester_type
        self.content = None
        self.completion_tokens = None
        self.responder_name = None

    def update_message(self, content: str):
        self.content = content
        self.completion_tokens = count_text_tokens(content)
        match = re.findall(r'@(\w+)', content)
        if match:
            self.responder_name = match[0]
        else:
            self.responder_name = None

    def switch_to_agent(self, task_id: str, content: str):
        self.task_id = task_id
        if self.content != content:
            self.content = content
            self.completion_tokens = count_text_tokens(content)
            match = re.findall(r'@(\w+)', content)
            if match:
                self.responder_name = match[0]
            else:
                self.responder_name = None

    def to_system_alert(self, content: str):
        self.msg_id = self.snowflake_id_generator.next_id()
        self.requester_name = "system"
        self.requester_type = None
        self.content = content
        self.completion_tokens = count_text_tokens(content)

        match = re.findall(r'@(\w+)', content)
        if match:
            self.responder_name = match[0]
        else:
            self.responder_name = None

    def message(self, content_type: str, content_tag: Optional[str] = None):
        data = {
            "msg_id": self.msg_id,
            "task_id": self.task_id,
            "content_type": content_type,
            "content_tag": content_tag if content_tag else "",
            "agent_name": self.requester_name,
            "content": self.content,
            "tokens": self.completion_tokens
        }
        return data

    def response(self, index: int, content_type: str, content_tag: str, content: str, completion_tokens: int,
                 response: any):
        self.response_proxy.send(self.msg_id, self.task_id, self.requester_name, index, content_type, content_tag,
                                 content,
                                 completion_tokens, response)

    async def a_response(self, index: int, content_type: str, content_tag: str, content: str, completion_tokens: int,
                         response: any):
        await self.response_proxy.a_send(self.msg_id, self.task_id, self.requester_name, index, content_type,
                                         content_tag, content,
                                         completion_tokens, response)

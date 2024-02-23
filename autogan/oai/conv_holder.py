import re
from typing import Optional
from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.protocol.response_protocol import ResponseProtocol
from autogan.utils.uuid_utils import SnowflakeIdGenerator


class DialogueManager:
    def __init__(
            self,
            conversation_id: int,
            response_proxy: ResponseProtocol,
            snowflake_id_generator: SnowflakeIdGenerator
    ):
        """在 agent 交流的过程中，管理每轮对话的消息内容，以及实时向客户端返回对话内容"""
        self.conversation_id = conversation_id
        self.task_id = conversation_id
        self.pre_task_id: Optional[int] = None
        self.response_proxy = response_proxy
        self.snowflake_id_generator = snowflake_id_generator
        self.msg_id: Optional[int] = None
        self.sender_name: Optional[str] = None
        self.sender_type: Optional[str] = None
        self.content: Optional[str] = None
        self.completion_tokens: Optional[int] = None
        self.receiver_name: Optional[str] = None

    def init_message_before_generate(self, sender_name: str, sender_type: str):
        """每次在生成、发送、存储消息之前，初始化消息"""
        self.msg_id = self.snowflake_id_generator.next_id()
        self.sender_name = sender_name
        self.sender_type = sender_type
        self.content = None
        self.completion_tokens = None
        self.receiver_name = None

    def before_switch(self, content: str, tokens: int):
        """发送至交换机前，设置最终要发送的消息内容"""
        self.content = content
        self.completion_tokens = tokens
        match = re.findall(r'@(\w+)', content)
        if match:
            self.receiver_name = match[0]
        else:
            self.receiver_name = None

    def after_switch(self, task_id: str, content: str):
        """消息离开交换机前，调整任务 id 和消息内容"""
        self.pre_task_id = self.task_id
        self.task_id = task_id
        if self.content != content:
            self.content = content
            self.completion_tokens = count_text_tokens(content)
            match = re.findall(r'@(\w+)', content)
            if match:
                self.receiver_name = match[0]
            else:
                self.receiver_name = None

    def init_message_before_alert(self, content: str):
        self.msg_id = self.snowflake_id_generator.next_id()
        self.sender_name = "system"
        self.sender_type = None
        self.content = content
        self.completion_tokens = count_text_tokens(content)
        match = re.findall(r'@(\w+)', content)
        if match:
            self.receiver_name = match[0]
        else:
            self.receiver_name = None

    @property
    def compressed_message(self):
        data = {
            'role': 'user' if self.sender_type == "HUMAN" else "assistant",
            'content': self.content,
            'name': self.sender_name,
            'tokens': self.completion_tokens
        }
        return data

    def message(self, content_type: str, content_tag: Optional[str] = None):
        data = {
            "msg_id": self.msg_id,
            "task_id": self.task_id,
            "content_type": content_type,
            "content_tag": content_tag if content_tag else "",
            "agent_name": self.sender_name,
            "agent_type": self.sender_type,
            "content": self.content,
            "tokens": self.completion_tokens
        }
        return data

    def response(self, index: int, content_type: str, content_tag: str, content: str, completion_tokens: int,
                 response: any):
        self.response_proxy.send(self.msg_id, self.task_id, self.sender_name, index, content_type, content_tag,
                                 content,
                                 completion_tokens, response)

    async def a_response(self, index: int, content_type: str, content_tag: str, content: str, completion_tokens: int,
                         response: any):
        await self.response_proxy.a_send(self.msg_id, self.task_id, self.sender_name, index, content_type,
                                         content_tag, content,
                                         completion_tokens, response)

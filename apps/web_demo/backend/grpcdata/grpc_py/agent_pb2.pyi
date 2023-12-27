from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReceiveRequest(_message.Message):
    __slots__ = ("user_id", "conversation_id", "content")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    conversation_id: int
    content: str
    def __init__(self, user_id: _Optional[int] = ..., conversation_id: _Optional[int] = ..., content: _Optional[str] = ...) -> None: ...

class ReceiveReply(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AgentRequest(_message.Message):
    __slots__ = ("user_id", "conversation_id", "content")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    conversation_id: int
    content: str
    def __init__(self, user_id: _Optional[int] = ..., conversation_id: _Optional[int] = ..., content: _Optional[str] = ...) -> None: ...

class AgentResponse(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class AudioAndLipRequest(_message.Message):
    __slots__ = ("text", "voice", "speed")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VOICE_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    text: str
    voice: str
    speed: int
    def __init__(self, text: _Optional[str] = ..., voice: _Optional[str] = ..., speed: _Optional[int] = ...) -> None: ...

class AudioAndLipResponse(_message.Message):
    __slots__ = ("audio_file", "lips_data")
    AUDIO_FILE_FIELD_NUMBER: _ClassVar[int]
    LIPS_DATA_FIELD_NUMBER: _ClassVar[int]
    audio_file: str
    lips_data: str
    def __init__(self, audio_file: _Optional[str] = ..., lips_data: _Optional[str] = ...) -> None: ...

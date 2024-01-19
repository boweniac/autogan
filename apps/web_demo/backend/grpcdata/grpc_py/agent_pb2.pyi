from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

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
    __slots__ = ("text", "model", "voice", "speed")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    VOICE_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    text: str
    model: str
    voice: str
    speed: float
    def __init__(self, text: _Optional[str] = ..., model: _Optional[str] = ..., voice: _Optional[str] = ..., speed: _Optional[float] = ...) -> None: ...

class AudioAndLipResponse(_message.Message):
    __slots__ = ("audio_file", "lips_data")
    AUDIO_FILE_FIELD_NUMBER: _ClassVar[int]
    LIPS_DATA_FIELD_NUMBER: _ClassVar[int]
    audio_file: str
    lips_data: str
    def __init__(self, audio_file: _Optional[str] = ..., lips_data: _Optional[str] = ...) -> None: ...

class AddConversationRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class AddConversationResponse(_message.Message):
    __slots__ = ("conversation_id",)
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    def __init__(self, conversation_id: _Optional[str] = ...) -> None: ...

class UpdateConversationTitleRequest(_message.Message):
    __slots__ = ("user_id", "conversation_id", "title")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    conversation_id: str
    title: str
    def __init__(self, user_id: _Optional[str] = ..., conversation_id: _Optional[str] = ..., title: _Optional[str] = ...) -> None: ...

class UpdateConversationTitleResponse(_message.Message):
    __slots__ = ("is_success",)
    IS_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    is_success: bool
    def __init__(self, is_success: bool = ...) -> None: ...

class GetConversationsRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class GetConversationsResponse(_message.Message):
    __slots__ = ("conversations",)
    CONVERSATIONS_FIELD_NUMBER: _ClassVar[int]
    conversations: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, conversations: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteConversationRequest(_message.Message):
    __slots__ = ("user_id", "conversation_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    conversation_id: str
    def __init__(self, user_id: _Optional[str] = ..., conversation_id: _Optional[str] = ...) -> None: ...

class DeleteConversationResponse(_message.Message):
    __slots__ = ("is_success",)
    IS_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    is_success: bool
    def __init__(self, is_success: bool = ...) -> None: ...

class GetLastMsgIdRequest(_message.Message):
    __slots__ = ("user_id", "conversation_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    conversation_id: str
    def __init__(self, user_id: _Optional[str] = ..., conversation_id: _Optional[str] = ...) -> None: ...

class GetLastMsgIdResponse(_message.Message):
    __slots__ = ("msg_id",)
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    msg_id: str
    def __init__(self, msg_id: _Optional[str] = ...) -> None: ...

class GetMessagesRequest(_message.Message):
    __slots__ = ("user_id", "conversation_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    conversation_id: str
    def __init__(self, user_id: _Optional[str] = ..., conversation_id: _Optional[str] = ...) -> None: ...

class GetMessagesResponse(_message.Message):
    __slots__ = ("messages",)
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, messages: _Optional[_Iterable[str]] = ...) -> None: ...

class AliyunStsRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class AliyunStsResponse(_message.Message):
    __slots__ = ("access_key_id", "access_key_secret", "expiration", "security_token")
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_SECRET_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    SECURITY_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_key_id: str
    access_key_secret: str
    expiration: str
    security_token: str
    def __init__(self, access_key_id: _Optional[str] = ..., access_key_secret: _Optional[str] = ..., expiration: _Optional[str] = ..., security_token: _Optional[str] = ...) -> None: ...

class AudioToTextRequest(_message.Message):
    __slots__ = ("user_id", "content")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    content: bytes
    def __init__(self, user_id: _Optional[str] = ..., content: _Optional[bytes] = ...) -> None: ...

class AudioToTextResponse(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

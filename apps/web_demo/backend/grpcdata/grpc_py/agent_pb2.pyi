from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

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

class StreamResponse(_message.Message):
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
    __slots__ = ("code", "msg", "data")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    data: AudioAndLipResponseData
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., data: _Optional[_Union[AudioAndLipResponseData, _Mapping]] = ...) -> None: ...

class AudioAndLipResponseData(_message.Message):
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
    __slots__ = ("code", "msg", "data")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    data: AddConversationResponseData
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., data: _Optional[_Union[AddConversationResponseData, _Mapping]] = ...) -> None: ...

class AddConversationResponseData(_message.Message):
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
    __slots__ = ("code", "msg")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ...) -> None: ...

class GetConversationsRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class GetConversationsResponse(_message.Message):
    __slots__ = ("code", "msg", "data")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    data: GetConversationsResponseData
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., data: _Optional[_Union[GetConversationsResponseData, _Mapping]] = ...) -> None: ...

class GetConversationsResponseData(_message.Message):
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
    __slots__ = ("code", "msg")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ...) -> None: ...

class GetLastMsgIdRequest(_message.Message):
    __slots__ = ("user_id", "conversation_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    conversation_id: str
    def __init__(self, user_id: _Optional[str] = ..., conversation_id: _Optional[str] = ...) -> None: ...

class GetLastMsgIdResponse(_message.Message):
    __slots__ = ("code", "msg", "data")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    data: GetLastMsgIdResponseData
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., data: _Optional[_Union[GetLastMsgIdResponseData, _Mapping]] = ...) -> None: ...

class GetLastMsgIdResponseData(_message.Message):
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
    __slots__ = ("code", "msg", "data")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    data: GetMessagesResponseData
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., data: _Optional[_Union[GetMessagesResponseData, _Mapping]] = ...) -> None: ...

class GetMessagesResponseData(_message.Message):
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
    __slots__ = ("code", "msg", "data")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    data: AliyunStsResponseData
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., data: _Optional[_Union[AliyunStsResponseData, _Mapping]] = ...) -> None: ...

class AliyunStsResponseData(_message.Message):
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
    __slots__ = ("code", "msg", "data")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    data: AudioToTextResponseData
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., data: _Optional[_Union[AudioToTextResponseData, _Mapping]] = ...) -> None: ...

class AudioToTextResponseData(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class AddFileRequest(_message.Message):
    __slots__ = ("api_type", "user_id", "base_id", "conversation_id", "file_name", "file")
    API_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    api_type: str
    user_id: int
    base_id: int
    conversation_id: int
    file_name: str
    file: bytes
    def __init__(self, api_type: _Optional[str] = ..., user_id: _Optional[int] = ..., base_id: _Optional[int] = ..., conversation_id: _Optional[int] = ..., file_name: _Optional[str] = ..., file: _Optional[bytes] = ...) -> None: ...

class GetIntroductionRequest(_message.Message):
    __slots__ = ("case_id",)
    CASE_ID_FIELD_NUMBER: _ClassVar[int]
    case_id: str
    def __init__(self, case_id: _Optional[str] = ...) -> None: ...

class GetIntroductionResponse(_message.Message):
    __slots__ = ("code", "msg", "data")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    data: _containers.RepeatedCompositeFieldContainer[GetIntroductionResponseData]
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., data: _Optional[_Iterable[_Union[GetIntroductionResponseData, _Mapping]]] = ...) -> None: ...

class GetIntroductionResponseData(_message.Message):
    __slots__ = ("agent_name", "message_blocks")
    AGENT_NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_BLOCKS_FIELD_NUMBER: _ClassVar[int]
    agent_name: str
    message_blocks: _containers.RepeatedCompositeFieldContainer[GetIntroductionResponseMessageBlockData]
    def __init__(self, agent_name: _Optional[str] = ..., message_blocks: _Optional[_Iterable[_Union[GetIntroductionResponseMessageBlockData, _Mapping]]] = ...) -> None: ...

class GetIntroductionResponseMessageBlockData(_message.Message):
    __slots__ = ("content_type", "content_tag", "content", "audio_and_lip")
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TAG_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    AUDIO_AND_LIP_FIELD_NUMBER: _ClassVar[int]
    content_type: str
    content_tag: str
    content: str
    audio_and_lip: AudioAndLipResponseData
    def __init__(self, content_type: _Optional[str] = ..., content_tag: _Optional[str] = ..., content: _Optional[str] = ..., audio_and_lip: _Optional[_Union[AudioAndLipResponseData, _Mapping]] = ...) -> None: ...

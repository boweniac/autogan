# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: agent.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x61gent.proto\x12\x05\x41gent\"I\n\x0c\x41gentRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x03\x12\x17\n\x0f\x63onversation_id\x18\x02 \x01(\x03\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"\x1e\n\x0eStreamResponse\x12\x0c\n\x04text\x18\x01 \x01(\t\"O\n\x12\x41udioAndLipRequest\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\r\n\x05model\x18\x02 \x01(\t\x12\r\n\x05voice\x18\x03 \x01(\t\x12\r\n\x05speed\x18\x04 \x01(\x02\"^\n\x13\x41udioAndLipResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12,\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x1e.Agent.AudioAndLipResponseData\"@\n\x17\x41udioAndLipResponseData\x12\x12\n\naudio_file\x18\x01 \x01(\t\x12\x11\n\tlips_data\x18\x02 \x01(\t\")\n\x16\x41\x64\x64\x43onversationRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"f\n\x17\x41\x64\x64\x43onversationResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12\x30\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\".Agent.AddConversationResponseData\"6\n\x1b\x41\x64\x64\x43onversationResponseData\x12\x17\n\x0f\x63onversation_id\x18\x01 \x01(\t\"Y\n\x1eUpdateConversationTitleRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x17\n\x0f\x63onversation_id\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\"<\n\x1fUpdateConversationTitleResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\"*\n\x17GetConversationsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"h\n\x18GetConversationsResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12\x31\n\x04\x64\x61ta\x18\x03 \x03(\x0b\x32#.Agent.GetConversationsResponseData\"9\n\x1cGetConversationsResponseData\x12\n\n\x02id\x18\x01 \x01(\x04\x12\r\n\x05title\x18\x02 \x01(\t\"E\n\x19\x44\x65leteConversationRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x17\n\x0f\x63onversation_id\x18\x02 \x01(\t\"7\n\x1a\x44\x65leteConversationResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\"?\n\x13GetLastMsgIdRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x17\n\x0f\x63onversation_id\x18\x02 \x01(\t\"`\n\x14GetLastMsgIdResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12-\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x1f.Agent.GetLastMsgIdResponseData\"*\n\x18GetLastMsgIdResponseData\x12\x0e\n\x06msg_id\x18\x01 \x01(\t\">\n\x12GetMessagesRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x17\n\x0f\x63onversation_id\x18\x02 \x01(\t\"^\n\x13GetMessagesResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12,\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x1e.Agent.GetMessagesResponseData\"+\n\x17GetMessagesResponseData\x12\x10\n\x08messages\x18\x01 \x03(\t\"#\n\x10\x41liyunStsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"Z\n\x11\x41liyunStsResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12*\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x1c.Agent.AliyunStsResponseData\"u\n\x15\x41liyunStsResponseData\x12\x15\n\raccess_key_id\x18\x01 \x01(\t\x12\x19\n\x11\x61\x63\x63\x65ss_key_secret\x18\x02 \x01(\t\x12\x12\n\nexpiration\x18\x03 \x01(\t\x12\x16\n\x0esecurity_token\x18\x04 \x01(\t\"6\n\x12\x41udioToTextRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"^\n\x13\x41udioToTextResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12,\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x1e.Agent.AudioToTextResponseData\"\'\n\x17\x41udioToTextResponseData\x12\x0c\n\x04text\x18\x01 \x01(\t\"~\n\x0e\x41\x64\x64\x46ileRequest\x12\x10\n\x08\x61pi_type\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\x04\x12\x0f\n\x07\x62\x61se_id\x18\x03 \x01(\x04\x12\x17\n\x0f\x63onversation_id\x18\x04 \x01(\x04\x12\x11\n\tfile_name\x18\x05 \x01(\t\x12\x0c\n\x04\x66ile\x18\x06 \x01(\x0c\")\n\x16GetIntroductionRequest\x12\x0f\n\x07\x63\x61se_id\x18\x01 \x01(\t\"f\n\x17GetIntroductionResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12\x30\n\x04\x64\x61ta\x18\x03 \x03(\x0b\x32\".Agent.GetIntroductionResponseData\"y\n\x1bGetIntroductionResponseData\x12\x12\n\nagent_name\x18\x01 \x01(\t\x12\x46\n\x0emessage_blocks\x18\x02 \x03(\x0b\x32..Agent.GetIntroductionResponseMessageBlockData\"\x9c\x01\n\'GetIntroductionResponseMessageBlockData\x12\x14\n\x0c\x63ontent_type\x18\x01 \x01(\t\x12\x13\n\x0b\x63ontent_tag\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x35\n\raudio_and_lip\x18\x04 \x01(\x0b\x32\x1e.Agent.AudioAndLipResponseData2\xc6\x07\n\x05\x41gent\x12@\n\x0eRpcAgentStream\x12\x13.Agent.AgentRequest\x1a\x15.Agent.StreamResponse\"\x00\x30\x01\x12G\n\x0eRpcAudioAndLip\x12\x19.Agent.AudioAndLipRequest\x1a\x1a.Agent.AudioAndLipResponse\x12S\n\x12RpcAddConversation\x12\x1d.Agent.AddConversationRequest\x1a\x1e.Agent.AddConversationResponse\x12k\n\x1aRpcUpdateConversationTitle\x12%.Agent.UpdateConversationTitleRequest\x1a&.Agent.UpdateConversationTitleResponse\x12V\n\x13RpcGetConversations\x12\x1e.Agent.GetConversationsRequest\x1a\x1f.Agent.GetConversationsResponse\x12\\\n\x15RpcDeleteConversation\x12 .Agent.DeleteConversationRequest\x1a!.Agent.DeleteConversationResponse\x12J\n\x0fRpcGetLastMsgId\x12\x1a.Agent.GetLastMsgIdRequest\x1a\x1b.Agent.GetLastMsgIdResponse\x12G\n\x0eRpcGetMessages\x12\x19.Agent.GetMessagesRequest\x1a\x1a.Agent.GetMessagesResponse\x12\x41\n\x0cRpcAliyunSts\x12\x17.Agent.AliyunStsRequest\x1a\x18.Agent.AliyunStsResponse\x12G\n\x0eRpcAudioToText\x12\x19.Agent.AudioToTextRequest\x1a\x1a.Agent.AudioToTextResponse\x12\x44\n\x10RpcAddFileStream\x12\x15.Agent.AddFileRequest\x1a\x15.Agent.StreamResponse\"\x00\x30\x01\x12S\n\x12RpcGetIntroduction\x12\x1d.Agent.GetIntroductionRequest\x1a\x1e.Agent.GetIntroductionResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'agent_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_AGENTREQUEST']._serialized_start=22
  _globals['_AGENTREQUEST']._serialized_end=95
  _globals['_STREAMRESPONSE']._serialized_start=97
  _globals['_STREAMRESPONSE']._serialized_end=127
  _globals['_AUDIOANDLIPREQUEST']._serialized_start=129
  _globals['_AUDIOANDLIPREQUEST']._serialized_end=208
  _globals['_AUDIOANDLIPRESPONSE']._serialized_start=210
  _globals['_AUDIOANDLIPRESPONSE']._serialized_end=304
  _globals['_AUDIOANDLIPRESPONSEDATA']._serialized_start=306
  _globals['_AUDIOANDLIPRESPONSEDATA']._serialized_end=370
  _globals['_ADDCONVERSATIONREQUEST']._serialized_start=372
  _globals['_ADDCONVERSATIONREQUEST']._serialized_end=413
  _globals['_ADDCONVERSATIONRESPONSE']._serialized_start=415
  _globals['_ADDCONVERSATIONRESPONSE']._serialized_end=517
  _globals['_ADDCONVERSATIONRESPONSEDATA']._serialized_start=519
  _globals['_ADDCONVERSATIONRESPONSEDATA']._serialized_end=573
  _globals['_UPDATECONVERSATIONTITLEREQUEST']._serialized_start=575
  _globals['_UPDATECONVERSATIONTITLEREQUEST']._serialized_end=664
  _globals['_UPDATECONVERSATIONTITLERESPONSE']._serialized_start=666
  _globals['_UPDATECONVERSATIONTITLERESPONSE']._serialized_end=726
  _globals['_GETCONVERSATIONSREQUEST']._serialized_start=728
  _globals['_GETCONVERSATIONSREQUEST']._serialized_end=770
  _globals['_GETCONVERSATIONSRESPONSE']._serialized_start=772
  _globals['_GETCONVERSATIONSRESPONSE']._serialized_end=876
  _globals['_GETCONVERSATIONSRESPONSEDATA']._serialized_start=878
  _globals['_GETCONVERSATIONSRESPONSEDATA']._serialized_end=935
  _globals['_DELETECONVERSATIONREQUEST']._serialized_start=937
  _globals['_DELETECONVERSATIONREQUEST']._serialized_end=1006
  _globals['_DELETECONVERSATIONRESPONSE']._serialized_start=1008
  _globals['_DELETECONVERSATIONRESPONSE']._serialized_end=1063
  _globals['_GETLASTMSGIDREQUEST']._serialized_start=1065
  _globals['_GETLASTMSGIDREQUEST']._serialized_end=1128
  _globals['_GETLASTMSGIDRESPONSE']._serialized_start=1130
  _globals['_GETLASTMSGIDRESPONSE']._serialized_end=1226
  _globals['_GETLASTMSGIDRESPONSEDATA']._serialized_start=1228
  _globals['_GETLASTMSGIDRESPONSEDATA']._serialized_end=1270
  _globals['_GETMESSAGESREQUEST']._serialized_start=1272
  _globals['_GETMESSAGESREQUEST']._serialized_end=1334
  _globals['_GETMESSAGESRESPONSE']._serialized_start=1336
  _globals['_GETMESSAGESRESPONSE']._serialized_end=1430
  _globals['_GETMESSAGESRESPONSEDATA']._serialized_start=1432
  _globals['_GETMESSAGESRESPONSEDATA']._serialized_end=1475
  _globals['_ALIYUNSTSREQUEST']._serialized_start=1477
  _globals['_ALIYUNSTSREQUEST']._serialized_end=1512
  _globals['_ALIYUNSTSRESPONSE']._serialized_start=1514
  _globals['_ALIYUNSTSRESPONSE']._serialized_end=1604
  _globals['_ALIYUNSTSRESPONSEDATA']._serialized_start=1606
  _globals['_ALIYUNSTSRESPONSEDATA']._serialized_end=1723
  _globals['_AUDIOTOTEXTREQUEST']._serialized_start=1725
  _globals['_AUDIOTOTEXTREQUEST']._serialized_end=1779
  _globals['_AUDIOTOTEXTRESPONSE']._serialized_start=1781
  _globals['_AUDIOTOTEXTRESPONSE']._serialized_end=1875
  _globals['_AUDIOTOTEXTRESPONSEDATA']._serialized_start=1877
  _globals['_AUDIOTOTEXTRESPONSEDATA']._serialized_end=1916
  _globals['_ADDFILEREQUEST']._serialized_start=1918
  _globals['_ADDFILEREQUEST']._serialized_end=2044
  _globals['_GETINTRODUCTIONREQUEST']._serialized_start=2046
  _globals['_GETINTRODUCTIONREQUEST']._serialized_end=2087
  _globals['_GETINTRODUCTIONRESPONSE']._serialized_start=2089
  _globals['_GETINTRODUCTIONRESPONSE']._serialized_end=2191
  _globals['_GETINTRODUCTIONRESPONSEDATA']._serialized_start=2193
  _globals['_GETINTRODUCTIONRESPONSEDATA']._serialized_end=2314
  _globals['_GETINTRODUCTIONRESPONSEMESSAGEBLOCKDATA']._serialized_start=2317
  _globals['_GETINTRODUCTIONRESPONSEMESSAGEBLOCKDATA']._serialized_end=2473
  _globals['_AGENT']._serialized_start=2476
  _globals['_AGENT']._serialized_end=3442
# @@protoc_insertion_point(module_scope)

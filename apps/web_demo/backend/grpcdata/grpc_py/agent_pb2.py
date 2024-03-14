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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x61gent.proto\x12\x05\x41gent\"I\n\x0c\x41gentRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\x12\x17\n\x0f\x63onversation_id\x18\x02 \x01(\x04\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"<\n\x10\x41utoTitleRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\x12\x17\n\x0f\x63onversation_id\x18\x02 \x01(\x04\"\x1e\n\x0eStreamResponse\x12\x0c\n\x04text\x18\x01 \x01(\t\"O\n\x12\x41udioAndLipRequest\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\r\n\x05model\x18\x02 \x01(\t\x12\r\n\x05voice\x18\x03 \x01(\t\x12\r\n\x05speed\x18\x04 \x01(\x02\"^\n\x13\x41udioAndLipResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12,\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x1e.Agent.AudioAndLipResponseData\"@\n\x17\x41udioAndLipResponseData\x12\x12\n\naudio_file\x18\x01 \x01(\t\x12\x11\n\tlips_data\x18\x02 \x01(\t\")\n\x16\x41\x64\x64\x43onversationRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\"f\n\x17\x41\x64\x64\x43onversationResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12\x30\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\".Agent.AddConversationResponseData\"6\n\x1b\x41\x64\x64\x43onversationResponseData\x12\x17\n\x0f\x63onversation_id\x18\x01 \x01(\t\"Y\n\x1eUpdateConversationTitleRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\x12\x17\n\x0f\x63onversation_id\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\"v\n\x1fUpdateConversationTitleResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12\x38\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32*.Agent.UpdateConversationTitleResponseData\"9\n#UpdateConversationTitleResponseData\x12\x12\n\nis_success\x18\x01 \x01(\x08\"*\n\x17GetConversationsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\"h\n\x18GetConversationsResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12\x31\n\x04\x64\x61ta\x18\x03 \x03(\x0b\x32#.Agent.GetConversationsResponseData\"9\n\x1cGetConversationsResponseData\x12\n\n\x02id\x18\x01 \x01(\x04\x12\r\n\x05title\x18\x02 \x01(\t\"E\n\x19\x44\x65leteConversationRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\x12\x17\n\x0f\x63onversation_id\x18\x02 \x01(\t\"j\n\x1a\x44\x65leteConversationResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12\x31\n\x04\x64\x61ta\x18\x03 \x03(\x0b\x32#.Agent.GetConversationsResponseData\"4\n\x1e\x44\x65leteConversationResponseData\x12\x12\n\nis_success\x18\x01 \x01(\x08\"?\n\x13GetLastMsgIdRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\x12\x17\n\x0f\x63onversation_id\x18\x02 \x01(\t\"`\n\x14GetLastMsgIdResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12-\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x1f.Agent.GetLastMsgIdResponseData\"*\n\x18GetLastMsgIdResponseData\x12\x0e\n\x06msg_id\x18\x01 \x01(\t\"^\n\x1dGetMessagesWhenChangedRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\x12\x17\n\x0f\x63onversation_id\x18\x02 \x01(\x04\x12\x13\n\x0blast_msg_id\x18\x03 \x01(\x04\"t\n\x1eGetMessagesWhenChangedResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12\x37\n\x04\x64\x61ta\x18\x03 \x03(\x0b\x32).Agent.GetMessagesWhenChangedResponseData\"\xb9\x01\n\"GetMessagesWhenChangedResponseData\x12\x0e\n\x06msg_id\x18\x01 \x01(\x04\x12\x0f\n\x07task_id\x18\x02 \x01(\x04\x12\x14\n\x0c\x63ontent_type\x18\x03 \x01(\t\x12\x13\n\x0b\x63ontent_tag\x18\x04 \x01(\t\x12\x12\n\nagent_name\x18\x05 \x01(\t\x12\x12\n\nagent_type\x18\x06 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x07 \x01(\t\x12\x0e\n\x06tokens\x18\x08 \x01(\r\">\n\x12GetMessagesRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\x12\x17\n\x0f\x63onversation_id\x18\x02 \x01(\x04\"^\n\x13GetMessagesResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12,\n\x04\x64\x61ta\x18\x03 \x03(\x0b\x32\x1e.Agent.GetMessagesResponseData\"\x9a\x01\n\x17GetMessagesResponseData\x12\x0e\n\x06msg_id\x18\x01 \x01(\x04\x12\x0f\n\x07task_id\x18\x02 \x01(\x04\x12\x14\n\x0c\x63ontent_type\x18\x03 \x01(\t\x12\x13\n\x0b\x63ontent_tag\x18\x04 \x01(\t\x12\x12\n\nagent_name\x18\x05 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x06 \x01(\t\x12\x0e\n\x06tokens\x18\x07 \x01(\r\"#\n\x10\x41liyunStsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\"Z\n\x11\x41liyunStsResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12*\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x1c.Agent.AliyunStsResponseData\"u\n\x15\x41liyunStsResponseData\x12\x15\n\raccess_key_id\x18\x01 \x01(\t\x12\x19\n\x11\x61\x63\x63\x65ss_key_secret\x18\x02 \x01(\t\x12\x12\n\nexpiration\x18\x03 \x01(\t\x12\x16\n\x0esecurity_token\x18\x04 \x01(\t\"6\n\x12\x41udioToTextRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"^\n\x13\x41udioToTextResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12,\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x1e.Agent.AudioToTextResponseData\"\'\n\x17\x41udioToTextResponseData\x12\x0c\n\x04text\x18\x01 \x01(\t\"~\n\x0e\x41\x64\x64\x46ileRequest\x12\x10\n\x08\x61pi_type\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\x04\x12\x0f\n\x07\x62\x61se_id\x18\x03 \x01(\x04\x12\x17\n\x0f\x63onversation_id\x18\x04 \x01(\x04\x12\x11\n\tfile_name\x18\x05 \x01(\t\x12\x0c\n\x04\x66ile\x18\x06 \x01(\x0c\")\n\x16GetIntroductionRequest\x12\x0f\n\x07\x63\x61se_id\x18\x01 \x01(\t\"f\n\x17GetIntroductionResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12\x30\n\x04\x64\x61ta\x18\x03 \x03(\x0b\x32\".Agent.GetIntroductionResponseData\"y\n\x1bGetIntroductionResponseData\x12\x12\n\nagent_name\x18\x01 \x01(\t\x12\x46\n\x0emessage_blocks\x18\x02 \x03(\x0b\x32..Agent.GetIntroductionResponseMessageBlockData\"\xab\x01\n\'GetIntroductionResponseMessageBlockData\x12\x14\n\x0c\x63ontent_type\x18\x01 \x01(\t\x12\x13\n\x0b\x63ontent_tag\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x44\n\raudio_and_lip\x18\x04 \x01(\x0b\x32-.Agent.GetIntroductionResponseAudioAndLipData\"\x87\x01\n&GetIntroductionResponseAudioAndLipData\x12J\n\naudio_file\x18\x01 \x01(\x0b\x32\x36.Agent.GetIntroductionResponseAudioAndLipAudioFileData\x12\x11\n\tlips_data\x18\x02 \x01(\t\"\xe2\x01\n/GetIntroductionResponseAudioAndLipAudioFileData\x12\x1c\n\x14\x63ustomer_manager_boy\x18\x01 \x01(\t\x12\x1d\n\x15\x63ustomer_manager_girl\x18\x02 \x01(\t\x12\r\n\x05\x63oder\x18\x03 \x01(\t\x12\x14\n\x0c\x64ocument_exp\x18\x04 \x01(\t\x12\x15\n\rsearch_expert\x18\x05 \x01(\t\x12\x11\n\tsecretary\x18\x06 \x01(\t\x12\x0e\n\x06tester\x18\x07 \x01(\t\x12\x13\n\x0bpainter_exp\x18\x08 \x01(\t\"Q\n\x14TextTranslateRequest\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\r\n\x05model\x18\x02 \x01(\t\x12\r\n\x05voice\x18\x03 \x01(\t\x12\r\n\x05speed\x18\x04 \x01(\x02\"b\n\x15TextTranslateResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12.\n\x04\x64\x61ta\x18\x03 \x03(\x0b\x32 .Agent.TextTranslateResponseData\"L\n\x19TextTranslateResponseData\x12\r\n\x05split\x18\x01 \x01(\t\x12\x11\n\ttranslate\x18\x02 \x01(\t\x12\r\n\x05\x61udio\x18\x03 \x01(\t2\xc9\t\n\x05\x41gent\x12@\n\x0eRpcAgentStream\x12\x13.Agent.AgentRequest\x1a\x15.Agent.StreamResponse\"\x00\x30\x01\x12H\n\x12RpcAutoTitleStream\x12\x17.Agent.AutoTitleRequest\x1a\x15.Agent.StreamResponse\"\x00\x30\x01\x12G\n\x0eRpcAudioAndLip\x12\x19.Agent.AudioAndLipRequest\x1a\x1a.Agent.AudioAndLipResponse\x12S\n\x12RpcAddConversation\x12\x1d.Agent.AddConversationRequest\x1a\x1e.Agent.AddConversationResponse\x12k\n\x1aRpcUpdateConversationTitle\x12%.Agent.UpdateConversationTitleRequest\x1a&.Agent.UpdateConversationTitleResponse\x12V\n\x13RpcGetConversations\x12\x1e.Agent.GetConversationsRequest\x1a\x1f.Agent.GetConversationsResponse\x12\\\n\x15RpcDeleteConversation\x12 .Agent.DeleteConversationRequest\x1a!.Agent.DeleteConversationResponse\x12J\n\x0fRpcGetLastMsgId\x12\x1a.Agent.GetLastMsgIdRequest\x1a\x1b.Agent.GetLastMsgIdResponse\x12h\n\x19RpcGetMessagesWhenChanged\x12$.Agent.GetMessagesWhenChangedRequest\x1a%.Agent.GetMessagesWhenChangedResponse\x12G\n\x0eRpcGetMessages\x12\x19.Agent.GetMessagesRequest\x1a\x1a.Agent.GetMessagesResponse\x12\x41\n\x0cRpcAliyunSts\x12\x17.Agent.AliyunStsRequest\x1a\x18.Agent.AliyunStsResponse\x12G\n\x0eRpcAudioToText\x12\x19.Agent.AudioToTextRequest\x1a\x1a.Agent.AudioToTextResponse\x12\x44\n\x10RpcAddFileStream\x12\x15.Agent.AddFileRequest\x1a\x15.Agent.StreamResponse\"\x00\x30\x01\x12S\n\x12RpcGetIntroduction\x12\x1d.Agent.GetIntroductionRequest\x1a\x1e.Agent.GetIntroductionResponse\x12M\n\x10RpcTextTranslate\x12\x1b.Agent.TextTranslateRequest\x1a\x1c.Agent.TextTranslateResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'agent_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_AGENTREQUEST']._serialized_start=22
  _globals['_AGENTREQUEST']._serialized_end=95
  _globals['_AUTOTITLEREQUEST']._serialized_start=97
  _globals['_AUTOTITLEREQUEST']._serialized_end=157
  _globals['_STREAMRESPONSE']._serialized_start=159
  _globals['_STREAMRESPONSE']._serialized_end=189
  _globals['_AUDIOANDLIPREQUEST']._serialized_start=191
  _globals['_AUDIOANDLIPREQUEST']._serialized_end=270
  _globals['_AUDIOANDLIPRESPONSE']._serialized_start=272
  _globals['_AUDIOANDLIPRESPONSE']._serialized_end=366
  _globals['_AUDIOANDLIPRESPONSEDATA']._serialized_start=368
  _globals['_AUDIOANDLIPRESPONSEDATA']._serialized_end=432
  _globals['_ADDCONVERSATIONREQUEST']._serialized_start=434
  _globals['_ADDCONVERSATIONREQUEST']._serialized_end=475
  _globals['_ADDCONVERSATIONRESPONSE']._serialized_start=477
  _globals['_ADDCONVERSATIONRESPONSE']._serialized_end=579
  _globals['_ADDCONVERSATIONRESPONSEDATA']._serialized_start=581
  _globals['_ADDCONVERSATIONRESPONSEDATA']._serialized_end=635
  _globals['_UPDATECONVERSATIONTITLEREQUEST']._serialized_start=637
  _globals['_UPDATECONVERSATIONTITLEREQUEST']._serialized_end=726
  _globals['_UPDATECONVERSATIONTITLERESPONSE']._serialized_start=728
  _globals['_UPDATECONVERSATIONTITLERESPONSE']._serialized_end=846
  _globals['_UPDATECONVERSATIONTITLERESPONSEDATA']._serialized_start=848
  _globals['_UPDATECONVERSATIONTITLERESPONSEDATA']._serialized_end=905
  _globals['_GETCONVERSATIONSREQUEST']._serialized_start=907
  _globals['_GETCONVERSATIONSREQUEST']._serialized_end=949
  _globals['_GETCONVERSATIONSRESPONSE']._serialized_start=951
  _globals['_GETCONVERSATIONSRESPONSE']._serialized_end=1055
  _globals['_GETCONVERSATIONSRESPONSEDATA']._serialized_start=1057
  _globals['_GETCONVERSATIONSRESPONSEDATA']._serialized_end=1114
  _globals['_DELETECONVERSATIONREQUEST']._serialized_start=1116
  _globals['_DELETECONVERSATIONREQUEST']._serialized_end=1185
  _globals['_DELETECONVERSATIONRESPONSE']._serialized_start=1187
  _globals['_DELETECONVERSATIONRESPONSE']._serialized_end=1293
  _globals['_DELETECONVERSATIONRESPONSEDATA']._serialized_start=1295
  _globals['_DELETECONVERSATIONRESPONSEDATA']._serialized_end=1347
  _globals['_GETLASTMSGIDREQUEST']._serialized_start=1349
  _globals['_GETLASTMSGIDREQUEST']._serialized_end=1412
  _globals['_GETLASTMSGIDRESPONSE']._serialized_start=1414
  _globals['_GETLASTMSGIDRESPONSE']._serialized_end=1510
  _globals['_GETLASTMSGIDRESPONSEDATA']._serialized_start=1512
  _globals['_GETLASTMSGIDRESPONSEDATA']._serialized_end=1554
  _globals['_GETMESSAGESWHENCHANGEDREQUEST']._serialized_start=1556
  _globals['_GETMESSAGESWHENCHANGEDREQUEST']._serialized_end=1650
  _globals['_GETMESSAGESWHENCHANGEDRESPONSE']._serialized_start=1652
  _globals['_GETMESSAGESWHENCHANGEDRESPONSE']._serialized_end=1768
  _globals['_GETMESSAGESWHENCHANGEDRESPONSEDATA']._serialized_start=1771
  _globals['_GETMESSAGESWHENCHANGEDRESPONSEDATA']._serialized_end=1956
  _globals['_GETMESSAGESREQUEST']._serialized_start=1958
  _globals['_GETMESSAGESREQUEST']._serialized_end=2020
  _globals['_GETMESSAGESRESPONSE']._serialized_start=2022
  _globals['_GETMESSAGESRESPONSE']._serialized_end=2116
  _globals['_GETMESSAGESRESPONSEDATA']._serialized_start=2119
  _globals['_GETMESSAGESRESPONSEDATA']._serialized_end=2273
  _globals['_ALIYUNSTSREQUEST']._serialized_start=2275
  _globals['_ALIYUNSTSREQUEST']._serialized_end=2310
  _globals['_ALIYUNSTSRESPONSE']._serialized_start=2312
  _globals['_ALIYUNSTSRESPONSE']._serialized_end=2402
  _globals['_ALIYUNSTSRESPONSEDATA']._serialized_start=2404
  _globals['_ALIYUNSTSRESPONSEDATA']._serialized_end=2521
  _globals['_AUDIOTOTEXTREQUEST']._serialized_start=2523
  _globals['_AUDIOTOTEXTREQUEST']._serialized_end=2577
  _globals['_AUDIOTOTEXTRESPONSE']._serialized_start=2579
  _globals['_AUDIOTOTEXTRESPONSE']._serialized_end=2673
  _globals['_AUDIOTOTEXTRESPONSEDATA']._serialized_start=2675
  _globals['_AUDIOTOTEXTRESPONSEDATA']._serialized_end=2714
  _globals['_ADDFILEREQUEST']._serialized_start=2716
  _globals['_ADDFILEREQUEST']._serialized_end=2842
  _globals['_GETINTRODUCTIONREQUEST']._serialized_start=2844
  _globals['_GETINTRODUCTIONREQUEST']._serialized_end=2885
  _globals['_GETINTRODUCTIONRESPONSE']._serialized_start=2887
  _globals['_GETINTRODUCTIONRESPONSE']._serialized_end=2989
  _globals['_GETINTRODUCTIONRESPONSEDATA']._serialized_start=2991
  _globals['_GETINTRODUCTIONRESPONSEDATA']._serialized_end=3112
  _globals['_GETINTRODUCTIONRESPONSEMESSAGEBLOCKDATA']._serialized_start=3115
  _globals['_GETINTRODUCTIONRESPONSEMESSAGEBLOCKDATA']._serialized_end=3286
  _globals['_GETINTRODUCTIONRESPONSEAUDIOANDLIPDATA']._serialized_start=3289
  _globals['_GETINTRODUCTIONRESPONSEAUDIOANDLIPDATA']._serialized_end=3424
  _globals['_GETINTRODUCTIONRESPONSEAUDIOANDLIPAUDIOFILEDATA']._serialized_start=3427
  _globals['_GETINTRODUCTIONRESPONSEAUDIOANDLIPAUDIOFILEDATA']._serialized_end=3653
  _globals['_TEXTTRANSLATEREQUEST']._serialized_start=3655
  _globals['_TEXTTRANSLATEREQUEST']._serialized_end=3736
  _globals['_TEXTTRANSLATERESPONSE']._serialized_start=3738
  _globals['_TEXTTRANSLATERESPONSE']._serialized_end=3836
  _globals['_TEXTTRANSLATERESPONSEDATA']._serialized_start=3838
  _globals['_TEXTTRANSLATERESPONSEDATA']._serialized_end=3914
  _globals['_AGENT']._serialized_start=3917
  _globals['_AGENT']._serialized_end=5142
# @@protoc_insertion_point(module_scope)

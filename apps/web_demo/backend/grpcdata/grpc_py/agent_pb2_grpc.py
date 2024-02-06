# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import agent_pb2 as agent__pb2


class AgentStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RpcAgentStream = channel.unary_stream(
                '/Agent.Agent/RpcAgentStream',
                request_serializer=agent__pb2.AgentRequest.SerializeToString,
                response_deserializer=agent__pb2.StreamResponse.FromString,
                )
        self.RpcAudioAndLip = channel.unary_unary(
                '/Agent.Agent/RpcAudioAndLip',
                request_serializer=agent__pb2.AudioAndLipRequest.SerializeToString,
                response_deserializer=agent__pb2.AudioAndLipResponse.FromString,
                )
        self.RpcAddConversation = channel.unary_unary(
                '/Agent.Agent/RpcAddConversation',
                request_serializer=agent__pb2.AddConversationRequest.SerializeToString,
                response_deserializer=agent__pb2.AddConversationResponse.FromString,
                )
        self.RpcUpdateConversationTitle = channel.unary_unary(
                '/Agent.Agent/RpcUpdateConversationTitle',
                request_serializer=agent__pb2.UpdateConversationTitleRequest.SerializeToString,
                response_deserializer=agent__pb2.UpdateConversationTitleResponse.FromString,
                )
        self.RpcGetConversations = channel.unary_unary(
                '/Agent.Agent/RpcGetConversations',
                request_serializer=agent__pb2.GetConversationsRequest.SerializeToString,
                response_deserializer=agent__pb2.GetConversationsResponse.FromString,
                )
        self.RpcDeleteConversation = channel.unary_unary(
                '/Agent.Agent/RpcDeleteConversation',
                request_serializer=agent__pb2.DeleteConversationRequest.SerializeToString,
                response_deserializer=agent__pb2.DeleteConversationResponse.FromString,
                )
        self.RpcGetLastMsgId = channel.unary_unary(
                '/Agent.Agent/RpcGetLastMsgId',
                request_serializer=agent__pb2.GetLastMsgIdRequest.SerializeToString,
                response_deserializer=agent__pb2.GetLastMsgIdResponse.FromString,
                )
        self.RpcGetMessagesWhenChanged = channel.unary_unary(
                '/Agent.Agent/RpcGetMessagesWhenChanged',
                request_serializer=agent__pb2.GetMessagesWhenChangedRequest.SerializeToString,
                response_deserializer=agent__pb2.GetMessagesWhenChangedResponse.FromString,
                )
        self.RpcGetMessages = channel.unary_unary(
                '/Agent.Agent/RpcGetMessages',
                request_serializer=agent__pb2.GetMessagesRequest.SerializeToString,
                response_deserializer=agent__pb2.GetMessagesResponse.FromString,
                )
        self.RpcAliyunSts = channel.unary_unary(
                '/Agent.Agent/RpcAliyunSts',
                request_serializer=agent__pb2.AliyunStsRequest.SerializeToString,
                response_deserializer=agent__pb2.AliyunStsResponse.FromString,
                )
        self.RpcAudioToText = channel.unary_unary(
                '/Agent.Agent/RpcAudioToText',
                request_serializer=agent__pb2.AudioToTextRequest.SerializeToString,
                response_deserializer=agent__pb2.AudioToTextResponse.FromString,
                )
        self.RpcAddFileStream = channel.unary_stream(
                '/Agent.Agent/RpcAddFileStream',
                request_serializer=agent__pb2.AddFileRequest.SerializeToString,
                response_deserializer=agent__pb2.StreamResponse.FromString,
                )
        self.RpcGetIntroduction = channel.unary_unary(
                '/Agent.Agent/RpcGetIntroduction',
                request_serializer=agent__pb2.GetIntroductionRequest.SerializeToString,
                response_deserializer=agent__pb2.GetIntroductionResponse.FromString,
                )


class AgentServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RpcAgentStream(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RpcAudioAndLip(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RpcAddConversation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RpcUpdateConversationTitle(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RpcGetConversations(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RpcDeleteConversation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RpcGetLastMsgId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RpcGetMessagesWhenChanged(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RpcGetMessages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RpcAliyunSts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RpcAudioToText(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RpcAddFileStream(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RpcGetIntroduction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AgentServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RpcAgentStream': grpc.unary_stream_rpc_method_handler(
                    servicer.RpcAgentStream,
                    request_deserializer=agent__pb2.AgentRequest.FromString,
                    response_serializer=agent__pb2.StreamResponse.SerializeToString,
            ),
            'RpcAudioAndLip': grpc.unary_unary_rpc_method_handler(
                    servicer.RpcAudioAndLip,
                    request_deserializer=agent__pb2.AudioAndLipRequest.FromString,
                    response_serializer=agent__pb2.AudioAndLipResponse.SerializeToString,
            ),
            'RpcAddConversation': grpc.unary_unary_rpc_method_handler(
                    servicer.RpcAddConversation,
                    request_deserializer=agent__pb2.AddConversationRequest.FromString,
                    response_serializer=agent__pb2.AddConversationResponse.SerializeToString,
            ),
            'RpcUpdateConversationTitle': grpc.unary_unary_rpc_method_handler(
                    servicer.RpcUpdateConversationTitle,
                    request_deserializer=agent__pb2.UpdateConversationTitleRequest.FromString,
                    response_serializer=agent__pb2.UpdateConversationTitleResponse.SerializeToString,
            ),
            'RpcGetConversations': grpc.unary_unary_rpc_method_handler(
                    servicer.RpcGetConversations,
                    request_deserializer=agent__pb2.GetConversationsRequest.FromString,
                    response_serializer=agent__pb2.GetConversationsResponse.SerializeToString,
            ),
            'RpcDeleteConversation': grpc.unary_unary_rpc_method_handler(
                    servicer.RpcDeleteConversation,
                    request_deserializer=agent__pb2.DeleteConversationRequest.FromString,
                    response_serializer=agent__pb2.DeleteConversationResponse.SerializeToString,
            ),
            'RpcGetLastMsgId': grpc.unary_unary_rpc_method_handler(
                    servicer.RpcGetLastMsgId,
                    request_deserializer=agent__pb2.GetLastMsgIdRequest.FromString,
                    response_serializer=agent__pb2.GetLastMsgIdResponse.SerializeToString,
            ),
            'RpcGetMessagesWhenChanged': grpc.unary_unary_rpc_method_handler(
                    servicer.RpcGetMessagesWhenChanged,
                    request_deserializer=agent__pb2.GetMessagesWhenChangedRequest.FromString,
                    response_serializer=agent__pb2.GetMessagesWhenChangedResponse.SerializeToString,
            ),
            'RpcGetMessages': grpc.unary_unary_rpc_method_handler(
                    servicer.RpcGetMessages,
                    request_deserializer=agent__pb2.GetMessagesRequest.FromString,
                    response_serializer=agent__pb2.GetMessagesResponse.SerializeToString,
            ),
            'RpcAliyunSts': grpc.unary_unary_rpc_method_handler(
                    servicer.RpcAliyunSts,
                    request_deserializer=agent__pb2.AliyunStsRequest.FromString,
                    response_serializer=agent__pb2.AliyunStsResponse.SerializeToString,
            ),
            'RpcAudioToText': grpc.unary_unary_rpc_method_handler(
                    servicer.RpcAudioToText,
                    request_deserializer=agent__pb2.AudioToTextRequest.FromString,
                    response_serializer=agent__pb2.AudioToTextResponse.SerializeToString,
            ),
            'RpcAddFileStream': grpc.unary_stream_rpc_method_handler(
                    servicer.RpcAddFileStream,
                    request_deserializer=agent__pb2.AddFileRequest.FromString,
                    response_serializer=agent__pb2.StreamResponse.SerializeToString,
            ),
            'RpcGetIntroduction': grpc.unary_unary_rpc_method_handler(
                    servicer.RpcGetIntroduction,
                    request_deserializer=agent__pb2.GetIntroductionRequest.FromString,
                    response_serializer=agent__pb2.GetIntroductionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Agent.Agent', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Agent(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RpcAgentStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Agent.Agent/RpcAgentStream',
            agent__pb2.AgentRequest.SerializeToString,
            agent__pb2.StreamResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RpcAudioAndLip(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Agent.Agent/RpcAudioAndLip',
            agent__pb2.AudioAndLipRequest.SerializeToString,
            agent__pb2.AudioAndLipResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RpcAddConversation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Agent.Agent/RpcAddConversation',
            agent__pb2.AddConversationRequest.SerializeToString,
            agent__pb2.AddConversationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RpcUpdateConversationTitle(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Agent.Agent/RpcUpdateConversationTitle',
            agent__pb2.UpdateConversationTitleRequest.SerializeToString,
            agent__pb2.UpdateConversationTitleResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RpcGetConversations(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Agent.Agent/RpcGetConversations',
            agent__pb2.GetConversationsRequest.SerializeToString,
            agent__pb2.GetConversationsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RpcDeleteConversation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Agent.Agent/RpcDeleteConversation',
            agent__pb2.DeleteConversationRequest.SerializeToString,
            agent__pb2.DeleteConversationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RpcGetLastMsgId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Agent.Agent/RpcGetLastMsgId',
            agent__pb2.GetLastMsgIdRequest.SerializeToString,
            agent__pb2.GetLastMsgIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RpcGetMessagesWhenChanged(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Agent.Agent/RpcGetMessagesWhenChanged',
            agent__pb2.GetMessagesWhenChangedRequest.SerializeToString,
            agent__pb2.GetMessagesWhenChangedResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RpcGetMessages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Agent.Agent/RpcGetMessages',
            agent__pb2.GetMessagesRequest.SerializeToString,
            agent__pb2.GetMessagesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RpcAliyunSts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Agent.Agent/RpcAliyunSts',
            agent__pb2.AliyunStsRequest.SerializeToString,
            agent__pb2.AliyunStsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RpcAudioToText(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Agent.Agent/RpcAudioToText',
            agent__pb2.AudioToTextRequest.SerializeToString,
            agent__pb2.AudioToTextResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RpcAddFileStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Agent.Agent/RpcAddFileStream',
            agent__pb2.AddFileRequest.SerializeToString,
            agent__pb2.StreamResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RpcGetIntroduction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Agent.Agent/RpcGetIntroduction',
            agent__pb2.GetIntroductionRequest.SerializeToString,
            agent__pb2.GetIntroductionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

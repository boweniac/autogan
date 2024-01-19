import threading
from pydub import AudioSegment
from apps.web_demo.backend.utils.aliyun_nls import TestSr

import consul
from concurrent import futures
import grpc
import queue

from apps.web_demo.backend.response.grpc import GrpcResponse

from apps.web_demo.backend.db.redis_storage import RedisStorage
from fastapi import HTTPException, FastAPI
from starlette import status

from apps.web_demo.backend.service.test_service import TestService
from apps.web_demo.backend.utils.aliyun_oss import Sample
from autogan.oai.audio_api_utils import AudioSpeechRequest
from autogan.oai.audio_generate_utils import generate_audio
from autogan.utils.uuid_utils import SnowflakeIdGenerator
from grpcdata.grpc_py import agent_pb2_grpc, agent_pb2
from grpcdata.grpc_py import helloworld_pb2
from grpcdata.grpc_py import helloworld_pb2_grpc
from grpcdata.grpc_py import health_pb2
from grpcdata.grpc_py import health_pb2_grpc

app = FastAPI()
storage = RedisStorage("172.17.0.1", 60101, 0)
snowflake_id = SnowflakeIdGenerator(datacenter_id=1, worker_id=1)
test_service = TestService("LLM_CONFIG", "off", True, storage)


class HelloWorld(helloworld_pb2_grpc.HelloWorldServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message=f'Hello, {request.name}')


class Health(health_pb2_grpc.HealthServicer):
    def Check(self, request, context):
        return health_pb2.HealthCheckResponse(status=health_pb2.HealthCheckResponse.SERVING)


class Agent(agent_pb2_grpc.AgentServicer):
    def RpcAgentStream(self, request, context):
        try:
            user_id = request.user_id
            conversation_id = request.conversation_id
            content = request.content
            if not user_id or not conversation_id or not content:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="User ID, Conversation ID and Content must not be empty")
            if storage.user_conversation_permissions(user_id, conversation_id):
                data_queue = queue.Queue()
                stop_event = threading.Event()
                stream_response = GrpcResponse(data_queue, stop_event)
                test_thread = threading.Thread(target=test_service.receive, args=(
                    conversation_id, conversation_id, "Customer", content, stream_response, snowflake_id))
                test_thread.start()
                while True:
                    while not data_queue.empty():
                        yield agent_pb2.AgentResponse(text=data_queue.get())
                    if not context.is_active() or not test_thread.is_alive():
                        stop_event.set()
                        test_thread.join()
                        break
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conversation permissions are wrong")
        except HTTPException as e:
            return e
        except Exception as e:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def RpcAudioAndLip(self, request, context):
        text = request.text
        model = request.model
        voice = request.voice
        speed = request.speed

        audio_speech_request = AudioSpeechRequest(text, model, voice, speed)

        file_name, lips_data = generate_audio(audio_speech_request)

        file_url = f"https://aibowen-base.boweniac.top/{file_name}"

        return agent_pb2.AudioAndLipResponse(audio_file=file_url, lips_data=lips_data)

    def RpcAddConversation(self, request, context):
        user_id = request.user_id

        conversation_id = snowflake_id.next_id()

        if storage.add_conversation(user_id, conversation_id):
            return agent_pb2.AddConversationResponse(conversation_id="")
        else:
            return agent_pb2.AddConversationResponse(conversation_id=str(conversation_id))

    def RpcUpdateConversationTitle(self, request, context):
        user_id = request.user_id
        conversation_id = request.conversation_id
        title = request.title

        storage.update_conversation_title(user_id, conversation_id, title)
        return agent_pb2.UpdateConversationTitleResponse(is_success=True)

    def RpcGetConversations(self, request, context):
        user_id = request.user_id

        conversations = storage.get_conversations(user_id)
        return agent_pb2.GetConversationsResponse(conversations=conversations)

    def RpcDeleteConversation(self, request, context):
        user_id = request.user_id
        conversation_id = request.conversation_id

        storage.delete_conversation(user_id, conversation_id)
        return agent_pb2.DeleteConversationResponse(is_success=True)

    def RpcGetLastMsgId(self, request, context):
        try:
            user_id = request.user_id
            conversation_id = request.conversation_id
            if not user_id or not conversation_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="User ID and Conversation ID must not be empty")

            if storage.user_conversation_permissions(user_id, conversation_id):
                msg_id = storage.get_last_msg_id(conversation_id)
                return agent_pb2.GetLastMsgIdResponse(msg_id=str(msg_id))
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conversation permissions are wrong")
        except Exception as e:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def RpcGetMessages(self, request, context):
        try:
            user_id = request.user_id
            conversation_id = request.conversation_id
            if not user_id or not conversation_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="User ID and Conversation ID must not be empty")

            if storage.user_conversation_permissions(user_id, conversation_id):
                messages = storage.get_messages(conversation_id)
                return agent_pb2.GetMessagesResponse(messages=messages)
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Conversation permissions are wrong")
        except Exception as e:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def RpcAliyunSts(self, request, context):
        try:
            user_id = request.user_id
            assumeRoleResponse = Sample.main()
            return agent_pb2.AliyunStsResponse(access_key_id=assumeRoleResponse.access_key_id,
                                               access_key_secret=assumeRoleResponse.access_key_secret,
                                               expiration=assumeRoleResponse.expiration,
                                               security_token=assumeRoleResponse.security_token)
        except Exception as e:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def RpcAudioToText(self, request, context):
        file_content = request.content

        # 这里可以添加保存文件的逻辑
        with open("file_name.mp4", "wb") as f:
            f.write(file_content)

        audio = AudioSegment.from_file("file_name.mp4", format="mp4")
        audio.export("file_name.wav", format="wav")
        # token = nls_token()
        name = "thread" + str(1)
        t = TestSr(name, "file_name.wav")
        t.start()
        return agent_pb2.AudioToTextResponse(text="assumeRoleResponse.access_key_id")


def serve():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        helloworld_pb2_grpc.add_HelloWorldServicer_to_server(HelloWorld(), server)
        health_pb2_grpc.add_HealthServicer_to_server(Health(), server)
        agent_pb2_grpc.add_AgentServicer_to_server(Agent(), server)

        server.add_insecure_port('[::]:60208')
        server.start()
        print("gRPC server started on port 60208.")

        c = consul.Consul(host="172.17.0.1", port=60401)

        # 尝试注册服务到Consul
        c.agent.service.register(
            "agent",
            service_id="agent-1",
            address="172.17.0.1",
            port=60208,
            tags=["grpc"],
            check=consul.Check().grpc("172.17.0.1:60208", interval="10s")  # 定义gRPC健康检查
        )
        print("Service registered with Consul.")

        server.wait_for_termination()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    serve()

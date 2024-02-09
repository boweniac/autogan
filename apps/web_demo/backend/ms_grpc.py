import json
import os
import threading

import autogan

from apps.web_demo.backend.db.db_storage import DBStorage
from apps.web_demo.backend.introduction_data import introduction_data
from autogan.oai.conv_holder import ConvHolder
from autogan.tools.file_tool import File
from pydub import AudioSegment

from apps.web_demo.backend.utils.aliyun.aliyun_access import AliyunAccess, aliyun_access
from apps.web_demo.backend.utils.aliyun.aliyun_nls import TestSr

import consul
from concurrent import futures
import grpc
import queue

from apps.web_demo.backend.response.grpc import GrpcResponse

from apps.web_demo.backend.db.redis_storage import RedisStorage
from fastapi import HTTPException, FastAPI
from starlette import status

from apps.web_demo.backend.service.test_service import TestService
from apps.web_demo.backend.utils.aliyun.aliyun_oss import Sample, bucket
from autogan.oai.audio_api_utils import AudioSpeechRequest
from autogan.oai.audio_generate_utils import generate_audio
from autogan.utils.es_utils import ESSearch
from autogan.utils.uuid_utils import SnowflakeIdGenerator
from grpcdata.grpc_py import agent_pb2_grpc, agent_pb2
from grpcdata.grpc_py import helloworld_pb2
from grpcdata.grpc_py import helloworld_pb2_grpc
from grpcdata.grpc_py import health_pb2
from grpcdata.grpc_py import health_pb2_grpc

app = FastAPI()
storage = DBStorage()
snowflake_id = SnowflakeIdGenerator(datacenter_id=1, worker_id=1)
es_config_dict = autogan.dict_from_json("ES_SEARCH")
es = ESSearch(es_config_dict["host"], es_config_dict["port"], es_config_dict["dims"])
test_service = TestService("LLM_CONFIG", "off", True, storage, es)
consul_config_dict = autogan.dict_from_json("CONSUL_CONFIG")


# aliyun_access = AliyunAccess()

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
                        yield agent_pb2.StreamResponse(text=data_queue.get())
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

    def RpcAutoTitleStream(self, request, context):
        try:
            user_id = request.user_id
            conversation_id = request.conversation_id
            if not user_id or not conversation_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="User ID, Conversation ID and Content must not be empty")
            if storage.user_conversation_permissions(user_id, conversation_id):
                data_queue = queue.Queue()
                stop_event = threading.Event()
                stream_response = GrpcResponse(data_queue, stop_event)
                test_thread = threading.Thread(target=test_service.auto_title, args=(
                    user_id, conversation_id, stream_response, snowflake_id))
                test_thread.start()
                while True:
                    while not data_queue.empty():
                        yield agent_pb2.StreamResponse(text=data_queue.get())
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

        return agent_pb2.AudioAndLipResponse(code=200, data={"audio_file": file_url, "lips_data": lips_data})

    def RpcAddConversation(self, request, context):
        user_id = request.user_id

        conversation_id = snowflake_id.next_id()

        storage.add_conversation(user_id, conversation_id)
        return agent_pb2.AddConversationResponse(code=200, data={"conversation_id": str(conversation_id)})

    def RpcUpdateConversationTitle(self, request, context):
        user_id = request.user_id
        conversation_id = request.conversation_id
        title = request.title

        storage.update_conversation_title(user_id, conversation_id, title)
        return agent_pb2.UpdateConversationTitleResponse(code=200)

    def RpcGetConversations(self, request, context):
        user_id = request.user_id
        conversations = storage.get_conversations(user_id)
        if conversations is None:
            conversations = []
        return agent_pb2.GetConversationsResponse(code=200, data=conversations)

    def RpcDeleteConversation(self, request, context):
        user_id = request.user_id
        conversation_id = request.conversation_id

        storage.delete_conversation(user_id, conversation_id)
        return agent_pb2.DeleteConversationResponse(code=200)

    def RpcGetLastMsgId(self, request, context):
        try:
            user_id = request.user_id
            conversation_id = request.conversation_id
            if not user_id or not conversation_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="User ID and Conversation ID must not be empty")

            if storage.user_conversation_permissions(user_id, conversation_id):
                msg_id = storage.get_last_msg_id(conversation_id)
                return agent_pb2.GetLastMsgIdResponse(code=200, data={"msg_id": str(msg_id)})
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conversation permissions are wrong")
        except Exception as e:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def RpcGetMessagesWhenChanged(self, request, context):
        try:
            user_id = request.user_id
            conversation_id = request.conversation_id
            last_msg_id = request.last_msg_id

            if not user_id or not conversation_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="User ID and Conversation ID must not be empty")

            if storage.user_conversation_permissions(user_id, conversation_id):
                messages = storage.get_messages_when_changed(conversation_id, last_msg_id)
                if messages is None:
                    messages = []
                return agent_pb2.GetMessagesWhenChangedResponse(code=200, data=messages)
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Conversation permissions are wrong")
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
                return agent_pb2.GetMessagesResponse(code=200, data=messages)
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Conversation permissions are wrong")
        except Exception as e:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def RpcAliyunSts(self, request, context):
        try:
            user_id = request.user_id
            assumeRoleResponse = Sample.main()

            data = {
                "access_key_id": assumeRoleResponse.access_key_id,
                "access_key_secret": assumeRoleResponse.access_key_secret,
                "expiration": assumeRoleResponse.expiration,
                "security_token": assumeRoleResponse.security_token
            }
            return agent_pb2.AliyunStsResponse(code=200, data=data)
        except Exception as e:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def RpcAudioToText(self, request, context):
        file_content = request.content

        # 这里可以添加保存文件的逻辑
        with open("file_name.mp4", "wb") as f:
            f.write(file_content)

        audio = AudioSegment.from_file("file_name.mp4", format="mp4")
        audio.export("file_name.wav", format="wav")
        name = "thread" + str(1)
        t = TestSr(name, "file_name.wav")
        r = t.test_run()
        return agent_pb2.AudioToTextResponse(code=200, data={"text": r})

    def RpcAddFileStream(self, request, context):
        try:
            api_type = request.api_type
            user_id = request.user_id
            base_id = request.base_id
            conversation_id = request.conversation_id
            _, ext = os.path.splitext(request.file_name)
            file_name = f"{snowflake_id.next_id()}.{ext}"
            file = request.file
            with open(f"extensions/{file_name}", "wb") as f:
                f.write(file)
            bucket.put_object_from_file(file_name, f"extensions/{file_name}")
            ft = File()
            text = ft.read(file_name)
            if not user_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="User ID must not be empty")

            data_queue = queue.Queue()
            stop_event = threading.Event()
            # stream_response = GrpcResponse(data_queue, stop_event)
            if api_type == "chat":
                msg_id = snowflake_id.next_id()
                msg = {
                    "msg_id": msg_id,
                    "task_id": conversation_id,
                    "content_type": "file",
                    "content_tag": file_name,
                    "agent_name": "Customer",
                    "content": f"Upload file: {file_name}",
                    "tokens": 0
                }
                storage.add_message(conversation_id, msg)
                test_service.add_file_message(conversation_id, "Customer", file_name)
                data = {
                    "msg_id": msg_id,
                    "agent_name": "Customer",
                    "step": file_name,
                    "index": 0,
                    "length": 0,
                }
                data_str = f'data: {json.dumps(data, ensure_ascii=False)}\n\n'
                data_queue.put(data_str)

                test_thread = threading.Thread(target=es.add_chat_file, args=(
                    user_id, conversation_id, file_name, text, data_queue))
            else:
                test_thread = threading.Thread(target=es.add_user_file, args=(
                    user_id, base_id, file_name, text, data_queue))
            test_thread.start()
            while True:
                while not data_queue.empty():
                    yield agent_pb2.StreamResponse(text=data_queue.get())
                if not context.is_active() or not test_thread.is_alive():
                    stop_event.set()
                    test_thread.join()
                    break
        except HTTPException as e:
            return e
        except Exception as e:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def RpcGetIntroduction(self, request, context):
        case_id = request.case_id

        if case_id == "introduction":
            data = introduction_data
        else:
            data = []
        return agent_pb2.GetIntroductionResponse(code=200, data=data)


def serve():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        helloworld_pb2_grpc.add_HelloWorldServicer_to_server(HelloWorld(), server)
        health_pb2_grpc.add_HealthServicer_to_server(Health(), server)
        agent_pb2_grpc.add_AgentServicer_to_server(Agent(), server)

        server.add_insecure_port(f'[::]:{consul_config_dict["grpc"]}')
        server.start()
        print(f"gRPC server started on port {consul_config_dict["grpc"]}.")

        c = consul.Consul(host=consul_config_dict["host"], port=consul_config_dict["port"])

        # 尝试注册服务到Consul
        c.agent.service.register(
            "agent",
            service_id="agent-1",
            address="172.17.0.1",
            port=consul_config_dict["grpc"],
            tags=["grpc"],
            check=consul.Check().grpc(f"172.17.0.1:{consul_config_dict["grpc"]}", interval="10s")  # 定义gRPC健康检查
        )
        print("Service registered with Consul.")

        server.wait_for_termination()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    serve()

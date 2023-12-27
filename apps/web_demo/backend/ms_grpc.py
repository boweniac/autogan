import threading
import consul
from concurrent import futures
import grpc
import queue

from apps.web_demo.backend.response.grpc import GrpcResponse

from apps.web_demo.backend.db.redis_storage import RedisStorage
from fastapi import HTTPException, FastAPI
from starlette import status

from apps.web_demo.backend.service.test_service import TestService
from grpcdata.grpc_py import agent_pb2_grpc, agent_pb2
from grpcdata.grpc_py import helloworld_pb2
from grpcdata.grpc_py import helloworld_pb2_grpc
from grpcdata.grpc_py import health_pb2
from grpcdata.grpc_py import health_pb2_grpc

app = FastAPI()
storage = RedisStorage("172.17.0.1", 60101, 0)
test_service = TestService("LLM_CONFIG", "off", True, storage)


class HelloWorld(helloworld_pb2_grpc.HelloWorldServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message=f'Hello, {request.name}')


class Health(health_pb2_grpc.HealthServicer):
    def Check(self, request, context):
        return health_pb2.HealthCheckResponse(status=health_pb2.HealthCheckResponse.SERVING)


class Agent(agent_pb2_grpc.AgentServicer):
    def ReceiveStream(self, request, context):
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
                test_thread = threading.Thread(target=test_service.receive, args=(conversation_id, conversation_id, "客户", content, stream_response))
                test_thread.start()
                while True:
                    while not data_queue.empty():
                        yield agent_pb2.ReceiveReply(text=data_queue.get())
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

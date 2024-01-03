import asyncio
import json
from fastapi import HTTPException, Query
from starlette import status

from apps.web_demo.backend.db.redis_storage import RedisStorage
from starlette.responses import StreamingResponse
from fastapi import FastAPI, WebSocket, Request

from apps.web_demo.backend.response.stream import StreamResponse
from apps.web_demo.backend.response.websocket import WebsocketResponse
from apps.web_demo.backend.service.test_service import TestService

app = FastAPI()
# data_queue = asyncio.Queue()
storage = RedisStorage("172.17.0.1", 60101, 0)
test_service = TestService("LLM_CONFIG", "off", True, storage)


@app.get("/add_conversation")
async def add_conversation(user_id: int = Query(None), conversation_id: int = Query(None)):
    try:
        if not user_id or not conversation_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User ID and Conversation ID must not be empty")

        err = storage.add_conversation(user_id, conversation_id)
        if err:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=err)
        else:
            return {"code": status.HTTP_200_OK, "data": "Conversation added successfully"}
    except HTTPException as e:
        return e
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/get_messages")
async def get_messages(user_id: int = Query(None), conversation_id: int = Query(None), last_msg_id: int = Query(None)):
    try:
        if not user_id or not conversation_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User ID and Conversation ID must not be empty")

        if storage.user_conversation_permissions(user_id, conversation_id):
            if last_msg_id and last_msg_id == storage.get_last_msg_id(conversation_id):
                return {"code": status.HTTP_200_OK, "data": None}
            else:
                return {"code": status.HTTP_200_OK, "data": storage.get_messages(conversation_id)}
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conversation permissions are wrong")
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/test")
async def stream_route(request: Request):
    try:
        data_queue = asyncio.Queue()
        data = await request.json()
        user_id = data["user_id"]
        conversation_id = data["conversation_id"]
        content = data["content"]

        if not user_id or not conversation_id or not content:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User ID, Conversation ID and Content must not be empty")

        if storage.user_conversation_permissions(user_id, conversation_id):
            stream_response = StreamResponse(data_queue)
            try:
                asyncio.create_task(
                    test_service.a_receive(conversation_id, conversation_id, "客户", content, stream_response))
                return StreamingResponse(stream_response.a_receive(), media_type="text/event-stream")
            except asyncio.CancelledError:
                stream_response.disconnected = True
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conversation permissions are wrong")
    except HTTPException as e:
        return e
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.websocket("/test")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            print("1")
            data = await websocket.receive_text()
            params = json.loads(data)  # 解析JSON格式的参数
            user_id = params.get('user_id')
            conversation_id = params.get('conversation_id')
            content = params.get('content')
            print(f"content: {content}")
            if not user_id or not conversation_id or not content:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="User ID, Conversation ID and Content must not be empty")

            if storage.user_conversation_permissions(user_id, conversation_id):
                # while True:
                websocket_response = WebsocketResponse(websocket)
                await test_service.a_receive(conversation_id, conversation_id, "客户", content, websocket_response)
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conversation permissions are wrong")
    except HTTPException as e:
        return e
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# 运行 Uvicorn 服务器
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=60207)
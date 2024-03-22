from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import socketio
import uvicorn

# Socket.IO 서버 인스턴스 생성
# CORS 문제를 방지하기 위해 모든 출처를 허용합니다. (운영 환경에서는 보안을 위해 이 설정을 제한하는 것이 좋습니다.)
# async_mode를 'asgi'로 설정하여 비동기 ASGI 애플리케이션과 호환되도록 합니다.
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')

# FastAPI 인스턴스 생성
app = FastAPI()

# Socket.IO 서버를 ASGI 애플리케이션으로 변환
socket_app = socketio.ASGIApp(sio)

# FastAPI 애플리케이션에 Socket.IO 서버를 마운트
# 이를 통해 FastAPI 경로는 일반 HTTP 요청을 처리하고, Socket.IO 경로는 웹소켓 연결을 처리할 수 있습니다.
app.mount("/", socket_app)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/favicon.ico", response_class=PlainTextResponse)
def favicon():
    return ""

# 연결 이벤트 핸들러
@sio.on("connect")
async def connect(sid, environ):
    print("Client connected", sid)

# 메시지 수신 이벤트 핸들러
@sio.on("message")
async def my_message(sid, data):
    print("Message from client:", data)
    await sio.emit('my_response', {'data': 'This is a response from server!'})

# 연결 해제 이벤트 핸들러
@sio.on("disconnect")
async def disconnect(sid):
    print("Client disconnected", sid)
    
if __name__=="__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=7777, lifespan="on", reload=True)
from fastapi import FastAPI
import numpy as np
import cv2
import json
import base64
import asyncio
import socket

app = FastAPI()

# 모델 불러오기
model = np.load_model()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(receive_frames())

async def receive_frames():
    # 소켓 생성 및 바인딩
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 8000))

    while True:
        # 데이터 수신
        data, address = sock.recvfrom(65507)
        json_data = json.loads(data.decode('utf-8'))

        # 프레임 복구
        buffer = base64.b64decode(json_data['frame'])
        frame = cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), cv2.IMREAD_COLOR)

        # 프레임 전처리
        processed_frame = preprocess_frame(frame)

        # 모델 예측
        prediction = model.predict(processed_frame)

        # 예측 결과 후처리
        processed_prediction = postprocess_prediction(prediction)

        # 결과 전송
        json_result = json.dumps(processed_prediction)
        sock.sendto(json_result.encode('utf-8'), address)

def preprocess_frame(frame):
    # 프레임 전처리 로직 구현
    # 예: 크기 조정, 정규화 등
    pass

def postprocess_prediction(prediction):
    # 예측 결과 후처리 로직 구현
    # 예: 클래스 레이블 매핑, 필터링 등
    pass
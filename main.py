from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from domain.viewer.router import router as viewer_router
from domain.map.router import router as map_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="자체감사 시스템", version="1.0")

# 1) CORS 설정: React 개발 서버에서 오는 요청 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 도메인으로 변경 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")            # 루트 경로
def read_root():
    return {"status": "ok"}
    
# 2) 단순 GET 엔드포인트
@app.get("/ping")
async def ping():
    return {"message": "pong"}

# 3) POST 데이터 수신 테스트용 엔드포인트
@app.post("/echo")
async def echo(request: Request):
    data = await request.json()
    print("받은 데이터:", data)             # 서버 콘솔에 로깅
    return {"you_sent": data}

@app.get("/api/health", summary="Health check", tags=["Health"])
async def health_check():
    """
    간단한 헬스체크 엔드포인트입니다.
    - status: 애플리케이션 상태 ("ok" 또는 "error")
    - uptime: 서버가 기동된 이후 경과 시간(초) — 필요시 추가 가능
    """
    return JSONResponse(content={"status": "ok"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


app.include_router(viewer_router, tags=["Viewer"])
app.include_router(map_router, tags=["Map"])
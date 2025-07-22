from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime

from domain.viewer.router import router as viewer_router
from domain.map.router import router as map_router

app = FastAPI(title="자체감사 시스템", version="1.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Accept-Ranges"],
)

# API 라우터 등록
app.include_router(viewer_router, prefix="/api/viewer", tags=["Viewer"])
app.include_router(map_router, prefix="/api/map", tags=["Map"])

# React 정적 빌드 파일 서빙
app.mount("/",
          StaticFiles(directory="frontend/FE/dist", html=False),
          name="frontend")


# 헬스체크 전용 엔드포인트
@app.get("/health", include_in_schema=False)
def healthcheck():
    return {"status": "OK", "timestamp": datetime.utcnow().isoformat() + "Z"}


@app.get("/")
def serve_root():
    print("Serving index.html")
    index_path = os.path.join("frontend/FE/dist", "index.html")
    return FileResponse(index_path)


# ✅ 정적 PDF 등
app.mount("/static", StaticFiles(directory="static"), name="static")


# PDF 다운로드 API
@app.get("/api/viewer/{uuid}/pdf", tags=["Viewer"])
async def get_viewer_pdf(uuid: str):
    file_path = f"static/pdfs/{uuid}.pdf"
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(file_path, media_type="application/pdf")


# 개발용 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

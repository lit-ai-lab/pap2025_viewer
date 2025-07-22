from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from domain.viewer.router import router as viewer_router
from domain.map.router import router as map_router

from datetime import datetime

app = FastAPI(title="자체감사 시스템", version="1.0")

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Accept-Ranges"],
)

# ✅ API 라우터 등록
app.include_router(viewer_router, tags=["Viewer"])
app.include_router(map_router, tags=["Map"])

# ✅ 프론트엔드 정적 빌드 파일 서빙
#app.mount("/app",
#StaticFiles(directory="frontend/FE/dist", html=True),
#name="frontend")

# ✅ 정적 PDF 등
app.mount("/static", StaticFiles(directory="static"), name="static")


# ✅ 헬스 체크 (배포용)
@app.get("/")
def root():
    return {"status": "healthy", "message": "API is running"}


# ✅ 별도 브라우저 진입점 리디렉션 (필요시)
@app.get("/redirect")
def redirect_to_frontend():
    return RedirectResponse(url="/app")


# ✅ 헬스 체크 전용 엔드포인트 (선택사항)
@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}


# ✅ PDF 파일 다운로드
@app.get("/api/viewer/{uuid}/pdf", tags=["Viewer"])
async def get_viewer_pdf(uuid: str):
    file_path = f"static/pdfs/{uuid}.pdf"
    try:
        return FileResponse(file_path, media_type="application/pdf")
    except:
        raise HTTPException(status_code=404, detail="PDF not found")


# ✅ 로컬 실행 (개발용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

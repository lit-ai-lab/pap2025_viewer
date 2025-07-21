from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from domain.viewer.router import router as viewer_router
from domain.map.router import router as map_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import HTTPException

app = FastAPI(title="자체감사 시스템", version="1.0")

# 1) CORS 설정: React 개발 서버에서 오는 요청 허용1
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 도메인으로 변경 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Accept-Ranges"],
)

app.mount(
    path="/static",
    app=StaticFiles(directory="static"),
    name="static",
)

@app.get("/")            # 루트 경로
def read_root():
    return {"status": "ok"}


@app.get("/api/viewer/{uuid}/pdf", tags=["Viewer"])
async def get_viewer_pdf(uuid: str):
    file_path = f"static/pdfs/{uuid}.pdf"
    try:
        return FileResponse(file_path, media_type="application/pdf")
    except Exception:
        raise HTTPException(status_code=404, detail="PDF not found")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


app.include_router(viewer_router, tags=["Viewer"])
app.include_router(map_router, tags=["Map"])
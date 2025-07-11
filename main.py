from fastapi import FastAPI
from domain.viewer.router import router as viewer_router
from domain.map.router import router as map_router

app = FastAPI(title="자체감사 시스템", version="1.0")

app.include_router(viewer_router, prefix="/viewer", tags=["Viewer"])
app.include_router(map_router, prefix="/maps", tags=["Map"])

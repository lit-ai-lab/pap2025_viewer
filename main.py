from fastapi import FastAPI
from .domain.map import router as map_router
from .domain.viewer import router as viewer_router
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gamsa Backend API")

app.include_router(map_router)
app.include_router(viewer_router)

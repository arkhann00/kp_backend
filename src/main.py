from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.db.init_db import init_db
from contextlib import asynccontextmanager

from src.api.routes.products import router as product_router
from src.api.routes.user import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.include_router(user_router)
    app.include_router(product_router)
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/", tags=["Health Check"])
async def health():
    return {"status": "ok", "message": "Marketplace API is running"}


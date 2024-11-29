# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from .db.database import engine, Base
from .db import models
from .db.crud import user_crud, tag_crud, location_crud, attraction_crud, attraction_tag_crud, attraction_review_crud
from .utils import auth_utils

app = FastAPI()
add_pagination(app)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 비동기 데이터베이스 테이블 생성 함수
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 앱 시작 시 테이블 생성
# @app.on_event("startup")
# async def on_startup():
#     await create_tables()

# 라우터 등록
app.include_router(user_crud.router)
app.include_router(tag_crud.router)
app.include_router(location_crud.router)
app.include_router(attraction_crud.router)
app.include_router(attraction_tag_crud.router)
app.include_router(attraction_review_crud.router)
app.include_router(auth_utils.router)

# 기본 경로 정의
@app.get("/")
async def root():
    return {
        "message": "Welcome to the FastAPI application!",
        "available_routes": {
            "users": "/users",
            "tags": "/tags",
            "locations": "/locations",
            "attractions": "/attractions",
            "attraction_tags": "/attraction_tags",
            "attraction_reviews": "/attraction_reviews",
            "auth_utils": "/auth",
        },
        "docs": "/docs",
        "redoc": "/redoc",
    }
# app/db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database
from aiomysql import create_pool

# MySQL DB Info
USERNAME = 'root'
PASSWORD = '0000'
HOST = '127.0.0.1'
PORT = '3306'
DBNAME = 'recommend'

# 데이터베이스 URL 설정 (필요에 따라 수정)
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# DATABASE_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'
DATABASE_URL = f'mysql+aiomysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'

# SQLAlchemy Base 클래스 생성
Base = declarative_base()

# 비동기 엔진과 세션 설정
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
# engine = create_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 비동기 데이터베이스 사용을 위한 Database 객체 생성
databse = Database(DATABASE_URL)

# 의존성 주입을 위한 세션 생성 함수
async def get_db():
    async with SessionLocal() as session:
        yield session
# app/utils/auth_utils.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from ..db.models import User
from ..db.schemas import LoginRequest
from ..db.database import get_db
from ..db.schemas import UserOut

import jwt
from datetime import datetime, timedelta, timezone
import pytz
# 한국 시간대 설정
KST = pytz.timezone('Asia/Seoul')
# 현재 UTC 시간을 한국 시간으로 변환
now_utc = datetime.now(timezone.utc)
now_kst = now_utc.astimezone(KST)

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

SALT_SIZE = 16
HASH_ALGORITHM = hashes.SHA256()
ITERATIONS = 100000
KEY_LENGTH = 32

def get_password_hash(password: str) -> str:
    salt = os.urandom(SALT_SIZE)
    kdf = PBKDF2HMAC(algorithm=HASH_ALGORITHM, length=KEY_LENGTH, salt=salt, iterations=ITERATIONS, backend=default_backend())
    key = kdf.derive(password.encode())
    return urlsafe_b64encode(salt + key).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    decoded_hash_password = urlsafe_b64decode(hashed_password.encode())
    salt = decoded_hash_password[:SALT_SIZE]
    key = decoded_hash_password[SALT_SIZE:]
    kdf = PBKDF2HMAC(algorithm=HASH_ALGORITHM, length=KEY_LENGTH, salt=salt, iterations=ITERATIONS, backend=default_backend())
    try:
        if key == kdf.derive(password.encode()):
            return True
        else:
            return False
    except ValueError:
        return False
    

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "ab#di*894[,!hwkemd6k0d@l$jc*:>k@bh)"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTS = 30

def create_access_token(data: dict, expires_delta: timedelta=None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = now_kst + expires_delta
    else:
        expire = now_kst + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTS)
    
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    user_name = payload.get("sub")
    print(user_name)

    if user_name is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},)

    return user_name

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    stmt = select(User).filter(User.user_name == login_request.user_name)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user or not verify_password(login_request.password, user.password):
        return {"access_token": None, "token_type": "bearer", "message": "Invalid credentials"}
    
    access_token = create_access_token(data={"sub": user.user_name})

    return {"access_token": access_token, "token_type": "bearer",
            "user_id": user.user_id, "user_name": user.user_name}

@router.get("/user/me", response_model=UserOut)
async def read_users_me(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    stmt = select(User).filter(User.user_name == current_user)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
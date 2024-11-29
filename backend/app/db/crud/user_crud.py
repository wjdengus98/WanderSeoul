# app/db/crud/user_crud.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from ..models import User
from ..schemas import UserCreate, UserOut
from ..database import get_db
from ...utils.auth_utils import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)

    db_user = User(**user.model_dump(exclude={'password'}), password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    stmt = select(User).filter(User.user_id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    stmt = select(User).filter(User.user_id == user_id)
    result = await db.execute(stmt)
    res_user = result.scalars().first()
    
    if not res_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 비밀번호가 제공된 경우 해시화
    if user.password:
        res_user.password = get_password_hash(user.password)

    for key, value in user.model_dump(exclude={'password'}).items():
        setattr(res_user, key, value)
    
    await db.commit()
    await db.refresh(res_user)

    return res_user

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    stmt = select(User).filter(User.user_id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        await db.delete(user)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    # 확인
    stmt = select(User).filter(User.user_id == user_id)
    result = await db.execute(stmt)
    deleted_user = result.scalars().first()
    
    if deleted_user:
        raise HTTPException(status_code=500, detail="Failed to delete User")

    return {'detail': 'User deleted successfully'}
# app/db/crud/tag_crud.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate, Params
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import select, func, literal
from ..models import Tag, AttractionTag
from ..schemas import TagCreate, TagOut
from ..database import get_db
from typing import List

router = APIRouter(prefix="/tags", tags=["tags"])

@router.post("/", response_model=TagOut)
async def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = Tag(**tag.model_dump())
    db.add(db_tag)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag

@router.get("/{tag_id}", response_model=TagOut)
async def read_tag(tag_id: int, db: Session = Depends(get_db)):
    stmt = select(Tag).filter(Tag.tag_id == tag_id)
    result = await db.execute(stmt)
    tag = result.scalars().first()
    
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.get("/", response_model=Page[TagOut])
async def read_tags(params: Params = Depends(), db: Session = Depends(get_db)):
    stmt1 = select(Tag.tag_id, Tag.tag_name).join(AttractionTag, AttractionTag.tag_id == Tag.tag_id, isouter=True)
    stmt2 = select(literal(0).label('tag_id'), literal('Etc.').label('tag_name'))
    union_stmt = stmt1.union_all(stmt2)
    stmt = select(union_stmt.c.tag_id, union_stmt.c.tag_name).group_by(union_stmt.c.tag_id, union_stmt.c.tag_name).order_by(func.count(union_stmt.c.tag_id).desc())
    
    result = await db.execute(stmt)
    tags = result.fetchall()

    if not tags:
        raise HTTPException(status_code=404, detail="No tags found")
    
    disable_installed_extensions_check()
    return paginate(list(tags), params)

@router.put("/{tag_id}", response_model=TagOut)
async def update_tag(tag_id: int, tag: TagCreate, db: Session = Depends(get_db)):
    stmt = select(Tag).filter(Tag.tag_id == tag_id)
    result = await db.execute(stmt)
    res_tag = result.scalars().first()
    
    if not res_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    for key, value in tag.model_dump().items():
        setattr(res_tag, key, value)
    
    await db.commit()
    await db.refresh(res_tag)

    return res_tag

@router.delete("/{tag_id}")
async def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    stmt = select(Tag).filter(Tag.tag_id == tag_id)
    result = await db.execute(stmt)
    tag = result.scalars().first()
    
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    try:
        await db.delete(tag)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    # 확인
    stmt = select(Tag).filter(Tag.tag_id == tag_id)
    result = await db.execute(stmt)
    deleted_tag = result.scalars().first()
    
    if deleted_tag:
        raise HTTPException(status_code=500, detail="Failed to delete Tag")

    return {'detail': 'Tag deleted successfully'}
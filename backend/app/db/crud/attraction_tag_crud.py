# app/db/crud/attraction_tag_crud.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from ..models import AttractionTag
from ..schemas import AttractionTagCreate, AttractionTagOut
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix="/attractionTags", tags=["attractionTags"])

@router.post("/", response_model=AttractionTagOut)
async def create_attraction_tag(attraction_tag: AttractionTagCreate, db: Session = Depends(get_db)):
    db_attraction_tag = AttractionTag(**attraction_tag.model_dump())
    db.add(db_attraction_tag)
    await db.commit()
    await db.refresh(db_attraction_tag)
    return db_attraction_tag

@router.get("/", response_model=List[AttractionTagOut])
async def read_attraction_tags(attr_tag_id: Optional[int], place_id: Optional[int], db: Session = Depends(get_db)):
    if attr_tag_id:
        stmt = select(AttractionTag).filter(AttractionTag.attr_tag_id == attr_tag_id)
    if place_id:
        stmt = select(AttractionTag).filter(AttractionTag.place_id == place_id)
    
    result = await db.execute(stmt)
    attraction_tag = result.scalars()
    
    if not attraction_tag:
        raise HTTPException(status_code=404, detail="AttractionTag not found")
    return attraction_tag

# @router.get("/by_place/{place_id}", response_model=List[AttractionTagOut])
# async def read_attraction_tags_by_place(place_id: int, db: Session = Depends(get_db)):
#     stmt = select(AttractionTag).filter(AttractionTag.place_id == place_id)
#     result = await db.execute(stmt)
#     attraction_tags = result.scalars()

#     if not attraction_tags:
#         raise HTTPException(status_code=404, detail="AttractionTag not found")
#     return attraction_tags

@router.put("/{attr_tag_id}", response_model=AttractionTagOut)
async def update_attraction_tags(attr_tag_id: int, attraction_tag: AttractionTagCreate, db: Session = Depends(get_db)):
    stmt = select(AttractionTag).filter(AttractionTag.attr_tag_id == attr_tag_id)
    result = await db.execute(stmt)
    res_attraction_tag = result.scalars().first()
    
    if not res_attraction_tag:
        raise HTTPException(status_code=404, detail="AttractionTag not found")
    
    for key, value in attraction_tag.model_dump().items():
        setattr(res_attraction_tag, key, value)
    
    await db.commit()
    await db.refresh(res_attraction_tag)

    return res_attraction_tag

@router.delete("/{attr_tag_id}")
async def delete_attraction_tags(attr_tag_id: int, db: Session = Depends(get_db)):
    stmt = select(AttractionTag).filter(AttractionTag.attr_tag_id == attr_tag_id)
    result = await db.execute(stmt)
    attraction_tag = result.scalars().first()
    
    if not attraction_tag:
        raise HTTPException(status_code=404, detail="AttractionTag not found")
    
    try:
        await db.delete(attraction_tag)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    # 확인
    stmt = select(AttractionTag).filter(AttractionTag.attr_tag_id == attr_tag_id)
    result = await db.execute(stmt)
    deleted_attraction_tag = result.scalars().first()
    
    if deleted_attraction_tag:
        raise HTTPException(status_code=500, detail="Failed to delete AttractionTag")

    return {'detail': 'AttractionTag deleted successfully'}
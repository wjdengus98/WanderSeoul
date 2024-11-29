# app/db/crud/location_crud.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from ..models import Location
from ..schemas import LocationCreate, LocationOut
from ..database import get_db

router = APIRouter(prefix="/locations", tags=["locations"])

@router.post("/", response_model=LocationOut)
async def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    db_location = Location(**location.model_dump())
    db.add(db_location)
    await db.commit()
    await db.refresh(db_location)
    return db_location

@router.get("/{location_id}", response_model=LocationOut)
async def read_location(location_id: int, db: Session = Depends(get_db)):
    stmt = select(Location).filter(Location.location_id == location_id)
    result = await db.execute(stmt)
    location = result.scalars().first()
    
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.put("/{location_id}", response_model=LocationOut)
async def update_location(location_id: int, location: LocationCreate, db: Session = Depends(get_db)):
    stmt = select(Location).filter(Location.location_id == location_id)
    result = await db.execute(stmt)
    res_location = result.scalars().first()
    
    if not res_location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    for key, value in location.model_dump().items():
        setattr(res_location, key, value)
    
    await db.commit()
    await db.refresh(res_location)

    return res_location

@router.delete("/{location_id}")
async def delete_location(location_id: int, db: Session = Depends(get_db)):
    stmt = select(Location).filter(Location.location_id == location_id)
    result = await db.execute(stmt)
    location = result.scalars().first()
    
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    try:
        await db.delete(location)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    # 확인
    stmt = select(Location).filter(Location.location_id == location_id)
    result = await db.execute(stmt)
    deleted_location = result.scalars().first()
    
    if deleted_location:
        raise HTTPException(status_code=500, detail="Failed to delete Location")

    return {'detail': 'Location deleted successfully'}
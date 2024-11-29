# app/db/crud/attraction_review_crud.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate, Params
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from ..models import AttractionReview, User
from ..schemas import AttractionReviewCreate, AttractionReviewOut
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix="/attractionReviews", tags=["attractionReviews"])

@router.post("/", response_model=AttractionReviewOut)
async def create_attraction_review(attraction_review: AttractionReviewCreate, db: Session = Depends(get_db)):
    db_attraction_review = AttractionReview(**attraction_review.model_dump())
    db.add(db_attraction_review)
    await db.commit()
    await db.refresh(db_attraction_review)
    return db_attraction_review

@router.get("/{review_id}", response_model=AttractionReviewOut)
async def read_attraction_review(review_id: int, db: Session = Depends(get_db)):
    stmt = select(AttractionReview).filter(AttractionReview.review_id == review_id)
    result = await db.execute(stmt)
    attraction_review = result.scalars().first()
    
    if not attraction_review:
        raise HTTPException(status_code=404, detail="AttractionReview not found")
    return attraction_review

@router.get("/place/{place_id}", response_model=Page[AttractionReviewOut])
async def read_attraction_reviews(place_id: int, params: Params = Depends(), db: Session = Depends(get_db)):
    stmt = select(AttractionReview, User.first_name) \
           .join(User, AttractionReview.user_id == User.user_id) \
           .filter(AttractionReview.place_id == place_id) \
           .order_by(AttractionReview.create_date.desc())
    
    result = await db.execute(stmt)
    attraction_reviews = result.all()
    
    if not attraction_reviews:
        raise HTTPException(status_code=404, detail="AttractionReview not found")
    
    response = [
        AttractionReviewOut(review_id=attraction_review.review_id, 
                            place_id=attraction_review.place_id, 
                            user_id=attraction_review.user_id, 
                            content=attraction_review.content, 
                            user_rating=attraction_review.user_rating, 
                            user_name=first_name,
                            create_date=attraction_review.create_date)
        for attraction_review, first_name in attraction_reviews
    ]
    return paginate(list(response), params)

@router.put("/{review_id}", response_model=AttractionReviewOut)
async def update_attraction_review(review_id: int, attraction_review: AttractionReviewCreate, db: Session = Depends(get_db)):
    stmt = select(AttractionReview).filter(AttractionReview.review_id == review_id)
    result = await db.execute(stmt)
    res_attraction_review = result.scalars().first()
    
    if not res_attraction_review:
        raise HTTPException(status_code=404, detail="AttractionReview not found")
    
    for key, value in attraction_review.model_dump().items():
        setattr(res_attraction_review, key, value)
    
    await db.commit()
    await db.refresh(res_attraction_review)

    return res_attraction_review

@router.delete("/{attr_tag_id}")
async def delete_attraction_review(review_id: int, db: Session = Depends(get_db)):
    stmt = select(AttractionReview).filter(AttractionReview.review_id == review_id)
    result = await db.execute(stmt)
    attraction_review = result.scalars().first()
    
    if not attraction_review:
        raise HTTPException(status_code=404, detail="AttractionReview not found")
    
    try:
        await db.delete(attraction_review)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    # 확인
    stmt = select(AttractionReview).filter(AttractionReview.review_id == review_id)
    result = await db.execute(stmt)
    deleted_attraction_review = result.scalars().first()
    
    if deleted_attraction_review:
        raise HTTPException(status_code=500, detail="Failed to delete AttractionReview")

    return {'detail': 'AttractionReview deleted successfully'}
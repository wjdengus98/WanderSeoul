# app/db/crud/attraction_crud.py
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, paginate, Params
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlalchemy import exists, func
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from ..models import Attraction, AttractionTag
from ..schemas import AttractionCreate, AttractionOut
from ..database import get_db
from typing import List
from ...utils.Word2VecRecommender import PrepWord2VecRecommender, Word2VecRecommender
from ...utils.BertSentenceRecommender import PrepBertSentenceRecommender, BertSentenceRecommender
from ...utils.AutorecWord2VecRecommender import AutorecWord2VecRecommender
from ...utils.auth_utils import get_current_user

router = APIRouter(prefix="/attractions", tags=["attractions"])

@router.post("/", response_model=AttractionOut)
async def create_attraction(attraction: AttractionCreate, db: Session = Depends(get_db)):
    db_attraction = Attraction(**attraction.model_dump())
    db.add(db_attraction)
    await db.commit()
    await db.refresh(db_attraction)
    return db_attraction

@router.get("/{place_id}", response_model=AttractionOut)
async def read_attraction(place_id: int, db: Session = Depends(get_db)):
    stmt = select(Attraction).filter(Attraction.place_id == place_id)
    result = await db.execute(stmt)
    attraction = result.scalars().first()
    
    if not attraction:
        raise HTTPException(status_code=404, detail="Attraction not found")
    return attraction

@router.get("/{place_id}/recommended", response_model=List[AttractionOut])
async def read_recommended_attractions(place_id: int, db: Session = Depends(get_db)):
    word2vec_recommender_prep = PrepWord2VecRecommender()
    word2vec_recommender = Word2VecRecommender(word2vec_recommender_prep.vectors, word2vec_recommender_prep.model_data_finally)
    recommended_place_ids = word2vec_recommender.get_recommended_attractions(place_id)
    
    attractions = []
    for place_id in recommended_place_ids:
        attraction = await read_attraction(place_id, db)
        attractions.append(attraction)
    
    return attractions

@router.get("/by_tags/", response_model=Page[AttractionOut])
async def read_attractions_by_tags(tags: List[int] = Query(..., description="List of tag IDs"), 
                                   params: Params = Depends(), 
                                   db: Session = Depends(get_db)):
    query_again = False

    if 0 in tags:
        stmt1 = select(Attraction).where(~exists(select(AttractionTag.place_id).where(AttractionTag.place_id == Attraction.place_id)))

        tags_without_0 = [tag for tag in tags if tag != 0]

        if tags_without_0:
            stmt2 = select(Attraction).join(AttractionTag, Attraction.place_id == AttractionTag.place_id).filter(AttractionTag.tag_id.in_(tags_without_0))
            stmt = stmt1.union_all(stmt2)
        else:
            stmt = stmt1
    else:
        stmt = select(Attraction).join(AttractionTag, Attraction.place_id == AttractionTag.place_id).filter(AttractionTag.tag_id.in_(tags))

    result = await db.execute(stmt)
    attractions = result.scalars().all()

    for attraction in attractions:
        if not isinstance(attraction, Attraction):
            query_again = True
            break
            
    if query_again:
        tags_again = [attraction for attraction in attractions]
        stmt = select(Attraction).filter(Attraction.place_id.in_(tags_again))
        
        result = await db.execute(stmt)
        attractions = result.scalars().all()
        # attractions = [AttractionOut.model_validate(attraction) for attraction in attractions]
    
    disable_installed_extensions_check()
    return paginate(list(attractions), params)

@router.get("/by_search/", response_model=List[AttractionOut])
async def read_attractions_by_search(search_query: str, db: Session = Depends(get_db)):
    bert_sentence_recommender_prep = PrepBertSentenceRecommender()
    bert_sentence_recommender = BertSentenceRecommender(bert_sentence_recommender_prep.model, bert_sentence_recommender_prep.model_data_finally, bert_sentence_recommender_prep.all_embeddings)
    recommended_place_ids = bert_sentence_recommender.recommend_places_by_sentence(search_query, top_n=10)
    
    attractions = []
    for place_id in recommended_place_ids:
        attraction = await read_attraction(place_id, db)
        attractions.append(attraction)
    
    return attractions

@router.get("/by_autorec/", response_model=List[AttractionOut])
async def read_attractions_by_autorec(user_name: str, db: Session = Depends(get_db)):
    # user_name = await get_current_user(access_token)
    autorec_word2vec_recommender = AutorecWord2VecRecommender()
    recommendations = autorec_word2vec_recommender.recommend_places(user_name, num_recommendations=4)

    attractions = []
    for place_id, _ in recommendations:
        attraction = await read_attraction(place_id, db)
        attractions.append(attraction)
    
    return attractions

@router.put("/{place_id}", response_model=AttractionOut)
async def update_attraction(place_id: int, attraction: AttractionCreate, db: Session = Depends(get_db)):
    stmt = select(Attraction).filter(Attraction.place_id == place_id)
    result = await db.execute(stmt)
    res_attraction = result.scalars().first()
    
    if not res_attraction:
        raise HTTPException(status_code=404, detail="Attraction not found")
    
    for key, value in attraction.model_dump().items():
        setattr(res_attraction, key, value)
    
    await db.commit()
    await db.refresh(res_attraction)

    return res_attraction

@router.delete("/{place_id}")
async def delete_attraction(place_id: int, db: Session = Depends(get_db)):
    stmt = select(Attraction).filter(Attraction.place_id == place_id)
    result = await db.execute(stmt)
    attraction = result.scalars().first()
    
    if not attraction:
        raise HTTPException(status_code=404, detail="Attraction not found")
    
    try:
        await db.delete(attraction)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    # 확인
    stmt = select(Attraction).filter(Attraction.place_id == place_id)
    result = await db.execute(stmt)
    deleted_attraction = result.scalars().first()
    
    if deleted_attraction:
        raise HTTPException(status_code=500, detail="Failed to delete Attraction")

    return {'detail': 'Attraction deleted successfully'}
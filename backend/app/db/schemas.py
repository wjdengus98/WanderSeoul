# app/db/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone

class UserBase(BaseModel):
    user_name: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    user_id: int
    create_date: Optional[datetime] = None
    last_login_date: Optional[datetime] = None

class TagBase(BaseModel):
    tag_name: str

class TagCreate(TagBase):
    pass

class TagOut(TagBase):
    tag_id: int
    update_date: Optional[datetime] = None
    updated_by: Optional[int] = None

class LocationBase(BaseModel):
    location_name: str

class LocationCreate(LocationBase):
    pass

class LocationOut(LocationBase):
    location_id: int
    update_date: Optional[datetime] = None
    updated_by: Optional[int] = None

class AttractionBase(BaseModel):
    place_name: str
    comm_score: Optional[float] = None
    cover_image_url: Optional[str] = None
    location_id: Optional[int] = None
    coordinate_type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    description: Optional[str] = None

class AttractionCreate(AttractionBase):
    pass

class AttractionOut(AttractionBase):
    place_id: int
    update_date: Optional[datetime] = None
    updated_by: Optional[int] = None

class AttractionTagBase(BaseModel):
    place_id: int
    tag_id: int

class AttractionTagCreate(AttractionTagBase):
    pass

class AttractionTagOut(AttractionTagBase):
    attr_tag_id: int
    update_date: Optional[datetime] = None
    updated_by: Optional[int] = None

class AttractionReviewBase(BaseModel):
    place_id: int
    user_id: int
    content: Optional[str] = None
    user_rating: Optional[float] = None

class AttractionReviewCreate(AttractionReviewBase):
    pass

class AttractionReviewOut(AttractionReviewBase):
    review_id: int
    user_name: Optional[str] = None
    create_date: Optional[datetime] = None

class LoginRequest(BaseModel):
    user_name: str
    password: str
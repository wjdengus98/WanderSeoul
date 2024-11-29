# app/db/models.py
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Text, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import pytz

Base = declarative_base()

# 한국 시간대 설정
KST = pytz.timezone('Asia/Seoul')
# 현재 UTC 시간을 한국 시간으로 변환
now_utc = datetime.now(timezone.utc)
now_kst = now_utc.astimezone(KST)

# User 모델 정의
class User(Base):
    __tablename__ = 'tbl_users'

    user_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True, index=True)
    user_name = Column(String(150), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(150))
    last_name = Column(String(150))
    email = Column(String(254))
    create_date = Column(DateTime, default=now_kst)
    last_login_date = Column(DateTime, default=now_kst)

# Tag 모델 정의
class Tag(Base):
    __tablename__ = 'tbl_tags'

    tag_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True, index=True)
    tag_name = Column(String(100), nullable=False)
    update_date = Column(DateTime, default=now_kst)
    updated_by = Column(Integer)

# Location 모델 정의
class Location(Base):
    __tablename__ = 'tbl_locations'

    location_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True, index=True)
    location_name = Column(String(100), nullable=False)
    update_date = Column(DateTime, default=now_kst)
    updated_by = Column(Integer)

# Attraction 모델 정의
class Attraction(Base):
    __tablename__ = 'tbl_attractions'

    place_id = Column(Integer, nullable=False, primary_key=True, index=True)
    place_name = Column(String(200), nullable=False)
    comm_score = Column(Float)
    cover_image_url = Column(String(200))
    location_id = Column(Integer, ForeignKey('tbl_locations.location_id'))
    coordinate_type = Column(String(10))
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String(300))
    description = Column(Text)
    update_date = Column(DateTime, default=now_kst)
    updated_by = Column(Integer)

# Attraction Tag 모델 정의
class AttractionTag(Base):
    __tablename__ = 'tbl_attraction_tags'

    attr_tag_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True, index=True)
    place_id = Column(Integer, ForeignKey('tbl_attractions.place_id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tbl_tags.tag_id'), nullable=False)
    update_date = Column(DateTime, default=now_kst)
    updated_by = Column(Integer)

# Attraction Review 모델 정의
class AttractionReview(Base):
    __tablename__ = 'tbl_attraction_reviews'

    review_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    place_id = Column(Integer, ForeignKey('tbl_attractions.place_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('tbl_users.user_id'), nullable=False)
    content = Column(Text)
    user_rating = Column(Float)
    create_date = Column(DateTime, default=now_kst)
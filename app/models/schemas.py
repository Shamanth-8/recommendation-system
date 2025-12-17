from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Assessment schemas
class QuestionBase(BaseModel):
    question_text: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None
    difficulty: DifficultyLevel

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int

    class Config:
        orm_mode = True

class AssessmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    difficulty: DifficultyLevel
    duration_minutes: int
    passing_score: float = Field(..., ge=0, le=100)

class AssessmentCreate(AssessmentBase):
    questions: List[QuestionCreate]

class AssessmentResponse(AssessmentBase):
    id: int
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    questions: List[QuestionResponse]

    class Config:
        orm_mode = True

class AssessmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    duration_minutes: Optional[int] = None
    passing_score: Optional[float] = None
    is_active: Optional[bool] = None

# User Assessment schemas
class UserAssessmentBase(BaseModel):
    user_id: int
    assessment_id: int
    score: float = Field(..., ge=0, le=100)
    responses: Optional[Dict[str, Any]] = None
    time_taken: Optional[int] = None  # in seconds

class UserAssessmentCreate(UserAssessmentBase):
    pass

class UserAssessmentResponse(UserAssessmentBase):
    id: int
    completed_at: datetime

    class Config:
        orm_mode = True

# Recommendation schemas
class RecommendationRequest(BaseModel):
    user_id: int
    assessment_id: int
    limit: int = Field(5, ge=1, le=10)

class RecommendationItem(BaseModel):
    assessment_id: int
    score: float
    reason: Optional[str] = None
    assessment: AssessmentResponse

class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]

# YouTube schemas
class YouTubeVideoBase(BaseModel):
    video_id: str
    title: str
    description: Optional[str] = None
    published_at: datetime
    channel_id: str
    channel_title: str
    thumbnail_url: Optional[str] = None
    duration: Optional[str] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class YouTubeVideoResponse(YouTubeVideoBase):
    class Config:
        orm_mode = True

class YouTubeSearchRequest(BaseModel):
    query: str
    max_results: int = Field(5, ge=1, le=25)
    category: Optional[str] = None

class YouTubeSearchResponse(BaseModel):
    videos: List[YouTubeVideoResponse]

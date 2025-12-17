from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    assessments = relationship("Assessment", back_populates="owner")

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, index=True, nullable=False)
    difficulty = Column(String, nullable=False)  # beginner, intermediate, advanced
    duration_minutes = Column(Integer, nullable=False)
    questions = Column(JSON, nullable=False)  # Store questions as JSON
    passing_score = Column(Float, nullable=False)  # Passing percentage
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    owner = relationship("User", back_populates="assessments")
    recommendations = relationship("Recommendation", back_populates="assessment")

class UserAssessment(Base):
    __tablename__ = "user_assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    score = Column(Float, nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    responses = Column(JSON, nullable=True)  # Store user responses
    time_taken = Column(Integer, nullable=True)  # Time taken in seconds

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    recommended_assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    score = Column(Float, nullable=False)  # Similarity score (0-1)
    reason = Column(Text, nullable=True)  # Why this recommendation was made
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    assessment = relationship("Assessment", foreign_keys=[assessment_id], back_populates="recommendations")
    recommended_assessment = relationship("Assessment", foreign_keys=[recommended_assessment_id])

class YouTubeVideo(Base):
    __tablename__ = "youtube_videos"

    id = Column(String, primary_key=True)  # YouTube video ID
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=False)
    channel_id = Column(String, nullable=False)
    channel_title = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=True)
    duration = Column(String, nullable=True)  # ISO 8601 duration format
    view_count = Column(Integer, nullable=True)
    like_count = Column(Integer, nullable=True)
    category = Column(String, nullable=True)  # e.g., "Tutorial", "Lecture", "Interview"
    tags = Column(JSON, nullable=True)  # List of tags as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

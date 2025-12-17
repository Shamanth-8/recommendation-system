from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .models import models, database
from .models.schemas import UserCreate, UserLogin, AssessmentCreate, AssessmentResponse, RecommendationRequest, RecommendationResponse
from .services import user_service, assessment_service, recommendation_service
from .services.youtube_service import YouTubeService

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title=settings.PROJECT_NAME)

# CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Initialize YouTube Service
youtube_service = YouTubeService(api_key=settings.YOUTUBE_API_KEY)

# Include routers
from .routes import users, assessments, recommendations
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(assessments.router, prefix=settings.API_V1_STR, tags=["assessments"])
app.include_router(recommendations.router, prefix=settings.API_V1_STR, tags=["recommendations"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Assessment Recommendation Engine"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

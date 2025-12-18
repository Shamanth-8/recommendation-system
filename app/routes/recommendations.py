from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from ..services.youtube_service import YouTubeService
from ..models.schemas import YouTubeSearchRequest, YouTubeSearchResponse, YouTubeVideoResponse
from ..config import settings

router = APIRouter()

# Initialize service (in a real app, use dependency injection)
youtube_service = YouTubeService(api_key=settings.YOUTUBE_API_KEY)

@router.post("/search", response_model=YouTubeSearchResponse)
async def search_videos(request: YouTubeSearchRequest):
    """
    Search for videos based on a query.
    """
    try:
        results = youtube_service.search_videos(request.query, request.max_results)
        return {"videos": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", tags=["recommendations"])
async def get_recommendations():
    return {"message": "Recommendations endpoint"}

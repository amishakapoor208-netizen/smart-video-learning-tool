"""
Transcript API Routes

This module defines the API endpoints for transcript extraction operations.

Purpose:
- Expose transcript extraction functionality via REST API
- Handle request validation and error responses
- Provide clean, intuitive API endpoints

Endpoints:
- POST /api/extract-transcript: Extract transcript from YouTube video
"""

from fastapi import APIRouter, HTTPException, status
from ..schemas.transcript_schema import TranscriptRequest, TranscriptResponse, ErrorResponse
from ..services.transcript_service import TranscriptService
from ..utils.youtube_utils import is_valid_youtube_url


# Create router for transcript endpoints
# prefix="/api" is added in main.py when including this router
router = APIRouter(
    prefix="/transcript",
    tags=["Transcript Extraction"],
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Server error"},
    }
)


@router.post(
    "/extract",
    response_model=TranscriptResponse,
    summary="Extract YouTube Video Transcript",
    description="Extract the complete transcript from a YouTube video",
    responses={
        200: {
            "description": "Transcript extracted successfully",
            "model": TranscriptResponse
        },
        400: {
            "description": "Invalid YouTube URL",
            "model": ErrorResponse
        },
        422: {
            "description": "Transcript unavailable for this video",
            "model": ErrorResponse
        }
    }
)
async def extract_transcript(request: TranscriptRequest):
    """
    Extract transcript from a YouTube video.
    
    This endpoint:
    1. Validates the YouTube URL
    2. Extracts the video ID
    3. Fetches the transcript using YouTube Transcript API
    4. Returns the clean transcript text
    
    Request Body:
        {
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
    
    Success Response (200):
        {
            "video_id": "dQw4w9WgXcQ",
            "transcript": "In this video we will learn about..."
        }
    
    Error Response (400 - Invalid URL):
        {
            "error": "Invalid YouTube URL",
            "detail": "Could not extract video ID from provided URL"
        }
    
    Error Response (422 - Transcript Unavailable):
        {
            "error": "Transcripts are disabled for this video",
            "detail": "The video creator has turned off the transcript feature."
        }
    
    Args:
        request (TranscriptRequest): Request containing YouTube URL
        
    Returns:
        TranscriptResponse: Video ID and extracted transcript
        
    Raises:
        HTTPException: If URL is invalid or transcript cannot be extracted
    """
    
    # Step 1: Validate YouTube URL
    is_valid, video_id = is_valid_youtube_url(request.youtube_url)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Invalid YouTube URL",
                "detail": "Please provide a valid YouTube URL. "
                         "Supported formats: youtube.com/watch?v=..., youtu.be/..., "
                         "youtube.com/embed/..."
            }
        )
    
    # Step 2: Extract transcript using TranscriptService
    success, transcript, error = TranscriptService.extract_transcript(video_id)
    
    # Step 3: Handle extraction errors
    if not success:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "Transcript Extraction Failed",
                "detail": error
            }
        )
    
    # Step 4: Return successful response
    return TranscriptResponse(
        video_id=video_id,
        transcript=transcript
    )


@router.get(
    "/health",
    summary="Transcript Service Health Check",
    description="Check if the transcript service is operational"
)
async def transcript_service_health():
    """
    Health check endpoint for the transcript service.
    
    This endpoint can be used to verify that the transcript service
    is running and operational.
    
    Returns:
        dict: Status and service information
        
    Example Response:
        {
            "status": "healthy",
            "service": "transcript_extraction",
            "message": "Transcript extraction service is operational"
        }
    """
    return {
        "status": "healthy",
        "service": "transcript_extraction",
        "message": "Transcript extraction service is operational"
    }

"""
Video Processing API Routes

This module defines the API endpoints for complete video processing operations.

Purpose:
- Expose video processing functionality via REST API
- Orchestrate transcript extraction and AI content generation
- Handle request validation and error responses
- Provide clean, intuitive API endpoints

Endpoints:
- POST /api/process-video: Process video and generate learning package
"""

from fastapi import APIRouter, HTTPException, status
from ..schemas.video_schema import ProcessVideoRequest, ProcessVideoResponse, ErrorResponse
from ..services.transcript_service import TranscriptService
from ..services.ai_service import AIService
from ..utils.youtube_utils import is_valid_youtube_url


# Create router for video processing endpoints
router = APIRouter(
    prefix="/video",
    tags=["Video Processing"],
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        422: {"model": ErrorResponse, "description": "Processing error"},
        500: {"model": ErrorResponse, "description": "Server error"},
    }
)

# Initialize services
transcript_service = TranscriptService()
ai_service = AIService()


@router.post(
    "/process",
    response_model=ProcessVideoResponse,
    summary="Process Video & Generate Learning Package",
    description="Extract transcript and generate summary, key points, and quiz from YouTube video",
    responses={
        200: {
            "description": "Video processed successfully",
            "model": ProcessVideoResponse
        },
        400: {
            "description": "Invalid YouTube URL",
            "model": ErrorResponse
        },
        422: {
            "description": "Processing error (transcript or AI generation failed)",
            "model": ErrorResponse
        }
    }
)
async def process_video(request: ProcessVideoRequest):
    """
    Process a YouTube video and generate a complete learning package.
    
    This endpoint performs the following steps:
    
    1. VALIDATE URL: Check if the YouTube URL is valid
    2. EXTRACT TRANSCRIPT: Fetch transcript from YouTube
    3. GENERATE SUMMARY: Create concise, exam-focused summary
    4. GENERATE KEY POINTS: Extract 5-7 core learning concepts
    5. GENERATE QUIZ: Create exactly 10 multiple-choice questions
    6. ASSEMBLE PACKAGE: Return complete learning package
    
    Request Body:
        {
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
    
    Success Response (200):
        {
            "video_id": "dQw4w9WgXcQ",
            "transcript": "Complete transcript text...",
            "summary": "Concise summary...",
            "key_points": ["Point 1", "Point 2", ...],
            "quiz": [
                {
                    "question": "Question?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A"
                },
                ... (exactly 10 questions)
            ]
        }
    
    Error Response (400 - Invalid URL):
        {
            "error": "Invalid YouTube URL",
            "detail": "Could not extract video ID from provided URL"
        }
    
    Error Response (422 - Processing Failed):
        {
            "error": "Transcript Extraction Failed",
            "detail": "Transcripts are disabled for this video"
        }
    
    Args:
        request (ProcessVideoRequest): Request containing YouTube URL
        
    Returns:
        ProcessVideoResponse: Complete learning package
        
    Raises:
        HTTPException: If URL is invalid or processing fails
    """
    
    # ===== STEP 1: VALIDATE YOUTUBE URL =====
    is_valid, video_id = is_valid_youtube_url(request.youtube_url)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Invalid YouTube URL",
                "detail": "Please provide a valid YouTube URL. "
                         "Supported formats: youtube.com/watch?v=..., youtu.be/..."
            }
        )
    
    # ===== STEP 2: EXTRACT TRANSCRIPT =====
    transcript_success, transcript, transcript_error = (
        transcript_service.extract_transcript(video_id)
    )
    
    if not transcript_success:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "Transcript Extraction Failed",
                "detail": transcript_error
            }
        )
    
    # ===== STEP 3: GENERATE LEARNING PACKAGE WITH AI =====
    ai_success, learning_package, ai_error = (
        ai_service.generate_learning_package(transcript)
    )
    
    if not ai_success:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "Content Generation Failed",
                "detail": ai_error
            }
        )
    
    # ===== STEP 4: ASSEMBLE COMPLETE RESPONSE =====
    response = ProcessVideoResponse(
        video_id=video_id,
        transcript=transcript,
        summary=learning_package["summary"],
        key_points=learning_package["key_points"],
        quiz=learning_package["quiz"]
    )
    
    return response


@router.get(
    "/health",
    summary="Video Processing Service Health Check",
    description="Check if video processing service is operational"
)
async def video_service_health():
    """
    Health check endpoint for the video processing service.
    
    Verifies that both transcript and AI services are operational.
    
    Returns:
        dict: Status and service information
        
    Example Response:
        {
            "status": "healthy",
            "service": "video_processing",
            "components": {
                "transcript_extraction": "operational",
                "ai_generation": "operational"
            }
        }
    """
    
    # Check if AI service can be initialized (checks for API key)
    try:
        AIService()
        ai_status = "operational"
    except ValueError:
        ai_status = "not_configured"
    
    return {
        "status": "healthy",
        "service": "video_processing",
        "components": {
            "transcript_extraction": "operational",
            "ai_generation": ai_status
        }
    }

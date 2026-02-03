"""
Transcript Schema Definitions

This module contains Pydantic models for request and response validation
related to YouTube transcript extraction functionality.

Purpose:
- Validate incoming API requests
- Ensure consistent response format
- Provide automatic API documentation
- Enable type hints for better code clarity
"""

from pydantic import BaseModel, Field, HttpUrl


class TranscriptRequest(BaseModel):
    """
    Request schema for transcript extraction endpoint.
    
    Validates that the user provides a valid YouTube URL.
    
    Attributes:
        youtube_url (str): The YouTube video URL to extract transcript from
        
    Example:
        {
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
    """
    youtube_url: str = Field(
        ...,
        description="YouTube URL of the video to extract transcript from",
        example="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )


class TranscriptResponse(BaseModel):
    """
    Successful response schema for transcript extraction.
    
    Contains the extracted transcript and video metadata.
    
    Attributes:
        video_id (str): The unique YouTube video ID
        transcript (str): The complete transcript as plain text
        
    Example:
        {
            "video_id": "dQw4w9WgXcQ",
            "transcript": "In this video we will learn about..."
        }
    """
    video_id: str = Field(
        ...,
        description="YouTube video ID",
        example="dQw4w9WgXcQ"
    )
    transcript: str = Field(
        ...,
        description="Complete transcript text extracted from video"
    )


class ErrorResponse(BaseModel):
    """
    Error response schema.
    
    Returned when transcript extraction fails.
    
    Attributes:
        error (str): Descriptive error message
        detail (str, optional): Additional details about the error
        
    Example:
        {
            "error": "Invalid YouTube URL",
            "detail": "Could not extract video ID from provided URL"
        }
    """
    error: str = Field(
        ...,
        description="Error message"
    )
    detail: str = Field(
        default=None,
        description="Additional error details"
    )

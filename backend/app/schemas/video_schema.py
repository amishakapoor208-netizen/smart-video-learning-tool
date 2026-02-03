"""
Video Processing Schema Definitions

This module contains Pydantic models for request and response validation
related to video processing and AI content generation.

Purpose:
- Validate incoming video processing requests
- Structure AI-generated content for consistent responses
- Provide automatic API documentation
- Enable type hints for better code clarity
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ProcessVideoRequest(BaseModel):
    """
    Request schema for video processing endpoint.
    
    Validates that the user provides a valid YouTube URL.
    
    Attributes:
        youtube_url (str): The YouTube video URL to process
        
    Example:
        {
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
    """
    youtube_url: str = Field(
        ...,
        description="YouTube URL of the video to process",
        example="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )


class QuizQuestion(BaseModel):
    """
    Schema for a single multiple-choice question.
    
    Attributes:
        question (str): The question text
        options (list): Four multiple-choice options (A, B, C, D)
        correct_answer (str): The correct option (A, B, C, or D)
        
    Example:
        {
            "question": "What is photosynthesis?",
            "options": [
                "Process of turning light into energy",
                "Process of turning water into ice",
                "Process of dividing cells",
                "Process of breaking down proteins"
            ],
            "correct_answer": "A"
        }
    """
    question: str = Field(
        ...,
        description="The quiz question text"
    )
    options: List[str] = Field(
        ...,
        min_items=4,
        max_items=4,
        description="Four answer options in order (A, B, C, D)"
    )
    correct_answer: str = Field(
        ...,
        description="The correct answer (A, B, C, or D)"
    )


class ProcessVideoResponse(BaseModel):
    """
    Successful response schema for video processing.
    
    Contains the complete learning package generated from the video:
    - Summary: Concise overview of content
    - Key Points: 5-7 core learning concepts
    - Quiz: Exactly 10 multiple-choice questions
    
    Attributes:
        video_id (str): The YouTube video ID
        transcript (str): The extracted video transcript
        summary (str): AI-generated summary of content
        key_points (list): List of key learning points
        quiz (list): List of 10 quiz questions
        
    Example:
        {
            "video_id": "dQw4w9WgXcQ",
            "transcript": "In this video...",
            "summary": "This video discusses...",
            "key_points": ["Point 1", "Point 2", ...],
            "quiz": [
                {
                    "question": "...",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A"
                }
            ]
        }
    """
    video_id: str = Field(
        ...,
        description="YouTube video ID",
        example="dQw4w9WgXcQ"
    )
    transcript: str = Field(
        ...,
        description="Complete transcript extracted from video"
    )
    summary: str = Field(
        ...,
        description="Concise, exam-focused summary of video content"
    )
    key_points: List[str] = Field(
        ...,
        description="5-7 key learning points from the transcript"
    )
    quiz: List[QuizQuestion] = Field(
        ...,
        min_items=10,
        max_items=10,
        description="Exactly 10 multiple-choice questions"
    )


class ErrorResponse(BaseModel):
    """
    Error response schema.
    
    Returned when video processing fails.
    
    Attributes:
        error (str): Error message
        detail (str, optional): Additional error details
        
    Example:
        {
            "error": "Transcript Extraction Failed",
            "detail": "Transcripts are disabled for this video"
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

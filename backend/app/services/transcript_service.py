"""
Transcript Service

This module handles all YouTube transcript extraction operations.

Purpose:
- Fetch transcripts from YouTube using YouTube Transcript API
- Handle errors gracefully (unavailable transcripts, private videos, etc.)
- Convert transcript data into clean, usable format
- Provide reliable, production-ready transcript extraction

Why Separated as Service:
Transcript extraction is a core business logic operation that:
1. Depends on external API (YouTube Transcript API)
2. Requires error handling and retry logic
3. May be reused across multiple endpoints
4. Should be independently testable
5. Demonstrates clean architecture principles

Automation Value:
This service automates the manual process of:
- Visiting YouTube
- Finding the transcript button
- Copying transcript text
By making it a single API call, teachers save hours of manual work
for every video they want to use in their curriculum.
"""

from typing import Optional, Tuple
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


class TranscriptService:
    """
    Service for extracting transcripts from YouTube videos.
    
    This class handles all operations related to fetching and processing
    YouTube video transcripts using the YouTube Transcript API.
    
    Methods:
        extract_transcript(video_id): Extract transcript for a video
        get_available_languages(video_id): Get available transcript languages
    """
    
    @staticmethod
    def extract_transcript(video_id: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Extract transcript from a YouTube video.
        
        This method:
        1. Attempts to fetch transcript in English
        2. Falls back to auto-generated transcripts if manual unavailable
        3. Formats transcript as plain text
        4. Handles errors gracefully
        
        Error Cases Handled:
        - TranscriptDisabled: Video has disabled transcripts
        - VideoUnavailable: Video doesn't exist or is private
        - NoTranscriptFound: No transcript available in any language
        - Network errors: API connection issues
        
        Args:
            video_id (str): YouTube video ID (11 characters)
            
        Returns:
            Tuple[bool, Optional[str], Optional[str]]:
            - success (bool): True if transcript extracted successfully
            - transcript (str): Plain text transcript if successful
            - error (str): Error message if failed
            
        Example:
            >>> service = TranscriptService()
            >>> success, transcript, error = service.extract_transcript("dQw4w9WgXcQ")
            >>> if success:
            ...     print(f"Got {len(transcript)} characters")
            ... else:
            ...     print(f"Error: {error}")
        """
        
        try:
            # Try to get transcript in English first
            # prefer_manually_created=True means we try manual transcripts first
            # then fall back to auto-generated if needed
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=['en']
            )
            
        except YouTubeTranscriptApi.TranscriptsDisabled:
            # Transcript feature is disabled for this video
            error_msg = (
                "Transcripts are disabled for this video. "
                "The video creator has turned off the transcript feature."
            )
            return False, None, error_msg
            
        except YouTubeTranscriptApi.NoTranscriptFound:
            # No transcript available even with fallback
            error_msg = (
                "No transcript available for this video. "
                "Try a video with English captions enabled."
            )
            return False, None, error_msg
            
        except Exception as e:
            # Catch other errors (network, invalid video, etc.)
            error_msg = f"Failed to fetch transcript: {str(e)}"
            return False, None, error_msg
        
        try:
            # Convert transcript list to plain text
            # TextFormatter joins all transcript entries into a single string
            formatter = TextFormatter()
            transcript_text = formatter.format_transcript(transcript_list)
            
            return True, transcript_text, None
            
        except Exception as e:
            # Error during formatting
            error_msg = f"Failed to format transcript: {str(e)}"
            return False, None, error_msg
    
    @staticmethod
    def get_available_languages(video_id: str) -> Tuple[bool, list, Optional[str]]:
        """
        Get list of available transcript languages for a video.
        
        This is useful for debugging and understanding what languages
        are available for a particular video.
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            Tuple[bool, list, Optional[str]]:
            - success (bool): True if successful
            - languages (list): List of available language codes
            - error (str): Error message if failed
            
        Example:
            >>> success, langs, error = TranscriptService.get_available_languages("dQw4w9WgXcQ")
            >>> if success:
            ...     print(f"Available: {langs}")  # ['en', 'fr', 'es', etc.]
        """
        
        try:
            transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Get manually created transcript languages
            manual_languages = [
                lang.language_code 
                for lang in transcripts.manually_created_transcripts
            ]
            
            # Get auto-generated transcript languages
            auto_languages = [
                lang.language_code 
                for lang in transcripts.generated_transcripts
            ]
            
            # Combine both lists
            all_languages = manual_languages + auto_languages
            
            return True, all_languages, None
            
        except Exception as e:
            error_msg = f"Failed to list available languages: {str(e)}"
            return False, [], error_msg

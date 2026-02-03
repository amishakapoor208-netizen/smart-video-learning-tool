"""
YouTube URL Utilities

This module provides utility functions for handling YouTube URLs.

Purpose:
- Validate YouTube URLs
- Extract video IDs from various YouTube URL formats
- Provide clean, reusable utilities for URL operations

Why Separated as Utility:
This is separated as a utility because URL validation is a common,
reusable operation that may be needed in multiple places across the
application (routes, services, background tasks, etc.).
"""

import re
from typing import Optional, Tuple


def extract_video_id(youtube_url: str) -> Optional[str]:
    """
    Extract YouTube video ID from various YouTube URL formats.
    
    Supports multiple YouTube URL formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://youtube.com/watch?v=VIDEO_ID
    - youtube.com/watch?v=VIDEO_ID
    
    Args:
        youtube_url (str): The YouTube URL to extract ID from
        
    Returns:
        Optional[str]: Video ID if found, None otherwise
        
    Example:
        >>> extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        'dQw4w9WgXcQ'
        
        >>> extract_video_id("https://youtu.be/dQw4w9WgXcQ")
        'dQw4w9WgXcQ'
        
        >>> extract_video_id("invalid url")
        None
    """
    
    # Pattern 1: youtube.com/watch?v=VIDEO_ID
    pattern1 = r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})'
    match = re.search(pattern1, youtube_url)
    if match:
        return match.group(1)
    
    # Pattern 2: youtu.be/VIDEO_ID
    pattern2 = r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})'
    match = re.search(pattern2, youtube_url)
    if match:
        return match.group(1)
    
    # Pattern 3: youtube.com/embed/VIDEO_ID
    pattern3 = r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})'
    match = re.search(pattern3, youtube_url)
    if match:
        return match.group(1)
    
    # No match found
    return None


def is_valid_youtube_url(youtube_url: str) -> Tuple[bool, Optional[str]]:
    """
    Validate if a URL is a valid YouTube URL and extract video ID.
    
    This function performs two checks:
    1. Checks if URL contains youtube or youtu.be domain
    2. Attempts to extract a valid video ID
    
    Args:
        youtube_url (str): The URL to validate
        
    Returns:
        Tuple[bool, Optional[str]]: (is_valid, video_id)
        - is_valid: True if URL is valid YouTube URL
        - video_id: Extracted video ID if valid, None otherwise
        
    Example:
        >>> is_valid_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        (True, 'dQw4w9WgXcQ')
        
        >>> is_valid_youtube_url("https://example.com")
        (False, None)
    """
    
    # Check if URL contains YouTube domain
    if not ('youtube.com' in youtube_url or 'youtu.be' in youtube_url):
        return False, None
    
    # Try to extract video ID
    video_id = extract_video_id(youtube_url)
    
    if video_id:
        return True, video_id
    else:
        return False, None

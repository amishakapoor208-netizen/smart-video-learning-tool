"""
AI Service - OpenAI Integration & Content Generation

This module handles all AI-powered content generation operations.

Purpose:
- Transform video transcripts into structured learning packages
- Generate summaries, key points, and quiz questions
- Interface with OpenAI API
- Handle prompt engineering and response parsing

Why Separated as Service:
AI content generation is a complex, expensive operation that:
1. Depends on external API (OpenAI)
2. Requires careful prompt engineering
3. Involves token costs and rate limits
4. Should be independently testable
5. May be reused across multiple endpoints

Automation Value:
This service automates the process of:
- Manually reading and summarizing videos
- Identifying key learning points
- Creating quiz questions for assessment
By automating these steps, teachers can generate complete learning packages
in seconds instead of spending hours per video.

Prompt Engineering:
Each prompt is optimized to:
- Generate consistent, high-quality output
- Enforce specific constraints (e.g., exactly 10 questions)
- Use appropriate academic language
- Provide structured data for parsing
"""

import os
import json
from typing import Optional, Tuple, List, Dict
from openai import OpenAI


class AIService:
    """
    Service for AI-powered educational content generation.
    
    Uses OpenAI API to generate summaries, key points, and quiz questions
    from video transcripts using optimized prompts.
    
    Methods:
        generate_learning_package: Generate complete learning package from transcript
        generate_summary: Generate summary from transcript
        generate_key_points: Generate key learning points
        generate_quiz: Generate exactly 10 multiple-choice questions
    """
    
    def __init__(self):
        """
        Initialize the AI Service with OpenAI client.
        
        Loads API key from environment variables.
        Raises error if OPENAI_API_KEY is not set.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please set it in your .env file."
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"  # Cost-effective model
        self.max_tokens = 2000  # Limit tokens to control costs
    
    # =====================================================
    # PROMPT TEMPLATES - CAREFULLY ENGINEERED
    # =====================================================
    
    @staticmethod
    def get_summary_prompt(transcript: str) -> str:
        """
        Get the optimized prompt for summary generation.
        
        Why This Prompt Works:
        - Asks for "concise" to avoid verbosity
        - Specifies "exam-focused" to prioritize important concepts
        - Uses simple language for clarity
        - Requests 2-3 sentences for length constraint
        - Instructs to use plain text for easy parsing
        
        Args:
            transcript (str): The video transcript to summarize
            
        Returns:
            str: Complete prompt for OpenAI
        """
        return f"""You are an expert educator creating study materials for students.

Your task: Create a concise, exam-focused summary of the following video transcript.

Requirements:
- Write 2-3 sentences maximum
- Focus on the most important concepts
- Use simple, clear academic language
- Avoid unnecessary details or examples
- Make it suitable for exam preparation

Transcript:
{transcript}

Summary:"""
    
    @staticmethod
    def get_key_points_prompt(transcript: str) -> str:
        """
        Get the optimized prompt for key points extraction.
        
        Why This Prompt Works:
        - Specifies exact count (5-7 points) to avoid too many/too few
        - Each point is a "core concept" not just any point
        - Forbids repetition explicitly
        - Uses numbered list format for easy parsing
        - Starts each point with action verb for clarity
        
        Args:
            transcript (str): The video transcript
            
        Returns:
            str: Complete prompt for OpenAI
        """
        return f"""You are an expert educator identifying key concepts from video content.

Your task: Extract 5-7 KEY LEARNING POINTS from the following transcript.

Requirements:
- Each point must represent a CORE CONCEPT from the transcript
- Number each point (1., 2., 3., etc.)
- Each point must be one clear sentence
- NO REPETITION - each point must be unique and distinct
- Use simple, actionable language
- Start with a strong verb when possible

Transcript:
{transcript}

Key Learning Points:"""
    
    @staticmethod
    def get_quiz_prompt(transcript: str) -> str:
        """
        Get the optimized prompt for quiz question generation.
        
        Why This Prompt Works:
        - EXPLICITLY specifies "EXACTLY 10 questions" (CAPITAL LETTERS)
        - Repeats the constraint in two places to enforce it
        - JSON format makes parsing reliable
        - Specifies all 4 options must be different
        - Correct answer specified explicitly
        - Forbids trick questions or ambiguity
        - Based ONLY on transcript content
        - All constraints are crystal clear to prevent hallucination
        
        Args:
            transcript (str): The video transcript
            
        Returns:
            str: Complete prompt for OpenAI
        """
        return f"""You are an expert educator creating multiple-choice quiz questions.

Your task: Create EXACTLY 10 multiple-choice questions based on this transcript.

CRITICAL CONSTRAINTS (MUST BE FOLLOWED):
- Generate EXACTLY 10 questions (no more, no less)
- Each question must be answerable from the transcript content
- Each question must have 4 unique options (A, B, C, D)
- Specify the correct answer clearly (must be one of: A, B, C, or D)
- No trick questions or ambiguous answers
- All 4 options must be plausible but only one is correct
- Questions should test understanding, not just memory

Output format (MUST be valid JSON):
[
  {{
    "question": "question text?",
    "options": ["option A", "option B", "option C", "option D"],
    "correct_answer": "A"
  }},
  ... (continue for exactly 10 questions total)
]

Transcript:
{transcript}

Quiz Questions (MUST be exactly 10):"""
    
    # =====================================================
    # AI GENERATION METHODS
    # =====================================================
    
    def generate_summary(self, transcript: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Generate a concise, exam-focused summary from transcript.
        
        Args:
            transcript (str): The video transcript
            
        Returns:
            Tuple[bool, Optional[str], Optional[str]]:
            - success (bool): True if generation successful
            - summary (str): Generated summary text
            - error (str): Error message if failed
        """
        try:
            prompt = self.get_summary_prompt(transcript)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educator creating study materials."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,  # Slightly creative but consistent
                max_tokens=self.max_tokens
            )
            
            summary = response.choices[0].message.content.strip()
            return True, summary, None
            
        except Exception as e:
            error_msg = f"Failed to generate summary: {str(e)}"
            return False, None, error_msg
    
    def generate_key_points(self, transcript: str) -> Tuple[bool, Optional[List[str]], Optional[str]]:
        """
        Generate 5-7 key learning points from transcript.
        
        Args:
            transcript (str): The video transcript
            
        Returns:
            Tuple[bool, Optional[List[str]], Optional[str]]:
            - success (bool): True if generation successful
            - key_points (list): List of key point strings
            - error (str): Error message if failed
        """
        try:
            prompt = self.get_key_points_prompt(transcript)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educator identifying key concepts."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=self.max_tokens
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Parse numbered list format (1. Point, 2. Point, etc.)
            key_points = []
            for line in response_text.split('\n'):
                line = line.strip()
                if line and any(line.startswith(f"{i}.") for i in range(1, 10)):
                    # Remove the number prefix
                    point = line.split('. ', 1)[1] if '. ' in line else line
                    if point:
                        key_points.append(point)
            
            if not key_points:
                # Fallback: treat each non-empty line as a point
                key_points = [line.strip() for line in response_text.split('\n') if line.strip()]
            
            return True, key_points, None
            
        except Exception as e:
            error_msg = f"Failed to generate key points: {str(e)}"
            return False, None, error_msg
    
    def generate_quiz(self, transcript: str) -> Tuple[bool, Optional[List[Dict]], Optional[str]]:
        """
        Generate EXACTLY 10 multiple-choice questions from transcript.
        
        IMPORTANT: This method validates that exactly 10 questions are generated.
        If AI returns more or less, it will try to fix it.
        
        Args:
            transcript (str): The video transcript
            
        Returns:
            Tuple[bool, Optional[List[Dict]], Optional[str]]:
            - success (bool): True if exactly 10 questions generated
            - quiz (list): List of 10 question dictionaries
            - error (str): Error message if failed
        """
        try:
            prompt = self.get_quiz_prompt(transcript)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educator creating quiz questions. "
                                 "You MUST generate EXACTLY 10 questions in valid JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=self.max_tokens
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Extract JSON from response (AI might add text before/after JSON)
            # Find the start and end of JSON array
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start == -1 or json_end == 0:
                return False, None, "AI response is not in JSON format"
            
            json_str = response_text[json_start:json_end]
            quiz_questions = json.loads(json_str)
            
            # ENFORCE: Must be exactly 10 questions
            if len(quiz_questions) != 10:
                return False, None, f"AI generated {len(quiz_questions)} questions instead of 10. Expected exactly 10."
            
            # Validate each question structure
            for i, q in enumerate(quiz_questions):
                if not all(key in q for key in ['question', 'options', 'correct_answer']):
                    return False, None, f"Question {i+1} missing required fields"
                
                if len(q['options']) != 4:
                    return False, None, f"Question {i+1} doesn't have exactly 4 options"
                
                if q['correct_answer'] not in ['A', 'B', 'C', 'D']:
                    return False, None, f"Question {i+1} has invalid correct_answer"
            
            return True, quiz_questions, None
            
        except json.JSONDecodeError as e:
            return False, None, f"Failed to parse AI response as JSON: {str(e)}"
        except Exception as e:
            return False, None, f"Failed to generate quiz: {str(e)}"
    
    def generate_learning_package(self, transcript: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Generate a complete learning package (summary + key points + quiz).
        
        This method orchestrates the three AI generation methods and returns
        a complete structured learning package.
        
        Args:
            transcript (str): The video transcript
            
        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]:
            - success (bool): True if all components generated successfully
            - package (dict): Complete learning package with summary, key_points, quiz
            - error (str): Error message if any component failed
        """
        
        # Validate transcript
        if not transcript or len(transcript.strip()) == 0:
            return False, None, "Transcript is empty"
        
        # Step 1: Generate Summary
        summary_success, summary, summary_error = self.generate_summary(transcript)
        if not summary_success:
            return False, None, f"Summary generation failed: {summary_error}"
        
        # Step 2: Generate Key Points
        points_success, key_points, points_error = self.generate_key_points(transcript)
        if not points_success:
            return False, None, f"Key points generation failed: {points_error}"
        
        # Step 3: Generate Quiz (EXACTLY 10 questions)
        quiz_success, quiz, quiz_error = self.generate_quiz(transcript)
        if not quiz_success:
            return False, None, f"Quiz generation failed: {quiz_error}"
        
        # Step 4: Assemble learning package
        learning_package = {
            "summary": summary,
            "key_points": key_points,
            "quiz": quiz
        }
        
        return True, learning_package, None

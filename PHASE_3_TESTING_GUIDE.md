# PHASE 3 - Testing Guide
## YouTube Transcript Extraction API

---

## 🚀 QUICK START

### 1. Start the Backend Server

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 2. Test the API

#### Option A: Using Swagger UI (Easiest)

1. Open browser: `http://localhost:8000/docs`
2. Click on `POST /api/transcript/extract`
3. Click "Try it out"
4. Paste YouTube URL in `youtube_url` field:
   ```
   https://www.youtube.com/watch?v=jNQXAC9IVRw
   ```
5. Click "Execute"

**Expected Response**:
```json
{
  "video_id": "jNQXAC9IVRw",
  "transcript": "In this video I'll explain some of the..."
}
```

#### Option B: Using cURL

```bash
curl -X POST "http://localhost:8000/api/transcript/extract" \
  -H "Content-Type: application/json" \
  -d '{"youtube_url":"https://www.youtube.com/watch?v=jNQXAC9IVRw"}'
```

#### Option C: Using Python

```python
import requests

url = "http://localhost:8000/api/transcript/extract"
data = {"youtube_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw"}

response = requests.post(url, json=data)

if response.status_code == 200:
    result = response.json()
    print(f"Video ID: {result['video_id']}")
    print(f"Transcript: {result['transcript'][:200]}...")
else:
    error = response.json()
    print(f"Error: {error['error']}")
```

---

## 🧪 TEST CASES

### Test Case 1: Valid YouTube URL (Success)

**URL**: `https://www.youtube.com/watch?v=jNQXAC9IVRw`

**Expected**: 
- Status: 200
- Returns video_id and transcript

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/transcript/extract" \
  -H "Content-Type: application/json" \
  -d '{"youtube_url":"https://www.youtube.com/watch?v=jNQXAC9IVRw"}'
```

---

### Test Case 2: Invalid URL Format (Error 400)

**URL**: `https://example.com`

**Expected**:
- Status: 400
- Error: "Invalid YouTube URL"

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/transcript/extract" \
  -H "Content-Type: application/json" \
  -d '{"youtube_url":"https://example.com"}'
```

**Expected Response**:
```json
{
  "detail": {
    "error": "Invalid YouTube URL",
    "detail": "Please provide a valid YouTube URL. Supported formats..."
  }
}
```

---

### Test Case 3: Video with Disabled Transcript (Error 422)

**Note**: Use a real YouTube video ID that has disabled transcripts

**Expected**:
- Status: 422
- Error: "Transcripts are disabled for this video"

---

### Test Case 4: Different YouTube URL Format (Success)

**URL**: `https://youtu.be/jNQXAC9IVRw`

**Expected**: 
- Status: 200
- Returns transcript (youtu.be format should work)

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/transcript/extract" \
  -H "Content-Type: application/json" \
  -d '{"youtube_url":"https://youtu.be/jNQXAC9IVRw"}'
```

---

### Test Case 5: Health Check (Success)

**Endpoint**: `GET /api/transcript/health`

**Expected**:
```json
{
  "status": "healthy",
  "service": "transcript_extraction",
  "message": "Transcript extraction service is operational"
}
```

**cURL**:
```bash
curl "http://localhost:8000/api/transcript/health"
```

---

## 📊 API DOCUMENTATION

### Endpoint: POST /api/transcript/extract

**Description**: Extract transcript from a YouTube video

**Request**:
```json
{
  "youtube_url": "string (required)"
}
```

**Success Response (200)**:
```json
{
  "video_id": "string",
  "transcript": "string"
}
```

**Error Response (400 - Bad Request)**:
```json
{
  "detail": {
    "error": "Invalid YouTube URL",
    "detail": "..."
  }
}
```

**Error Response (422 - Unprocessable Entity)**:
```json
{
  "detail": {
    "error": "Transcript Extraction Failed",
    "detail": "..."
  }
}
```

---

## 🔍 AVAILABLE TEST VIDEOS

Here are some YouTube videos that support transcripts:

| Title | URL | Use Case |
|---|---|---|
| "Me at the zoo" | https://www.youtube.com/watch?v=jNQXAC9IVRw | First YouTube video |
| YouTube Rewind 2018 | https://www.youtube.com/watch?v=YQHsXMglC9A | Popular video |

**Note**: Always test with videos that have English captions enabled.

---

## ✅ AUTOMATED TESTING

### Unit Tests (To be implemented)

```python
import pytest
from app.utils.youtube_utils import extract_video_id, is_valid_youtube_url
from app.services.transcript_service import TranscriptService

def test_extract_video_id_standard_url():
    """Test extracting video ID from standard YouTube URL"""
    result = extract_video_id("https://www.youtube.com/watch?v=jNQXAC9IVRw")
    assert result == "jNQXAC9IVRw"

def test_extract_video_id_short_url():
    """Test extracting video ID from shortened youtu.be URL"""
    result = extract_video_id("https://youtu.be/jNQXAC9IVRw")
    assert result == "jNQXAC9IVRw"

def test_extract_video_id_invalid():
    """Test that invalid URL returns None"""
    result = extract_video_id("https://example.com")
    assert result is None

def test_is_valid_youtube_url_valid():
    """Test validation of valid YouTube URL"""
    is_valid, video_id = is_valid_youtube_url("https://www.youtube.com/watch?v=jNQXAC9IVRw")
    assert is_valid is True
    assert video_id == "jNQXAC9IVRw"

def test_is_valid_youtube_url_invalid():
    """Test validation of invalid YouTube URL"""
    is_valid, video_id = is_valid_youtube_url("https://example.com")
    assert is_valid is False
    assert video_id is None

def test_extract_transcript_valid_video():
    """Test extracting transcript from valid video"""
    success, transcript, error = TranscriptService.extract_transcript("jNQXAC9IVRw")
    assert success is True
    assert transcript is not None
    assert len(transcript) > 0
    assert error is None
```

---

## 🐛 DEBUGGING TIPS

### Check Backend Logs

Watch terminal where you ran `uvicorn app.main:app --reload`:
- Look for incoming requests
- Check for error messages
- Verify transcript API responses

### Test YouTube Transcript API Directly

```python
from youtube_transcript_api import YouTubeTranscriptApi

try:
    transcript = YouTubeTranscriptApi.get_transcript("jNQXAC9IVRw")
    print(f"Success! Got {len(transcript)} entries")
except Exception as e:
    print(f"Error: {e}")
```

### Test URL Extraction

```python
from app.utils.youtube_utils import extract_video_id

test_urls = [
    "https://www.youtube.com/watch?v=jNQXAC9IVRw",
    "https://youtu.be/jNQXAC9IVRw",
    "youtube.com/watch?v=jNQXAC9IVRw",
]

for url in test_urls:
    video_id = extract_video_id(url)
    print(f"{url} → {video_id}")
```

---

## 📱 WHAT'S NEXT

### Phase 4 - AI Summary Generation

This phase's transcript API will be used:

```python
# In Phase 4
from app.services.transcript_service import TranscriptService
from openai import OpenAI

# Extract transcript
success, transcript, _ = TranscriptService.extract_transcript(video_id)

if success:
    # Generate summary using OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    summary = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"Summarize this: {transcript}"
        }]
    )
    return summary.choices[0].message.content
```

---

## 🎯 SUCCESS CRITERIA

**Phase 3 is complete when**:
- ✅ API extracts transcripts successfully
- ✅ URL validation works for all formats
- ✅ Error handling covers all edge cases
- ✅ Code is clean and well-documented
- ✅ Ready for Phase 4 integration

---

**Created**: February 2, 2026  
**Status**: Phase 3 Testing Guide

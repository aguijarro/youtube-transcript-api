import pytest
from unittest.mock import patch
from youtube_transcript_api import TranscriptsDisabled, NoTranscriptFound, YouTubeTranscriptApi

# Mock data for tests
MOCK_TRANSCRIPT = [
    {
        "text": "sample text",
        "start": 0.0,
        "duration": 1.0
    }
]

def test_get_transcript_success(test_app):
    """Test successful transcript retrieval"""
    video_id = "Tm_2RZm8JB8"
    
    with patch.object(YouTubeTranscriptApi, 'get_transcript') as mock_get:
        mock_get.return_value = MOCK_TRANSCRIPT
        response = test_app.get(f"/api/v1/transcript/{video_id}")
        
        assert response.status_code == 200
        assert response.json() == {"transcript": MOCK_TRANSCRIPT}

def test_get_transcript_invalid_video(test_app):
    """Test invalid video ID scenario"""
    video_id = "invalid_id"
    
    with patch.object(YouTubeTranscriptApi, 'get_transcript') as mock_get:
        # Create exception with proper arguments
        exception = NoTranscriptFound(
            video_id=video_id,
            requested_language_codes=["en"],
            transcript_data={}
        )
        mock_get.side_effect = exception
        
        response = test_app.get(f"/api/v1/transcript/{video_id}")
        
        assert response.status_code == 404
        assert "detail" in response.json()
        assert response.json()["detail"] == f"No transcript found for video {video_id}"

def test_get_transcript_no_captions(test_app):
    """Test video without captions scenario"""
    video_id = "video_without_captions"
    
    with patch.object(YouTubeTranscriptApi, 'get_transcript') as mock_get:
        mock_get.side_effect = TranscriptsDisabled(video_id)
        response = test_app.get(f"/api/v1/transcript/{video_id}")
        
        assert response.status_code == 404
        assert "detail" in response.json()
        assert response.json()["detail"] == f"Transcripts are disabled for video {video_id}"

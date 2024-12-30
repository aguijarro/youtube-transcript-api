import pytest
from unittest.mock import patch
from bson import ObjectId

# Mock data for tests
MOCK_STORED_TRANSCRIPTS = [
    {
        "_id": ObjectId("507f1f77bcf86cd799439011"),
        "video_id": "test_video_1",
        "url_endpoint": "http://test.com/api/v1/transcript/test_video_1",
        "response": {
            "transcript": [
                {"text": "test text 1", "start": 0.0, "duration": 1.0}
            ]
        },
        "created_at": "2024-01-01T00:00:00"
    },
    {
        "_id": ObjectId("507f1f77bcf86cd799439012"),
        "video_id": "test_video_2",
        "url_endpoint": "http://test.com/api/v1/transcript/test_video_2",
        "response": {
            "transcript": [
                {"text": "test text 2", "start": 1.0, "duration": 1.0}
            ]
        },
        "created_at": "2024-01-01T00:00:00"
    }
]

@pytest.mark.asyncio
async def test_get_all_transcripts_success(test_app):
    """Test successful retrieval of all stored transcripts"""
    with patch('app.repositories.transcript_repository.TranscriptRepository.get_all_transcript_requests') as mock_get:
        # Prepare mock data with converted _id to id
        mock_response = []
        for doc in MOCK_STORED_TRANSCRIPTS:
            doc_copy = doc.copy()
            doc_copy['id'] = str(doc_copy.pop('_id'))
            mock_response.append(doc_copy)
        
        mock_get.return_value = mock_response
        response = test_app.get("/api/v1/transcript/")
        
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["video_id"] == "test_video_1"
        assert response.json()[1]["video_id"] == "test_video_2"
        assert "id" in response.json()[0]
        assert "url_endpoint" in response.json()[0]
        assert "created_at" in response.json()[0]
        mock_get.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_transcripts_empty(test_app):
    """Test retrieval when no transcripts are stored"""
    with patch('app.repositories.transcript_repository.TranscriptRepository.get_all_transcript_requests') as mock_get:
        mock_get.return_value = []
        response = test_app.get("/api/v1/transcript/")
        
        assert response.status_code == 200
        assert response.json() == []
        mock_get.assert_called_once()

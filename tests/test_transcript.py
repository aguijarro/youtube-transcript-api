import pytest
from unittest.mock import patch
from bson import ObjectId
from fastapi.testclient import TestClient

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

@pytest.fixture
def mock_transcript_data():
    return {
        'video1': [
            {'text': 'Hello', 'start': 0.0, 'duration': 1.0},
            {'text': 'World', 'start': 1.0, 'duration': 1.0}
        ],
        'video2': [
            {'text': 'Test', 'start': 0.0, 'duration': 1.0},
            {'text': 'Video', 'start': 1.0, 'duration': 1.0}
        ]
    }

@pytest.mark.asyncio
async def test_get_multiple_transcripts(client: TestClient, mock_db, mock_transcript_data):
    # Mock the YouTubeTranscriptApi.get_transcripts method
    with patch('app.api.v1.endpoints.transcript.YouTubeTranscriptApi.get_transcripts') as mock_get_transcripts:
        # Set up the mock to return our test data
        mock_get_transcripts.return_value = (mock_transcript_data, {})
        
        # Test data
        test_payload = {
            "video_ids": ["video1", "video2"],
            "languages": ["en", "de"]
        }
        
        # Make the request
        response = client.post("/api/v1/transcript/batch", json=test_payload)
        
        # Assertions
        assert response.status_code == 200
        assert response.json() == {"transcripts": mock_transcript_data}
        
        # Verify the mock was called correctly
        mock_get_transcripts.assert_called_once_with(
            ["video1", "video2"],
            languages=["en", "de"]
        )

@pytest.mark.asyncio
async def test_get_multiple_transcripts_no_transcript(client: TestClient, mock_db):
    with patch('app.api.v1.endpoints.transcript.YouTubeTranscriptApi.get_transcripts') as mock_get_transcripts:
        mock_get_transcripts.side_effect = NoTranscriptFound()
        
        response = client.post("/api/v1/transcript/batch", 
                             json={"video_ids": ["invalid_id"], "languages": ["en"]})
        
        assert response.status_code == 404
        assert "No transcripts found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_multiple_transcripts_disabled(client: TestClient, mock_db):
    with patch('app.api.v1.endpoints.transcript.YouTubeTranscriptApi.get_transcripts') as mock_get_transcripts:
        mock_get_transcripts.side_effect = TranscriptsDisabled()
        
        response = client.post("/api/v1/transcript/batch", 
                             json={"video_ids": ["disabled_id"], "languages": ["en"]})
        
        assert response.status_code == 404
        assert "Transcripts are disabled" in response.json()["detail"]

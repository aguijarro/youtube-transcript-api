from fastapi import APIRouter, HTTPException, Depends, Request
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from typing import List, Dict, Union
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.mongodb import get_database
from app.services.transcript_service import TranscriptService
from app.schemas.transcript import TranscriptResponse

router = APIRouter()

@router.get("/{video_id}", response_model=Dict[str, List[Dict[str, Union[str, float]]]])
async def get_transcript(
    video_id: str,
    request: Request,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """
    Get transcript for a YouTube video and store the request
    
    Args:
        video_id: YouTube video ID
        request: FastAPI request object
        db: MongoDB database connection
        
    Returns:
        Dictionary containing transcript list with text, start time and duration
        
    Raises:
        404: If video not found or has no transcripts
        500: For other errors
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        response = {"transcript": transcript}
        
        # Store the request in the database with the URL
        transcript_service = TranscriptService(db)
        await transcript_service.store_transcript_request(
            video_id=video_id,
            url_endpoint=str(request.url),
            response=response
        )
        
        return response
        
    except NoTranscriptFound:
        raise HTTPException(
            status_code=404,
            detail=f"No transcript found for video {video_id}"
        )
    except TranscriptsDisabled:
        raise HTTPException(
            status_code=404,
            detail=f"Transcripts are disabled for video {video_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving transcript: {str(e)}"
        )

@router.get("/", response_model=List[TranscriptResponse])
async def get_all_transcripts(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """
    Get all stored transcript requests
    
    Args:
        db: MongoDB database connection
        
    Returns:
        List of all transcript requests with their responses
    """
    transcript_service = TranscriptService(db)
    return await transcript_service.get_all_transcripts()

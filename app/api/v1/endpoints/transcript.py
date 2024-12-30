from fastapi import APIRouter, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from typing import List, Dict, Union

router = APIRouter()

@router.get("/{video_id}", response_model=Dict[str, List[Dict[str, Union[str, float]]]])
async def get_transcript(video_id: str):
    """
    Get transcript for a YouTube video
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Dictionary containing transcript list with text, start time and duration
        
    Raises:
        404: If video not found or has no transcripts
        500: For other errors
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return {"transcript": transcript}
        
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

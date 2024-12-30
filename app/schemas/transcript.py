from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Union

class TranscriptRequest(BaseModel):
    video_id: str
    url_endpoint: str
    response: Dict[str, List[Dict[str, Union[str, float]]]]
    created_at: datetime = datetime.utcnow()

class TranscriptResponse(TranscriptRequest):
    id: str = Field(..., description="MongoDB document ID")

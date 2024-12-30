from typing import List
from app.repositories.transcript_repository import TranscriptRepository
from app.schemas.transcript import TranscriptRequest, TranscriptResponse
from motor.motor_asyncio import AsyncIOMotorClient

class TranscriptService:
    def __init__(self, db: AsyncIOMotorClient):
        self.repository = TranscriptRepository(db)

    async def store_transcript_request(self, video_id: str, url_endpoint: str, response: dict):
        transcript_request = TranscriptRequest(
            video_id=video_id,
            url_endpoint=url_endpoint,
            response=response
        )
        return await self.repository.create_transcript_request(transcript_request)

    async def get_all_transcripts(self) -> List[TranscriptResponse]:
        return await self.repository.get_all_transcript_requests()

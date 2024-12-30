from datetime import datetime
from typing import List
from app.schemas.transcript import TranscriptRequest, TranscriptResponse
from motor.motor_asyncio import AsyncIOMotorClient

class TranscriptRepository:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = self.db.transcripts

    async def create_transcript_request(self, transcript_request: TranscriptRequest):
        result = await self.collection.insert_one(transcript_request.model_dump())
        return result.inserted_id

    async def get_all_transcript_requests(self) -> List[TranscriptResponse]:
        cursor = self.collection.find({})
        transcripts = []
        async for doc in cursor:
            doc['id'] = str(doc.pop('_id'))  # Convert ObjectId to string
            transcripts.append(TranscriptResponse(**doc))
        return transcripts

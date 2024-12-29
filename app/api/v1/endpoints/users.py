from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.user import User, UserCreate
from app.services.user_service import get_users, create_user

router = APIRouter()

@router.get("/", response_model=List[User])
async def read_users():
    return await get_users()

@router.post("/", response_model=User)
async def create_new_user(user: UserCreate):
    return await create_user(user) 
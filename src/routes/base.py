from fastapi import FastAPI, APIRouter
import os
from helpers.config import get_settings

router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@router.get("/")
async def welcome():
    return {
        "message": "Welcome to the FastAPI application!"
    }

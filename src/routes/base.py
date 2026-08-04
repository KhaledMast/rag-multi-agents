from fastapi import FastAPI, APIRouter
import os
from helpers.config import get_settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome():
    return {
        "message": "Welcome to the FastAPI application!"
    }

from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

class options(str, Enum):
    check = "check"

app = FastAPI()

class request(BaseModel):
    text: str

class response(BaseModel):
    success: bool
    country: str
    keywords: list[str]
    found_on: int
    total_checked: int
    results: dict
    error: str | None

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Fact Checker API"    
    }

@app.post("/{options.check}/", response_model=response)
async def checker(req: request):
    return
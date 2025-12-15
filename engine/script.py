from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from core.verifier import Verifier

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

verifier = Verifier()

class Request(BaseModel):
    text: str

class Response(BaseModel):
    success: bool
    country: str
    keywords: list[str]
    found_on: int
    total_checked: int
    results: dict
    error: Optional[str] = None

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Fact Checker API"    
    }

@app.post("/check", response_model=Response)
async def checker(req: Request):
    try:
        if not req.text or len(req.text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Text must be at least 10 characters"
            )
        
        result = await verifier.verify(req.text)

        if "error" in result:
            return Response(
                success=False,
                country=result.get("country", ""),
                keywords=result.get("keywords", []),
                found_on=result.get("found_on", 0),
                total_checked=result.get("total_checked", 0),
                results=result.get("results", {}),
                error=result["error"]
            )

        return Response(
            success=True,
            country=result["country"],
            keywords=result["keywords"],
            found_on=result["found_on"],
            total_checked=result["total_checked"],
            results=result["results"],
            error=None
        )
    
    except HTTPException:
        raise
    except Exception as e:
        return Response(
            success=False,
            country="",
            keywords=[],
            found_on=0,
            total_checked=0,
            results={},
            error=str(e)
        )
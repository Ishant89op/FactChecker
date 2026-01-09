from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from dataclasses import dataclass, field

from core.verifier import Verifier
from core.verdict import verdict
from core.verifier import VerifierResult

from model.request import Request
from model.response import Response

from core2.playwright_launcher import launcher

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

verifier = Verifier()

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Fact Checker API" ,
        "google_search_M1": "This method searches on google. (/check_M1)",
        "direct_site_search_M2": "This method individually searches the sites.(/check_M2)"
    }

@app.post("/check_M1", response_model=Response)
async def google_search(req: Request):
    try:
        if not req.text or len(req.text.strip()) < 10:
            return Response(
                error = "Text must be at least 10 characters"
            )
        
        result: VerifierResult = await verifier.verify(req.text)

        if result.error is not None:
            return Response(
                error = result.error
            )

        found_on = result["found_on"]
        total_checked = result["total_checked"]
        overall_verdict = verdict(found_on, total_checked)

        return Response(
            success=True,
            country=result.country,
            keywords=result.keywords,
            numbers=result.numbers,
            phrases=result.phrases,
            found_on=result.found_on,
            total_checked=result.total_checked,
            results=result.results,
            overall_verdict=overall_verdict
        )
    
    except HTTPException:
        return Response(
            error = "HTTP Exception error"
        )
    except Exception as e:
        return Response(
            error=str(e)
        )
    
@app.post("/check_M2", response_model=Response)
async def site_search(req: Request):
    try:
        if not req.text or len(req.text.strip()) < 10:
            return Response(
                error = "Text must be at least 10 characters"
            )
        
        result: VerifierResult = await launcher(req.text)

        return Response(
            success=True,
            found_on=result.found_on,
            total_checked=result.total_checked,
            results=result.results
        )
    
    except HTTPException:
        return Response(
            error = "HTTP Exception error"
        )
    except Exception as e:
        return Response(
            error=str(e)
        )
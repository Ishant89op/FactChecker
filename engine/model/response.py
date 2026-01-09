from pydantic import BaseModel
from typing import List, Optional
from model.result import Result

class Response(BaseModel):
    success: bool = False
    country: str = ""
    keywords: List[str] = []
    numbers: List[str] = []
    phrases: List[str] = []
    found_on: int = -1
    total_checked: int = -1
    results: List[Result] = []
    overall_verdict: str = ""
    error: Optional[str] = None
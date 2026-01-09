from pydantic import BaseModel
from typing import List, Optional
from model.result import Result

class VerifierResult(BaseModel):
    country: str = ""
    keywords: List[str] = []
    numbers: List[str] = []
    phrases: List[str] = []
    found_on: int = -1
    total_checked: int = -1
    results: List[Result] = []
    error: Optional[str] = None

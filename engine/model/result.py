from pydantic import BaseModel
from typing import Optional

class Result(BaseModel):
    found: bool = False
    site: str = ""
    url: str = ""
    snippet: str = ""
    numbers_matched: int = -1
    phrases_matched: int = -1
    verdict: bool = False
    error: Optional[str] = None

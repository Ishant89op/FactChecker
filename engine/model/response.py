from dataclasses import dataclass, field
from typing import Optional, List
from model.verifier_result import VerifierResult

@dataclass
class Response:
    success: bool = False
    country: str = ""
    keywords: List[str] = field(default_factory=list)
    numbers: List[str] = field(default_factory=list)
    phrases: List[str] = field(default_factory=list)
    found_on: int = -1
    total_checked: int = -1
    results: Optional[VerifierResult] = None
    overall_verdict: str = ""
    error: Optional[str] = None

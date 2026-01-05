from typing import Optional
from dataclasses import dataclass
from model.result import Result

@dataclass
class VerifierResult:
    def __init__(
            self,
            country: str = "",
            keywords: list[str] = [],
            numbers: list[str] = [],
            phrases: list[str] = [],
            found_on: int = -1,
            total_checked: int = -1,
            results: list[Result] = [],
            error: Optional[str] = None

    ):
        self.country = country
        self.keywords = keywords
        self.numbers = numbers
        self.phrases = phrases
        self.found_on = found_on
        self.total_checked = total_checked
        self.results = results
        self.error = error
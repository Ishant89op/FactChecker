from dataclasses import dataclass
from typing import Optional

@dataclass
class Result:
    def __init__(
        self,
        found: bool = False,
        site: str = "",
        url: str = "",
        snippet: str = "",
        numbers_matched: int = -1,
        phrases_matched: int = -1,
        verdict: bool = False,
        error: Optional[str] = None
    ):
        self.found = found
        self.site = site
        self.url = url
        self.snippet = snippet
        self.numbers_matched = numbers_matched
        self.phrases_matched = phrases_matched
        self.verdict = verdict
        self.error = error
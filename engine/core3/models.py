from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from enum import Enum


class StanceType(str, Enum):
    SUPPORTING = "supporting"
    CONTRADICTING = "contradicting"
    NEUTRAL = "neutral"


class VerdictType(str, Enum):
    VERY_LIKELY = "VERY_LIKELY"
    LIKELY = "LIKELY"
    UNLIKELY = "UNLIKELY"
    VERY_UNLIKELY = "VERY_UNLIKELY"
    DISPUTED = "DISPUTED"


class InputType(str, Enum):
    STATEMENT = "statement"
    URL = "url"


class JobStatusType(str, Enum):
    QUEUED = "queued"
    SCRAPING = "scraping"
    ANALYZING = "analyzing"
    RECONCILING = "reconciling"
    COMPLETE = "complete"
    FAILED = "failed"


class SourceEvidence(BaseModel):
    source_name: str
    url: str
    relevant_text: str = Field(max_length=500)
    stance: StanceType
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PlaywrightScore(BaseModel):
    score: int = Field(ge=1, le=10)
    reasoning: str
    sources_used: list[str]


class LLMVerdict(BaseModel):
    model_name: str
    verdict: VerdictType
    score: int = Field(ge=1, le=10)
    reasoning: str
    sources_used: list[str]


class ReconciledResult(BaseModel):
    final_verdict: VerdictType
    final_score: int = Field(ge=1, le=10)
    playwright_score: PlaywrightScore
    gemini_verdict: Optional[LLMVerdict] = None
    openai_verdict: Optional[LLMVerdict] = None
    sources: list[SourceEvidence]
    models_agree: bool
    reconciliation_note: str


class VerificationRequest(BaseModel):
    input: str
    type: InputType


class JobStatus(BaseModel):
    job_id: str
    status: JobStatusType
    sources_checked: int = 0
    total_sources: int = 0
    message: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class JobResult(BaseModel):
    job_id: str
    request: VerificationRequest
    result: Optional[ReconciledResult] = None
    error: Optional[str] = None
    completed_at: Optional[datetime] = None

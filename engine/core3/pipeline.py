import logging
from datetime import datetime, timezone

from core3.scraper import scrape_all
from core3.scorer import compute_score
from core3.llm import run_llm_engines
from core3.reconciler import reconcile
from core3.models import (
    VerificationRequest,
    ReconciledResult,
    JobResult,
)

logger = logging.getLogger(__name__)


async def run_pipeline(
    job_id: str,
    request: VerificationRequest,
    claim_text: str,
    gemini_api_key: str,
    openai_api_key: str,
    gemini_model: str,
    openai_model: str,
    update_status_fn=None,
) -> JobResult:
    try:
        if update_status_fn:
            await update_status_fn(job_id, "scraping", "Scraping sources...")

        evidence = await scrape_all(claim_text)
        logger.info(f"Job {job_id}: scraped {len(evidence)} sources")

        if update_status_fn:
            await update_status_fn(
                job_id,
                "analyzing",
                f"Analyzing {len(evidence)} sources with LLMs...",
                sources_checked=len(evidence),
            )

        playwright_score = compute_score(evidence)

        gemini_verdict, openai_verdict = await run_llm_engines(
            claim=claim_text,
            evidence=evidence,
            gemini_api_key=gemini_api_key,
            openai_api_key=openai_api_key,
            gemini_model=gemini_model,
            openai_model=openai_model,
        )

        if update_status_fn:
            await update_status_fn(job_id, "reconciling", "Reconciling scores...")

        result = reconcile(
            playwright_score=playwright_score,
            gemini_verdict=gemini_verdict,
            openai_verdict=openai_verdict,
            sources=evidence,
        )

        if update_status_fn:
            await update_status_fn(
                job_id,
                "complete",
                f"Verification complete. Score: {result.final_score}/10",
            )

        return JobResult(
            job_id=job_id,
            request=request,
            result=result,
            completed_at=datetime.now(timezone.utc),
        )

    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")

        if update_status_fn:
            await update_status_fn(job_id, "failed", f"Pipeline error: {str(e)[:200]}")

        return JobResult(
            job_id=job_id,
            request=request,
            error=str(e)[:500],
            completed_at=datetime.now(timezone.utc),
        )

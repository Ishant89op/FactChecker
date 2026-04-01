import asyncio
import logging

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from core3.models import VerificationRequest, InputType
from core3.pipeline import run_pipeline
from api.auth import get_current_user
from api.job_store import job_store
from api.url_fetcher import fetch_url_text, URLFetchError, UnsupportedContentError
from api.settings import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["verification"])


async def _run_verification_task(
    job_id: str,
    request: VerificationRequest,
    claim_text: str,
):
    """Background task that runs the full verification pipeline."""
    try:
        result = await run_pipeline(
            job_id=job_id,
            request=request,
            claim_text=claim_text,
            gemini_api_key=settings.gemini_api_key,
            openai_api_key=settings.openai_api_key,
            gemini_model=settings.gemini_model,
            openai_model=settings.openai_model,
            update_status_fn=job_store.update_status,
        )
        await job_store.store_result(job_id, result)
    except Exception as e:
        logger.error(f"Background task failed for {job_id}: {str(e)[:200]}")
        await job_store.update_status(
            job_id, "failed", f"Unexpected error: {str(e)[:200]}"
        )


@router.post("/verify")
async def verify(
    request: VerificationRequest,
    user: dict = Depends(get_current_user),
):
    uid = user["uid"]

    # Validate input length
    if len(request.input.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Input too short. Provide at least 5 characters.",
        )
    if len(request.input) > 2000:
        raise HTTPException(
            status_code=400,
            detail="Input too long. Maximum 2000 characters.",
        )

    # Resolve claim text
    claim_text = request.input.strip()

    if request.type == InputType.URL:
        try:
            claim_text = await fetch_url_text(request.input.strip())
        except UnsupportedContentError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except URLFetchError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Create job and fire background task
    job_id = job_store.create_job(request, uid)

    asyncio.create_task(_run_verification_task(job_id, request, claim_text))

    return {"job_id": job_id, "status": "queued", "message": "Verification started"}


@router.get("/verify/{job_id}/status")
async def get_verification_status(
    job_id: str,
    user: dict = Depends(get_current_user),
):
    status_obj = job_store.get_status(job_id)
    if not status_obj:
        raise HTTPException(status_code=404, detail="Job not found")

    # Verify ownership
    job_uid = job_store.get_job_uid(job_id)
    if job_uid and job_uid != user["uid"]:
        raise HTTPException(status_code=403, detail="Access denied")

    return status_obj.model_dump(mode="json")


@router.get("/verify/{job_id}/result")
async def get_verification_result(
    job_id: str,
    user: dict = Depends(get_current_user),
):
    # Verify ownership
    job_uid = job_store.get_job_uid(job_id)
    if job_uid and job_uid != user["uid"]:
        raise HTTPException(status_code=403, detail="Access denied")

    result = job_store.get_result(job_id)
    if result:
        return result.model_dump(mode="json")

    # Check if job exists but isn't done yet
    status_obj = job_store.get_status(job_id)
    if status_obj:
        return JSONResponse(
            status_code=202,
            content={
                "job_id": job_id,
                "status": status_obj.status,
                "message": "Verification still in progress",
            },
        )

    raise HTTPException(status_code=404, detail="Job not found")


@router.get("/health")
async def health():
    return {"status": "ok"}

import asyncio
import uuid
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

from core3.models import (
    JobStatus,
    JobStatusType,
    JobResult,
    VerificationRequest,
)
from api.firebase import get_firestore_client

logger = logging.getLogger(__name__)

CLEANUP_AGE_HOURS = 2


class JobStore:
    def __init__(self):
        self._jobs: dict[str, dict] = {}
        self._results: dict[str, JobResult] = {}
        self._lock = asyncio.Lock()

    def create_job(self, request: VerificationRequest, uid: str) -> str:
        job_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        self._jobs[job_id] = {
            "job_id": job_id,
            "uid": uid,
            "status": JobStatusType.QUEUED,
            "sources_checked": 0,
            "total_sources": 0,
            "message": "Job queued",
            "created_at": now,
            "request": request,
        }

        asyncio.create_task(self._write_to_firestore_create(job_id, request, uid, now))

        return job_id

    async def update_status(
        self,
        job_id: str,
        status: str,
        message: str = "",
        sources_checked: int = 0,
        total_sources: int = 0,
    ):
        async with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id]["status"] = status
                self._jobs[job_id]["message"] = message
                if sources_checked:
                    self._jobs[job_id]["sources_checked"] = sources_checked
                if total_sources:
                    self._jobs[job_id]["total_sources"] = total_sources

        asyncio.create_task(
            self._write_to_firestore_status(job_id, status, message)
        )

    async def store_result(self, job_id: str, result: JobResult):
        async with self._lock:
            self._results[job_id] = result
            if job_id in self._jobs:
                uid = self._jobs[job_id].get("uid", "")
        asyncio.create_task(self._write_to_firestore_result(job_id, result, uid))

    def get_status(self, job_id: str) -> Optional[JobStatus]:
        job = self._jobs.get(job_id)
        if not job:
            return None
        return JobStatus(
            job_id=job["job_id"],
            status=job["status"],
            sources_checked=job["sources_checked"],
            total_sources=job["total_sources"],
            message=job["message"],
            created_at=job["created_at"],
        )

    def get_result(self, job_id: str) -> Optional[JobResult]:
        return self._results.get(job_id)

    def get_job_uid(self, job_id: str) -> Optional[str]:
        job = self._jobs.get(job_id)
        if job:
            return job.get("uid")
        return None

    async def cleanup_old_jobs(self):
        cutoff = datetime.now(timezone.utc) - timedelta(hours=CLEANUP_AGE_HOURS)
        async with self._lock:
            expired = [
                jid for jid, j in self._jobs.items()
                if j["created_at"] < cutoff
            ]
            for jid in expired:
                self._jobs.pop(jid, None)
                self._results.pop(jid, None)
            if expired:
                logger.info(f"Cleaned up {len(expired)} expired jobs")

    async def _write_to_firestore_create(
        self, job_id: str, request: VerificationRequest, uid: str, created_at: datetime
    ):
        try:
            db = get_firestore_client()
            doc_ref = db.collection("users").document(uid).collection(
                "verifications"
            ).document(job_id)
            await doc_ref.set({
                "job_id": job_id,
                "input": request.input,
                "type": request.type.value,
                "status": "queued",
                "final_score": None,
                "final_verdict": None,
                "result": None,
                "error": None,
                "created_at": created_at,
                "completed_at": None,
            })
        except Exception as e:
            logger.warning(f"Firestore create failed for {job_id}: {str(e)[:100]}")

    async def _write_to_firestore_status(
        self, job_id: str, status: str, message: str
    ):
        try:
            uid = self.get_job_uid(job_id)
            if not uid:
                return
            db = get_firestore_client()
            doc_ref = db.collection("users").document(uid).collection(
                "verifications"
            ).document(job_id)
            await doc_ref.update({"status": status})
        except Exception as e:
            logger.warning(f"Firestore status update failed for {job_id}: {str(e)[:100]}")

    async def _write_to_firestore_result(
        self, job_id: str, result: JobResult, uid: str
    ):
        try:
            db = get_firestore_client()
            doc_ref = db.collection("users").document(uid).collection(
                "verifications"
            ).document(job_id)

            update_data = {
                "status": "complete" if not result.error else "failed",
                "completed_at": result.completed_at,
            }

            if result.result:
                update_data["final_score"] = result.result.final_score
                update_data["final_verdict"] = result.result.final_verdict
                update_data["result"] = result.result.model_dump(mode="json")
            if result.error:
                update_data["error"] = result.error

            await doc_ref.update(update_data)
        except Exception as e:
            logger.warning(f"Firestore result write failed for {job_id}: {str(e)[:100]}")


job_store = JobStore()

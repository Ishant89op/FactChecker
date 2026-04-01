import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from google.cloud.firestore_v1 import AsyncClient

from api.auth import get_current_user
from api.firebase import get_firestore_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/history", tags=["history"])


@router.get("")
async def get_history(
    user: dict = Depends(get_current_user),
    limit: int = Query(default=20, ge=1, le=100),
    cursor: str = Query(default=""),
):
    uid = user["uid"]
    db = get_firestore_client()
    col_ref = db.collection("users").document(uid).collection("verifications")

    query = col_ref.order_by("created_at", direction="DESCENDING").limit(limit)

    if cursor:
        cursor_doc = await col_ref.document(cursor).get()
        if cursor_doc.exists:
            query = query.start_after(cursor_doc)

    docs = await query.get()

    items = []
    for doc in docs:
        data = doc.to_dict()
        input_text = data.get("input", "")
        if len(input_text) > 80:
            input_text = input_text[:77] + "..."

        items.append({
            "job_id": data.get("job_id", doc.id),
            "input": input_text,
            "type": data.get("type", "statement"),
            "final_score": data.get("final_score"),
            "final_verdict": data.get("final_verdict"),
            "created_at": data.get("created_at"),
        })

    next_cursor = ""
    if items and len(items) == limit:
        next_cursor = items[-1]["job_id"]

    return {
        "items": items,
        "next_cursor": next_cursor,
    }


@router.get("/{job_id}")
async def get_history_detail(
    job_id: str,
    user: dict = Depends(get_current_user),
):
    uid = user["uid"]
    db = get_firestore_client()
    doc_ref = db.collection("users").document(uid).collection(
        "verifications"
    ).document(job_id)

    doc = await doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Verification not found")

    data = doc.to_dict()

    doc_uid = uid
    if data.get("uid") and data["uid"] != uid:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this verification",
        )

    return data

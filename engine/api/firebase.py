import json
import os
import logging

import firebase_admin
from firebase_admin import credentials, firestore_async

logger = logging.getLogger(__name__)

_app = None
_db = None


def init_firebase(service_account_json: str = "", service_account_path: str = ""):
    global _app, _db

    if _app is not None:
        return

    cred = None

    if service_account_json:
        try:
            account_info = json.loads(service_account_json)
            cred = credentials.Certificate(account_info)
            logger.info("Firebase initialized from Secret Manager JSON")
        except json.JSONDecodeError:
            logger.warning("Failed to parse service account JSON from Secret Manager")

    if cred is None and service_account_path and os.path.exists(service_account_path):
        cred = credentials.Certificate(service_account_path)
        logger.info(f"Firebase initialized from file: {service_account_path}")

    if cred is None:
        logger.error("No valid Firebase credentials found")
        raise RuntimeError("Firebase credentials not available")

    _app = firebase_admin.initialize_app(cred)
    _db = firestore_async.client()


def get_firestore_client():
    if _db is None:
        raise RuntimeError("Firebase not initialized. Call init_firebase() first.")
    return _db

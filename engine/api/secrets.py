import os
import logging
from typing import Optional
from functools import lru_cache

logger = logging.getLogger(__name__)

_secret_cache: dict[str, str] = {}


def _fetch_from_secret_manager(secret_name: str, project_id: str) -> Optional[str]:
    try:
        from google.cloud import secretmanager

        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logger.debug(f"Secret Manager unavailable for '{secret_name}': {str(e)[:100]}")
        return None


def get_secret(secret_name: str, env_var_fallback: str = "") -> Optional[str]:
    if secret_name in _secret_cache:
        return _secret_cache[secret_name]

    # Replace with your GCP project ID
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "")

    if project_id:
        value = _fetch_from_secret_manager(secret_name, project_id)
        if value:
            _secret_cache[secret_name] = value
            logger.info(f"Loaded '{secret_name}' from Secret Manager")
            return value

    if env_var_fallback:
        value = os.getenv(env_var_fallback)
        if value:
            _secret_cache[secret_name] = value
            logger.info(f"Loaded '{secret_name}' from env var '{env_var_fallback}'")
            return value

    return None


def clear_cache():
    _secret_cache.clear()

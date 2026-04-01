import os
import sys
import logging

from api.secrets import get_secret

logger = logging.getLogger(__name__)


class Settings:
    def __init__(self):
        self.app_api_key: str = ""
        self.gemini_api_key: str = ""
        self.openai_api_key: str = ""
        self.firebase_service_account: str = ""
        self.firebase_service_account_path: str = ""
        self.gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))

    def load(self):
        self.app_api_key = get_secret(
            "factcheck-app-api-key", "APP_API_KEY"
        ) or ""

        self.gemini_api_key = get_secret(
            "factcheck-gemini-api-key", "GEMINI_API_KEY"
        ) or ""

        self.openai_api_key = get_secret(
            "factcheck-openai-api-key", "OPENAI_API_KEY"
        ) or ""

        self.firebase_service_account = get_secret(
            "factcheck-firebase-service-account", ""
        ) or ""

        self.firebase_service_account_path = os.getenv(
            "FIREBASE_SERVICE_ACCOUNT_PATH", "./serviceAccountKey.json"
        )

        missing = []
        if not self.app_api_key:
            missing.append("APP_API_KEY")
        if not self.gemini_api_key:
            missing.append("GEMINI_API_KEY")
        if not self.openai_api_key:
            missing.append("OPENAI_API_KEY")

        has_firebase = (
            bool(self.firebase_service_account)
            or os.path.exists(self.firebase_service_account_path)
        )
        if not has_firebase:
            missing.append("FIREBASE_SERVICE_ACCOUNT")

        if missing:
            logger.error(
                f"Missing required secrets: {', '.join(missing)}. "
                "Set them in Secret Manager or .env for local development."
            )
            sys.exit(1)

        logger.info("All secrets loaded successfully")


settings = Settings()

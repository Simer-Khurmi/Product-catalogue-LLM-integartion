from dotenv import load_dotenv
import os

load_dotenv()

TMF_BASE_URL = os.getenv("TMF_BASE_URL", "").rstrip("/")
MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"
HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", "20"))

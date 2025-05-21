import os

# CORS settings
ALLOWED_ORIGINS = [os.getenv("ALLOWED_ORIGIN", "*")]
ALLOW_CREDENTIALS = True
ALLOWED_METHODS = ["*"]
ALLOWED_HEADERS = ["*"]

# Static files directory for avatars
AVATARS_DIR = os.getenv("AVATARS_DIR", "avatars")

# Service URLs and ports
PORT = int(os.getenv("PORT", 5105))
AI_ENGINE_URL = os.getenv("AI_ENGINE_URL", "http://ai-engine:6000")
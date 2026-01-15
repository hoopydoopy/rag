# core/ai/client.py

from pathlib import Path
from google import genai

# Load API key
SECRET_DIR = Path(__file__).resolve().parents[2] / "secret"
API_KEY_FILE = SECRET_DIR / "google_api_key.txt"
api_key = API_KEY_FILE.read_text().strip()

client = genai.Client(api_key=api_key)

DEFAULT_MODEL = "models/gemma-3-27b-it"

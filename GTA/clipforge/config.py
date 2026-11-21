"""Configuration for GTA ClipForge."""

from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "exports"
DATA_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

class BrandConfig(BaseModel):
    name: str = "gta"
    target_duration_min: float = 15.0
    target_duration_max: float = 45.0
    aspect_ratio: str = "9:16"
    caption_style: str = "high_energy_yellow"
    scoring_weights: dict = {
        "loudness": 0.35,
        "hype_words": 0.25,
        "motion_energy": 0.25,
        "transcript": 0.15,
    }
    prompt_tone: str = "high-energy gaming hook, dramatic, funny, fast-paced"


class Settings:
    DATABASE_PATH: Path = DATA_DIR / "clipforge.db"
    TOKEN_ENCRYPTION_KEY: str = ""
    GEMINI_API_KEY: str = ""
    PUBLIC_MEDIA_BASE_URL: str = "http://localhost:8800"
    PUBLISH_ENABLED: bool = False


settings = Settings()
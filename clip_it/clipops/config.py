"""Configuration & Brand Settings for Clip Operations Center."""

import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "exports"
DATA_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


class BrandConfig(BaseModel):
    name: str
    target_duration_min: float
    target_duration_max: float
    aspect_ratio: str = "9:16"
    caption_style: str
    scoring_weights: dict
    prompt_tone: str


BRAND_CONFIGS = {
    "gta": BrandConfig(
        name="gta",
        target_duration_min=15.0,
        target_duration_max=45.0,
        aspect_ratio="9:16",
        caption_style="high_energy_yellow",
        scoring_weights={
            "loudness": 0.35,
            "hype_words": 0.25,
            "motion_energy": 0.25,
            "transcript": 0.15,
        },
        prompt_tone="high-energy gaming hook, dramatic, funny, fast-paced",
    ),
    "podcast": BrandConfig(
        name="podcast",
        target_duration_min=30.0,
        target_duration_max=90.0,
        aspect_ratio="9:16",
        caption_style="clean_readable_white",
        scoring_weights={
            "speech_clarity": 0.30,
            "sentiment_insight": 0.30,
            "completeness": 0.20,
            "speaker_change": 0.20,
        },
        prompt_tone="insightful, intrigue hook, clear value, thought-provoking",
    ),
}


class Settings:
    DATABASE_PATH: Path = DATA_DIR / "clipops.db"
    TOKEN_ENCRYPTION_KEY: str = os.getenv("TOKEN_ENCRYPTION_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    YOUTUBE_CLIENT_ID: str = os.getenv("YOUTUBE_CLIENT_ID", "")
    YOUTUBE_CLIENT_SECRET: str = os.getenv("YOUTUBE_CLIENT_SECRET", "")
    PUBLIC_MEDIA_BASE_URL: str = os.getenv("PUBLIC_MEDIA_BASE_URL", "http://localhost:8765")
    PUBLISH_ENABLED: bool = os.getenv("CLIPOPS_PUBLISH_ENABLED", "0") in ("1", "true", "True")


settings = Settings()


def get_brand_config(brand_name: str) -> BrandConfig:
    brand = brand_name.lower()
    if brand not in BRAND_CONFIGS:
        raise ValueError(f"Unknown brand '{brand_name}'. Valid brands: {list(BRAND_CONFIGS.keys())}")
    return BRAND_CONFIGS[brand]

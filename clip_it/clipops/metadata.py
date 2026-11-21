"""Hook titles, descriptions, hashtags, and thumbnail generation."""

import re
from typing import List, Dict, Any

from clipops.config import get_brand_config


def generate_metadata(clip_text: str, brand: str = "gta",
                      moment_signals: List[str] = None) -> Dict[str, Any]:
    """Generate title, description, and hashtags for a clip."""
    cfg = get_brand_config(brand)
    signals = moment_signals or []
    signal_text = " ".join(signals)
    brand_lower = brand.lower()

    if brand_lower == "gta":
        title = _gta_title(clip_text, signals)
        description = _gta_description(clip_text, signals)
        hashtags = ["#GTA", "#Shorts", "#Gaming", "#ClipForge"]
    else:
        title = _podcast_title(clip_text, signals)
        description = _podcast_description(clip_text, signals)
        hashtags = ["#Podcast", "#Shorts", "#ClipForge", "#Interview"]

    return {
        "title": title,
        "description": description,
        "hashtags": hashtags,
        "tags": hashtags,
    }


def _gta_title(text: str, signals: List[str]) -> str:
    hooks = [
        "You Won't Believe This...",
        "This Just Happened 😱",
        "No Way This Is Real!",
        "The Ultimate Clutch!",
        "Wait For The Ending...",
        "Best Moment Of The Stream!",
        "Insane Play Caught On Cam!",
    ]
    # Pick a hook based on text content
    text_lower = text.lower()
    if "kill" in text_lower or "clutch" in text_lower:
        return hooks[3]
    if "laugh" in text_lower or "funny" in text_lower:
        return hooks[5]
    if "no way" in text_lower:
        return hooks[2]
    return hooks[0]


def _gta_description(text: str, signals: List[str]) -> str:
    snippet = text[:120].strip()
    return f"{snippet}...\n\n🔥 Best moments clipped live. Subscribe for more!\n#GTA #Shorts #Gaming"


def _podcast_title(text: str, signals: List[str]) -> str:
    hooks = [
        "The Truth About...",
        "This Will Change How You Think",
        "The Hidden Lesson",
        "What They Don't Tell You",
        "A Must-Listen Insight",
        "The Real Story Behind It",
    ]
    text_lower = text.lower()
    if "lesson" in text_lower or "learned" in text_lower:
        return hooks[2]
    if "truth" in text_lower or "real" in text_lower:
        return hooks[0]
    if "secret" in text_lower:
        return hooks[3]
    return hooks[1]


def _podcast_description(text: str, signals: List[str]) -> str:
    snippet = text[:140].strip()
    return f"{snippet}...\n\n🎧 Full episode linked in bio. Share with someone who needs to hear this.\n#Podcast #Shorts #ClipForge"


def generate_thumbnail(clip_text: str, brand: str = "gta", output_path: str = None) -> str:
    """Generate a simple thumbnail image."""
    if output_path is None:
        return ""
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGB", (1280, 720), (20, 20, 30))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 64)
        except Exception:
            font = ImageFont.load_default()
        title = generate_metadata(clip_text, brand)["title"][:40]
        draw.text((40, 300), title, fill=(255, 255, 0), font=font)
        img.save(output_path)
        return output_path
    except Exception:
        return ""
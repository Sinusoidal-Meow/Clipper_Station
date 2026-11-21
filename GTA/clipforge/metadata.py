"""Title, description, and hashtag generation for gaming clips."""

from typing import List, Dict, Any

def generate_metadata(clip_text: str, moment_signals: List[str] = None) -> Dict[str, Any]:
    """Generate title, description, and hashtags for a gaming clip."""
    clip_text = clip_text or ""
    signals = moment_signals or []

    title = _gta_title(clip_text, signals)
    description = _gta_description(clip_text, signals)
    hashtags = ["#GTA", "#Shorts", "#Gaming", "#ClipForge"]

    return {
        "title": title,
        "description": description,
        "hashtags": hashtags,
        "tags": hashtags
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
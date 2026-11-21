"""Multi-signal moment detection for clipops."""

import re
from typing import List, Dict, Any

HYPE_KEYWORDS = [
    "oh my god", "omg", "insane", "insanity", "crazy", "insane",
    "holy", "holy shit", "let's go", "lets go", "goat", "sick",
    "no way", "what a", "unbelievable", "incredible", "sicko",
    "fire", "banger", "clutch", "kill", "killcam", "rage",
    "laugh", "funny", "lol", "lmao", "rofl", "moment", "best",
    "greatest", "epic", "perfect", "nice", "beautiful", "chef kiss",
]

PODCAST_INSIGHT_KEYWORDS = [
    "important", "truth", "realize", "realized", "understand",
    "insight", "lesson", "learned", "key", "fundamental", "actually",
    "the thing is", "here's the thing", "point is", "bottom line",
    "remember", "never forget", "mind-blowing", "mind blowing",
    "breakthrough", "game changer", "game-changer", "secret",
]


def detect_moments(transcript: List[Dict[str, Any]], brand: str = "gta",
                  audio_features: List[Dict[str, Any]] = None,
                  chat_messages: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Score transcript segments for clip-worthy moments."""
    audio_features = audio_features or []
    chat_messages = chat_messages or []

    keywords = HYPE_KEYWORDS if brand == "gta" else PODCAST_INSIGHT_KEYWORDS
    moments = []

    for seg in transcript:
        text = seg.get("text", "").lower()
        score = 0.0
        signals = []

        # Keyword scoring
        kw_hits = [kw for kw in keywords if kw in text]
        if kw_hits:
            score += 0.4 * min(len(kw_hits), 1.0)
            signals.append(f"keywords: {kw_hits}")

        # Volume spike
        if audio_features:
            seg_audio = [a for a in audio_features if a.get("start", 0) >= seg["start"] - 0.5
                         and a.get("end", 0) <= seg["end"] + 0.5]
            if seg_audio:
                avg_loud = sum(a.get("loudness", 0) for a in seg_audio) / len(seg_audio)
                if avg_loud > 0.7:
                    score += 0.3
                    signals.append(f"loudness:{avg_loud:.2f}")

        # Chat spike
        if chat_messages:
            seg_chat = [c for c in chat_messages
                        if c.get("timestamp", 0) >= seg["start"] - 1.0
                        and c.get("timestamp", 0) <= seg["end"] + 1.0]
            if seg_chat:
                score += 0.2 * min(len(seg_chat) / 10.0, 1.0)
                signals.append(f"chat:{len(seg_chat)}")

        # Exclamation / excitement
        if "!" in text:
            score += 0.1

        if score > 0.25:
            moments.append({
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"],
                "score": round(score, 3),
                "signals": signals,
                "words": seg.get("words", []),
            })

    return moments


def rank_moments(moments: List[Dict[str, Any]], brand: str = "gta") -> List[Dict[str, Any]]:
    """Rank moments by score and filter by brand duration constraints."""
    from clipops.config import get_brand_config
    cfg = get_brand_config(brand)

    ranked = sorted(moments, key=lambda m: m["score"], reverse=True)
    for m in ranked:
        m["duration"] = m["end"] - m["start"]
        # Penalize clips outside target range
        if m["duration"] < cfg.target_duration_min:
            m["score"] *= 0.7
        elif m["duration"] > cfg.target_duration_max:
            m["score"] *= 0.8

    ranked = [m for m in ranked if m["score"] > 0.25]
    return ranked
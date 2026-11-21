"""Moment detection for gaming content."""

from typing import List, Dict, Any

HYPE_KEYWORDS = [
    "oh my god", "insane", "fire", "holy shit", "laugh", "funny", "wow",
    "amazing", "clutch", "sick", "best", "no way", "wait", "epic",
    "crazy", "legendary", "unbelievable", "shocked", "mind blown"
]


def detect_moments(transcript: List[Dict], audio_features: List[Dict] = None, chat_messages: List[Dict] = None) -> List[Dict]:
    """Detect hype moments from transcript with optional audio features."""
    audio_features = audio_features or []
    chat_messages = chat_messages or []
    moments = []

    for segment in transcript:
        text_lower = segment.get("text", "").lower()
        score = 0.0
        signals = []

        for keyword in HYPE_KEYWORDS:
            if keyword in text_lower:
                score += 0.3
                signals.append(f"keywords: {keyword}")

        for keyword in ["laugh", "funny", "haha"]:
            if keyword in text_lower:
                score += 0.2
                signals.append("fun: laugh")

        if audio_features:
            for feat in audio_features:
                if feat.get("start") == segment.get("start"):
                    loudness = feat.get("loudness", 0)
                    if loudness > 0.7:
                        score += 0.2 * loudness
                        signals.append(f"loudness: {loudness:.2f}")

        if chat_messages:
            signals.append("chat: activity_detected")

        if score >= 0.25:
            moments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"],
                "score": min(score, 1.0),
                "words": segment.get("words", []),
                "signals": signals
            })

    return moments


def rank_moments(moments: List[Dict], brand: str = "gta") -> List[Dict]:
    """Rank moments by score, apply duration penalties, and add duration."""
    if not moments:
        return []

    scored = []
    for m in moments:
        base_score = m.get("score", 0.5)
        duration = m["end"] - m["start"]

        if duration < 15.0:
            penalty = (15.0 - duration) * 0.02
            final_score = base_score - penalty
        else:
            final_score = base_score

        if final_score < 0.25:
            continue

        scored.append({
            **m,
            "score": final_score,
            "duration": duration
        })

    return sorted(scored, key=lambda x: x["score"], reverse=True)
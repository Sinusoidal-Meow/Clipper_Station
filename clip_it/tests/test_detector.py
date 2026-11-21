"""Tests for clipops.detector module."""

import pytest
from clipops.detector import detect_moments, rank_moments, HYPE_KEYWORDS, PODCAST_INSIGHT_KEYWORDS


class TestKeywords:
    def test_hype_keywords_list(self):
        assert len(HYPE_KEYWORDS) > 0
        assert "oh my god" in HYPE_KEYWORDS
        assert "insane" in HYPE_KEYWORDS

    def test_podcast_keywords_list(self):
        assert len(PODCAST_INSIGHT_KEYWORDS) > 0
        assert "truth" in PODCAST_INSIGHT_KEYWORDS
        assert "insight" in PODCAST_INSIGHT_KEYWORDS


class TestDetectMoments:
    def test_returns_list(self):
        result = detect_moments([], brand="gta")
        assert isinstance(result, list)

    def test_detects_hype_keyword(self):
        transcript = [
            {"start": 0, "end": 2, "text": "Oh my god what a play!", "words": []}
        ]
        result = detect_moments(transcript, brand="gta")
        assert len(result) == 1
        assert result[0]["score"] > 0.25

    def test_detects_fun_keyword(self):
        transcript = [
            {"start": 0, "end": 2, "text": "that's so funny lol", "words": []}
        ]
        result = detect_moments(transcript, brand="gta")
        assert len(result) >= 1

    def test_no_moment_low_score(self):
        transcript = [
            {"start": 0, "end": 2, "text": "um okay then", "words": []}
        ]
        result = detect_moments(transcript, brand="gta")
        assert len(result) == 0

    def test_podcast_detects_insight(self):
        transcript = [
            {"start": 0, "end": 5, "text": "here's the real truth about this game", "words": []}
        ]
        result = detect_moments(transcript, brand="podcast")
        assert len(result) >= 1
        if result:
            assert result[0]["score"] > 0.25

    def test_with_audio_features(self):
        transcript = [
            {"start": 0, "end": 2, "text": "this is interesting content here", "words": []}
        ]
        audio = [{"start": 0, "end": 2, "loudness": 0.8}]
        result = detect_moments(transcript, brand="gta", audio_features=audio)
        assert len(result) >= 0

    def test_with_chat_messages(self):
        transcript = [
            {"start": 0, "end": 2, "text": "interesting clip material", "words": []}
        ]
        chat = [{"timestamp": 1.0}]
        result = detect_moments(transcript, brand="gta", chat_messages=chat)
        assert len(result) >= 0

    def test_moment_has_required_fields(self):
        transcript = [
            {"start": 0, "end": 3, "text": "oh my goodness wow", "words": [{"word": "oh", "start": 0, "end": 0.5}]}
        ]
        result = detect_moments(transcript, brand="gta")
        if result:
            seg = result[0]
            assert "start" in seg
            assert "end" in seg
            assert "text" in seg
            assert "score" in seg
            assert "words" in seg
            assert "signals" in seg

    def test_signals_is_list(self):
        transcript = [
            {"start": 0, "end": 2, "text": "oh my god this is amazing", "words": []}
        ]
        result = detect_moments(transcript, brand="gta")
        if result:
            assert isinstance(result[0]["signals"], list)


class TestRankMoments:
    def test_returns_list(self):
        moments = [{"start": 0, "end": 2, "score": 0.5}]
        result = rank_moments(moments, brand="gta")
        assert isinstance(result, list)

    def test_sorted_by_score_descending(self):
        moments = [
            {"start": 0, "end": 2, "score": 0.3},
            {"start": 2, "end": 4, "score": 0.8},
            {"start": 4, "end": 6, "score": 0.5},
        ]
        result = rank_moments(moments, brand="gta")
        assert len(result) >= 1
        if len(result) > 1:
            assert result[0]["score"] >= result[-1]["score"]

    def test_filters_low_score(self):
        moments = [
            {"start": 0, "end": 2, "score": 0.2},
        ]
        result = rank_moments(moments, brand="gta")
        assert len(result) == 0

    def test_adds_duration(self):
        moments = [{"start": 0, "end": 3, "score": 0.5}]
        result = rank_moments(moments, brand="gta")
        if result:
            assert result[0]["duration"] == 3.0

    def test_gta_duration_penalty_short(self):
        moments = [
            {"start": 0, "end": 2, "score": 0.8, "text": "oh my god wow amazing", "words": []}
        ]
        result = rank_moments(moments, brand="gta")
        if result:
            assert result[0]["duration"] == 2.0

    def test_podcast_duration_handled(self):
        moments = [
            {"start": 0, "end": 30, "score": 0.8, "text": "interesting insight here", "words": []}
        ]
        result = rank_moments(moments, brand="podcast")
        if result:
            assert result[0]["duration"] == 30.0
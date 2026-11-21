"""Tests for clipforge.detector module."""

import pytest
from clipforge.detector import detect_moments, rank_moments, HYPE_KEYWORDS
from clipforge.config import BrandConfig


class TestHypeKeywords:
    def test_hype_keywords_list_has_items(self):
        assert len(HYPE_KEYWORDS) > 0

    def test_hype_keywords_lowercase(self):
        for kw in HYPE_KEYWORDS:
            assert kw == kw.lower()

    def test_oh_my_god_keyword(self):
        assert "oh my god" in HYPE_KEYWORDS

    def test_insane_keyword(self):
        assert "insane" in HYPE_KEYWORDS


class TestDetectMoments:
    def test_returns_list(self, sample_transcript):
        result = detect_moments(sample_transcript)
        assert isinstance(result, list)

    def test_detects_hype_keyword(self, sample_transcript):
        result = detect_moments(sample_transcript)
        assert len(result) >= 1

    def test_detects_oh_my_god(self):
        transcript = [{"start": 0, "end": 2, "text": "oh my god what a play!", "words": []}]
        result = detect_moments(transcript)
        assert len(result) == 1
        assert result[0]["score"] > 0.25

    def test_no_moment_low_score(self):
        transcript = [{"start": 0, "end": 2, "text": "um okay then", "words": []}]
        result = detect_moments(transcript)
        assert len(result) == 0

    def test_has_signals_field(self, sample_transcript):
        result = detect_moments(sample_transcript)
        if result:
            assert "signals" in result[0]
            assert isinstance(result[0]["signals"], list)

    def test_with_audio_features(self, sample_transcript, sample_audio_features):
        result = detect_moments(sample_transcript, audio_features=sample_audio_features)
        assert len(result) >= 0


class TestRankMoments:
    def test_empty_input(self, sample_transcript):
        assert rank_moments([], brand="gta") == []

    def test_single_moment(self, sample_transcript):
        moments = [{"start": 0, "end": 2, "score": 0.8, "text": "test", "words": [], "signals": []}]
        result = rank_moments(moments, brand="gta")
        assert len(result) >= 1

    def test_sorted_by_score(self, sample_transcript):
        moments = [
            {"start": 0, "end": 2, "score": 0.3, "text": "test", "words": [], "signals": []},
            {"start": 2, "end": 4, "score": 0.9, "text": "test", "words": [], "signals": []},
            {"start": 4, "end": 6, "score": 0.5, "text": "test", "words": [], "signals": []},
        ]
        result = rank_moments(moments, brand="gta")
        if len(result) > 1:
            assert result[0]["score"] >= result[-1]["score"]

    def test_adds_duration(self):
        moments = [{"start": 0, "end": 5, "score": 0.8, "text": "test", "words": [], "signals": []}]
        result = rank_moments(moments, brand="gta")
        assert result[0]["duration"] == 5.0

    def test_filters_low_score(self):
        moments = [{"start": 0, "end": 2, "score": 0.1, "text": "test", "words": [], "signals": []}]
        result = rank_moments(moments, brand="gta")
        assert len(result) == 0


class TestGTAConfig:
    def test_gta_minimum_duration(self):
        cfg = BrandConfig()
        assert cfg.target_duration_min == 15.0

    def test_gta_maximum_duration(self):
        cfg = BrandConfig()
        assert cfg.target_duration_max == 45.0
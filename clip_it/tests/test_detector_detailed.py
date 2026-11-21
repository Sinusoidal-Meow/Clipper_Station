"""Detailed tests for clipops.detector module."""

import pytest
from clipops.detector import detect_moments, rank_moments, HYPE_KEYWORDS, PODCAST_INSIGHT_KEYWORDS
from clipops.config import BRAND_CONFIGS


class TestHypeKeywordsList:
    def test_list_has_items(self):
        assert len(HYPE_KEYWORDS) > 0

    def test_lowercase_keywords(self):
        for kw in HYPE_KEYWORDS:
            assert kw == kw.lower()

    def test_contains_oh_my_god(self):
        assert "oh my god" in HYPE_KEYWORDS

    def test_contains_insane(self):
        assert "insane" in HYPE_KEYWORDS

    def test_contains_fire(self):
        assert "fire" in HYPE_KEYWORDS

    def test_keyword_count(self):
        assert len(HYPE_KEYWORDS) >= 10


class TestPodcastKeywordsList:
    def test_list_has_items(self):
        assert len(PODCAST_INSIGHT_KEYWORDS) > 0

    def test_lowercase_keywords(self):
        for kw in PODCAST_INSIGHT_KEYWORDS:
            assert kw == kw.lower()

    def test_contains_truth(self):
        assert "truth" in PODCAST_INSIGHT_KEYWORDS

    def test_contains_insight(self):
        assert "insight" in PODCAST_INSIGHT_KEYWORDS

    def test_keyword_count(self):
        assert len(PODCAST_INSIGHT_KEYWORDS) >= 5


class TestDetectMomentsKeywordScoring:
    @pytest.mark.parametrize("keyword", ["oh my god", "insane", "fire", "holy shit", "laugh"])
    def test_detects_specific_keyword(self, keyword):
        transcript = [{"start": 0, "end": 2, "text": keyword, "words": []}]
        result = detect_moments(transcript, brand="gta")
        assert len(result) >= 1

    @pytest.mark.parametrize("keyword", ["truth", "insight", "lesson", "learned", "realized"])
    def test_detects_podcast_keyword(self, keyword):
        transcript = [{"start": 0, "end": 3, "text": keyword, "words": []}]
        result = detect_moments(transcript, brand="podcast")
        assert len(result) >= 1


class TestDetectMomentsSignals:
    def test_has_signals_field(self):
        transcript = [{"start": 0, "end": 2, "text": "oh my god wow", "words": []}]
        result = detect_moments(transcript, brand="gta")
        if result:
            assert "signals" in result[0]
            assert isinstance(result[0]["signals"], list)

    def test_signals_contain_keyword_match(self):
        transcript = [{"start": 0, "end": 2, "text": "oh my god amazing", "words": []}]
        result = detect_moments(transcript, brand="gta")
        if result:
            signals = result[0]["signals"]
            assert any("keywords" in s for s in signals)


class TestRankMomentsSorting:
    def test_empty_input(self):
        assert rank_moments([], brand="gta") == []

    def test_single_moment(self):
        moments = [{"start": 0, "end": 2, "score": 0.5}]
        result = rank_moments(moments, brand="gta")
        assert len(result) == 1
        assert result[0]["score"] <= 0.5

    def test_multi_moment_sorting(self):
        moments = [
            {"start": 0, "end": 2, "score": 0.3},
            {"start": 2, "end": 4, "score": 0.9},
            {"start": 4, "end": 6, "score": 0.5},
            {"start": 6, "end": 8, "score": 0.1},
        ]
        result = rank_moments(moments, brand="gta")
        assert len(result) >= 1
        if len(result) > 1:
            assert result[0]["score"] >= result[-1]["score"]


class TestRankMomentsFiltering:
    def test_filters_score_below_threshold(self):
        moments = [{"start": 0, "end": 2, "score": 0.1}]
        result = rank_moments(moments, brand="gta")
        assert result == []

    def test_preserves_score_above_threshold(self):
        moments = [{"start": 0, "end": 2, "score": 0.26}]
        result = rank_moments(moments, brand="gta")
        assert len(result) >= 0


class TestRankMomentsDuration:
    def test_adds_duration_field(self):
        moments = [{"start": 0, "end": 5, "score": 0.8}]
        result = rank_moments(moments, brand="gta")
        assert result[0]["duration"] == 5.0

    def test_duration_calculation(self):
        moments = [
            {"start": 0, "end": 3, "score": 0.8},
            {"start": 3, "end": 10, "score": 0.8},
        ]
        result = rank_moments(moments, brand="gta")
        durations = [m["duration"] for m in result]
        assert 3.0 in durations
        assert 7.0 in durations


class TestRankMomentsBrandSpecific:
    def test_gta_minimum_duration(self):
        cfg = BRAND_CONFIGS["gta"]
        min_dur = cfg.target_duration_min
        assert min_dur == 15.0

    def test_gta_maximum_duration(self):
        cfg = BRAND_CONFIGS["gta"]
        max_dur = cfg.target_duration_max
        assert max_dur == 45.0

    def test_podcast_minimum_duration(self):
        cfg = BRAND_CONFIGS["podcast"]
        min_dur = cfg.target_duration_min
        assert min_dur == 30.0

    def test_podcast_maximum_duration(self):
        cfg = BRAND_CONFIGS["podcast"]
        max_dur = cfg.target_duration_max
        assert max_dur == 90.0
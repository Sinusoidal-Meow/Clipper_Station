"""Tests for clipforge.metadata module."""

import pytest
from clipforge.metadata import generate_metadata, _gta_title, _gta_description


class TestGenerateMetadata:
    def test_returns_dict(self):
        result = generate_metadata("test clip text")
        assert isinstance(result, dict)

    def test_has_title(self):
        result = generate_metadata("test clip")
        assert "title" in result

    def test_has_description(self):
        result = generate_metadata("test clip")
        assert "description" in result

    def test_has_hashtags(self):
        result = generate_metadata("test clip")
        assert "hashtags" in result

    def test_has_tags(self):
        result = generate_metadata("test clip")
        assert "tags" in result

    def test_gta_has_gaming_tags(self):
        result = generate_metadata("epic clip")
        assert "#GTA" in result["hashtags"]

    def test_hashtag_includes_shorts(self):
        result = generate_metadata("test")
        assert "#Shorts" in result["hashtags"]


class TestGTATitle:
    def test_returns_string(self):
        result = _gta_title("test text", [])
        assert isinstance(result, str)

    def test_non_empty(self):
        result = _gta_title("amazing clip", [])
        assert len(result) > 0

    def test_max_length(self):
        result = _gta_title("x" * 200, [])
        assert len(result) <= 60

    def test_kill_clutch_selection(self):
        result = _gta_title("that was a kill", [])
        assert "Clutch" in result


class TestGTADescription:
    def test_returns_string(self):
        result = _gta_description("test clip text", [])
        assert isinstance(result, str)

    def test_includes_hashtags(self):
        result = _gta_description("epic moment", [])
        assert "#" in result

    def test_includes_clip_text(self):
        result = _gta_description("amazing play happened", [])
        assert "amazing" in result.lower()

    def test_has_call_to_action(self):
        result = _gta_description("epic play", [])
        assert "Subscribe" in result or "clip" in result.lower()
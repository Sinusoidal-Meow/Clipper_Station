"""Tests for clipops.metadata module."""

import pytest
from clipops.metadata import (
    generate_metadata, generate_thumbnail,
    _gta_title, _gta_description, _podcast_title, _podcast_description
)


class TestGenerateMetadata:
    def test_returns_dict(self):
        result = generate_metadata("test clip text", brand="gta")
        assert isinstance(result, dict)

    def test_has_title(self):
        result = generate_metadata("test clip", brand="gta")
        assert "title" in result

    def test_has_description(self):
        result = generate_metadata("test clip", brand="gta")
        assert "description" in result

    def test_has_hashtags(self):
        result = generate_metadata("test clip", brand="gta")
        assert "hashtags" in result

    def test_has_tags(self):
        result = generate_metadata("test clip", brand="gta")
        assert "tags" in result

    def test_gta_has_gaming_tags(self):
        result = generate_metadata("wow clip", brand="gta")
        assert "#GTA" in result["hashtags"]

    def test_podcast_has_podcast_tags(self):
        result = generate_metadata("interesting insight", brand="podcast")
        assert "#Podcast" in result["hashtags"]

    def test_signals_included_in_description(self):
        result = generate_metadata("test", brand="gta", moment_signals=["keywords: oh my god"])
        assert len(result["description"]) > 0


class TestGTATitle:
    def test_returns_string(self):
        result = _gta_title("test text", [])
        assert isinstance(result, str)

    def test_includes_hook(self):
        result = _gta_title("you won't believe this", [])
        assert len(result) > 0

    def test_kill_keyword_selection(self):
        result = _gta_title("that was a kill", [])
        assert "Ultimate Clutch" in result
        assert len(result) <= 60


class TestGTADescription:
    def test_returns_string(self):
        result = _gta_description("test clip text", [])
        assert isinstance(result, str)

    def test_includes_hashtags(self):
        result = _gta_description("epic moment", [])
        assert "#" in result


class TestPodcastTitle:
    def test_returns_string(self):
        result = _podcast_title("test insight", [])
        assert isinstance(result, str)

    def test_learned_keyword_selection(self):
        result = _podcast_title("this is something I learned", [])
        assert "Hidden Lesson" in result


class TestPodcastDescription:
    def test_returns_string(self):
        result = _podcast_description("valuable insight here", [])
        assert isinstance(result, str)


class TestGenerateThumbnail:
    def test_missing_pillow(self):
        result = generate_thumbnail("test")
        assert result == ""

    def test_with_path_returns_string(self):
        result = generate_thumbnail("test", "gta", "/tmp/thumb.jpg")
        assert isinstance(result, str)
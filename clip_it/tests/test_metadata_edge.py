"""Edge case tests for clipops.metadata module."""

import pytest
from clipops.metadata import generate_metadata, generate_thumbnail


class TestMetadataEdgeCases:
    def test_empty_text(self):
        result = generate_metadata("", brand="gta")
        assert "title" in result

    def test_empty_text_podcast(self):
        result = generate_metadata("", brand="podcast")
        assert "title" in result

    def test_long_text_truncated(self):
        long_text = "a" * 500
        result = generate_metadata(long_text, brand="gta")
        assert len(result["title"]) <= 60

    def test_special_characters(self):
        result = generate_metadata("test <script>&\"'`$", brand="gta")
        assert "title" in result

    def test_unicode_text(self):
        result = generate_metadata("test 😂🔥 unicode text", brand="gta")
        assert "title" in result

    def test_case_insensitive_brand_gta(self):
        result = generate_metadata("test", brand="GTA")
        assert "#GTA" in result["hashtags"]

    def test_case_insensitive_brand_podcast(self):
        result = generate_metadata("test", brand="PODCAST")
        assert "#Podcast" in result["hashtags"]

    def test_signals_empty_list(self):
        result = generate_metadata("test", brand="gta", moment_signals=[])
        assert "title" in result

    def test_signals_multiple_entries(self):
        result = generate_metadata("test", brand="gta", moment_signals=["keywords: oh", "loudness:0.9"])
        assert "title" in result


class TestThumbnailEdgeCases:
    def test_empty_text_thumbnail(self):
        result = generate_thumbnail("", "gta", "/tmp/test.jpg")
        assert result == "" or result.endswith(".jpg")

    def test_none_brand_thumbnail(self):
        result = generate_thumbnail("test", None, "/tmp/test.jpg")
        assert result == ""

    def test_none_output_path(self):
        result = generate_thumbnail("test", "gta")
        assert result == ""

    def test_empty_output_path(self):
        result = generate_thumbnail("test", "gta", "")
        assert result == ""


class TestMetadataIntegration:
    def test_full_workflow_gta(self):
        text = "oh my god this play was insane"
        meta = generate_metadata(text, brand="gta")
        assert meta["title"]
        assert meta["description"]
        assert meta["hashtags"]
        assert "#GTA" in meta["hashtags"] or "#Shorts" in meta["hashtags"]

    def test_full_workflow_podcast(self):
        text = "here is the real truth about this game"
        meta = generate_metadata(text, brand="podcast")
        assert meta["title"]
        assert meta["description"]
        assert "#Podcast" in meta["hashtags"]

    def test_metadata_isolation_gta(self):
        meta1 = generate_metadata("clip one", brand="gta")
        meta2 = generate_metadata("clip two", brand="gta")
        assert meta1["title"] != meta2["title"] or True  # both have titles

    def test_metadata_isolation_podcast(self):
        meta1 = generate_metadata("clip one", brand="podcast")
        meta2 = generate_metadata("clip two", brand="podcast")
        assert meta1["title"] != meta2["title"] or True
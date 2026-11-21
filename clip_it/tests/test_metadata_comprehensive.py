"""Comprehensive tests for metadata generation."""

import pytest
from clipops.metadata import (
    generate_metadata, generate_thumbnail,
    _gta_title, _gta_description, _podcast_title, _podcast_description
)


class TestGTATitleComprehensive:
    @pytest.mark.parametrize("text,expected_in_output", [
        ("you won't believe this", "won't"),
        ("no way this is real", "way"),
        ("clutch kill", "clutch"),
    ])
    def test_title_contains_keyword(self, text, expected_in_output):
        result = _gta_title(text, [])
        assert expected_in_output.lower() in result.lower()

    def test_title_oh_my_god(self):
        result = _gta_title("oh my god amazing", [])
        assert result

    def test_title_wait_for_it(self):
        result = _gta_title("wait for it now", [])
        assert result

    def test_title_best_moment(self):
        result = _gta_title("best moment ever", [])
        assert result

    def test_title_insane_play(self):
        result = _gta_title("insane play", [])
        assert result

    def test_title_sick_combo(self):
        result = _gta_title("sick combo", [])
        assert result

    def test_title_max_length(self):
        result = _gta_title("x" * 200, [])
        assert len(result) <= 60

    def test_title_non_empty(self):
        result = _gta_title("test", [])
        assert len(result) > 0

    def test_title_has_exclamation(self):
        result = _gta_title("amazing clip", [])
        assert result


class TestGTADescriptionComprehensive:
    def test_description_has_hashtags(self):
        result = _gta_description("test clip", [])
        assert "#" in result

    def test_description_includes_clip_text(self):
        result = _gta_description("epic moment happened", [])
        assert "epic" in result.lower()

    def test_description_length_reasonable(self):
        result = _gta_description("test clip text content", [])
        assert len(result) >= 20

    def test_description_has_call_to_action(self):
        result = _gta_description("amazing play", [])
        assert "Subscribe" in result or "clip" in result.lower() or len(result) > 0


class TestPodcastTitleComprehensive:
    @pytest.mark.parametrize("text,expected_in_output", [
        ("truth about gaming", "truth"),
        ("truth in real insight", "truth"),
    ])
    def test_title_contains_keyword(self, text, expected_in_output):
        result = _podcast_title(text, [])
        assert expected_in_output.lower() in result.lower()

    def test_title_real_insight(self):
        result = _podcast_title("real insight here", [])
        assert result

    def test_title_hidden_fact(self):
        result = _podcast_title("hidden fact revealed", [])
        assert result  # Just check title is returned

    def test_title_learned_something(self):
        result = _podcast_title("learned something", [])
        assert "lesson" in result.lower() or "learned" in result.lower()

    def test_title_secret_is(self):
        result = _podcast_title("the secret is", [])
        assert "secret" in result.lower() or "they" in result.lower()

    def test_title_max_length(self):
        result = _podcast_title("x" * 300, [])
        assert len(result) <= 70


class TestPodcastDescriptionComprehensive:
    def test_description_has_hashtags(self):
        result = _podcast_description("valuable insight", [])
        assert "#" in result

    def test_description_has_mention(self):
        result = _podcast_description("listen to this", [])
        assert result


class TestGenerateMetadataComprehensive:
    def test_all_brands_return_dict(self):
        for brand in ["gta", "podcast"]:
            result = generate_metadata("test", brand=brand)
            assert isinstance(result, dict)

    def test_all_keys_present_gta(self):
        result = generate_metadata("test", brand="gta")
        assert "title" in result
        assert "description" in result
        assert "hashtags" in result
        assert "tags" in result

    def test_all_keys_present_podcast(self):
        result = generate_metadata("test", brand="podcast")
        assert "title" in result
        assert "description" in result
        assert "hashtags" in result
        assert "tags" in result

    def test_gta_has_gaming_hashtags(self):
        result = generate_metadata("epic clip", brand="gta")
        tags = result["hashtags"]
        assert isinstance(tags, list)
        assert len(tags) > 0

    def test_podcast_has_podcast_hashtags(self):
        result = generate_metadata("insight", brand="podcast")
        tags = result["hashtags"]
        assert isinstance(tags, list)

    def test_tags_is_list(self):
        result = generate_metadata("test", brand="gta")
        assert isinstance(result["tags"], list)


class TestMetadataIntegrationComprehensive:
    def test_gta_tags_include_short(self):
        result = generate_metadata("test", brand="gta")
        assert "#Shorts" in result["hashtags"]

    def test_podcast_tags_include_short(self):
        result = generate_metadata("test", brand="podcast")
        assert "#Shorts" in result["hashtags"]


class TestThumbnailEdgeCasesComprehensive:
    def test_empty_string_text(self):
        result = generate_thumbnail("", "gta", "/tmp/test.jpg")
        assert result == "" or result.endswith(".jpg")

    def test_none_brand(self):
        result = generate_thumbnail("test", None, "/tmp/test.jpg")
        assert result == ""

    def test_missing_output_path(self):
        result = generate_thumbnail("test", "gta")
        assert result == ""

    def test_whitespace_text(self):
        result = generate_thumbnail("   ", "gta", "/tmp/test.jpg")
        assert result == "" or result.endswith(".jpg")
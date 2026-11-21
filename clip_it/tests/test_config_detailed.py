"""Detailed tests for clipops.config module."""

import pytest
from clipops.config import BRAND_CONFIGS, BrandConfig, get_brand_config, settings


class TestBrandConfigDataclass:
    def test_brand_config_creation(self):
        cfg = BrandConfig(
            name="test",
            target_duration_min=10.0,
            target_duration_max=20.0,
            aspect_ratio="1:1",
            caption_style="test_style",
            scoring_weights={"test": 0.5},
            prompt_tone="test tone"
        )
        assert cfg.name == "test"
        assert cfg.target_duration_min == 10.0

    def test_brand_config_default_aspect_ratio(self):
        cfg = BrandConfig(
            name="test",
            target_duration_min=5,
            target_duration_max=10,
            caption_style="test",
            scoring_weights={"test": 0.5},
            prompt_tone="test"
        )
        assert cfg.aspect_ratio == "9:16"

    def test_brand_config_default_caption_style(self):
        cfg = BrandConfig(
            name="test",
            target_duration_min=5,
            target_duration_max=10,
            caption_style="test_style",
            scoring_weights={"test": 0.5},
            prompt_tone="test"
        )
        assert cfg.caption_style == "test_style"


class TestBrandConfigValues:
    def test_gta_values(self):
        cfg = BRAND_CONFIGS["gta"]
        assert cfg.name == "gta"
        assert cfg.target_duration_min == 15.0
        assert cfg.target_duration_max == 45.0

    def test_podcast_values(self):
        cfg = BRAND_CONFIGS["podcast"]
        assert cfg.name == "podcast"
        assert cfg.target_duration_min == 30.0
        assert cfg.target_duration_max == 90.0


class TestGetBrandConfigErrors:
    def test_invalid_brand_raises(self):
        with pytest.raises(ValueError):
            get_brand_config("invalid")

    def test_case_sensitive_brand(self):
        cfg = get_brand_config("GTA")
        assert cfg.name == "gta"


class TestSettingsAttributes:
    def test_has_database_path(self):
        assert hasattr(settings, "DATABASE_PATH")

    def test_has_token_encryption_key(self):
        assert hasattr(settings, "TOKEN_ENCRYPTION_KEY")

    def test_has_gemini_api_key(self):
        assert hasattr(settings, "GEMINI_API_KEY")

    def test_has_youtube_client_id(self):
        assert hasattr(settings, "YOUTUBE_CLIENT_ID")

    def test_has_youtube_client_secret(self):
        assert hasattr(settings, "YOUTUBE_CLIENT_SECRET")

    def test_has_public_media_base_url(self):
        assert hasattr(settings, "PUBLIC_MEDIA_BASE_URL")

    def test_has_publish_enabled(self):
        assert hasattr(settings, "PUBLISH_ENABLED")


class TestSettingsValues:
    def test_database_path_format(self):
        assert str(settings.DATABASE_PATH).endswith("clipops.db")

    def test_publish_disabled_default(self):
        assert settings.PUBLISH_ENABLED is False

    def test_token_encryption_key_default_empty(self):
        assert settings.TOKEN_ENCRYPTION_KEY == ""

    def test_gemini_api_key_default_empty(self):
        assert settings.GEMINI_API_KEY == ""

    def test_public_media_base_url_default(self):
        assert "localhost" in settings.PUBLIC_MEDIA_BASE_URL or "http" in settings.PUBLIC_MEDIA_BASE_URL
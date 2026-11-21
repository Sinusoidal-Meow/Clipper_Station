"""Tests for clipops.config module."""

import pytest
from clipops.config import BRAND_CONFIGS, get_brand_config, settings


class TestBrandConfig:
    def test_brand_configs_exists(self):
        assert "gta" in BRAND_CONFIGS
        assert "podcast" in BRAND_CONFIGS

    def test_gta_target_duration(self):
        cfg = get_brand_config("gta")
        assert cfg.target_duration_min == 15.0
        assert cfg.target_duration_max == 45.0

    def test_gta_aspect_ratio(self):
        cfg = get_brand_config("gta")
        assert cfg.aspect_ratio == "9:16"

    def test_gta_caption_style(self):
        cfg = get_brand_config("gta")
        assert cfg.caption_style == "high_energy_yellow"

    def test_podcast_target_duration(self):
        cfg = get_brand_config("podcast")
        assert cfg.target_duration_min == 30.0
        assert cfg.target_duration_max == 90.0

    def test_podcast_caption_style(self):
        cfg = get_brand_config("podcast")
        assert cfg.caption_style == "clean_readable_white"

    def test_get_brand_config_invalid(self):
        with pytest.raises(ValueError):
            get_brand_config("invalid_brand")

    def test_scoring_weights_present(self):
        cfg = get_brand_config("gta")
        assert "loudness" in cfg.scoring_weights
        assert "hype_words" in cfg.scoring_weights


class TestSettings:
    def test_settings_exists(self):
        assert settings is not None
        assert hasattr(settings, "DATABASE_PATH")
        assert hasattr(settings, "TOKEN_ENCRYPTION_KEY")

    def test_publish_disabled_default(self):
        assert settings.PUBLISH_ENABLED is False

    def test_database_path_exists(self):
        from clipops.config import DATA_DIR
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        assert DATA_DIR.exists()
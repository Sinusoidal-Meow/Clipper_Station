"""Tests for clipforge.config module."""

import pytest
from clipforge.config import BrandConfig, settings, BASE_DIR, DATA_DIR, EXPORTS_DIR


class TestBrandConfig:
    def test_brand_config_defaults(self):
        cfg = BrandConfig()
        assert cfg.name == "gta"
        assert cfg.target_duration_min == 15.0
        assert cfg.target_duration_max == 45.0

    def test_brand_config_aspect_ratio(self):
        cfg = BrandConfig()
        assert cfg.aspect_ratio == "9:16"

    def test_brand_config_caption_style(self):
        cfg = BrandConfig()
        assert cfg.caption_style == "high_energy_yellow"

    def test_brand_config_scoring_weights(self):
        cfg = BrandConfig()
        assert "loudness" in cfg.scoring_weights
        assert "hype_words" in cfg.scoring_weights

    def test_brand_config_custom_values(self):
        cfg = BrandConfig(name="custom", target_duration_min=10.0)
        assert cfg.name == "custom"
        assert cfg.target_duration_min == 10.0


class TestSettings:
    def test_settings_exists(self):
        assert settings is not None
        assert hasattr(settings, "DATABASE_PATH")
        assert hasattr(settings, "TOKEN_ENCRYPTION_KEY")

    def test_data_dir_exists(self):
        assert DATA_DIR.exists()

    def test_exports_dir_exists(self):
        assert EXPORTS_DIR.exists()

    def test_base_dir_exists(self):
        assert BASE_DIR.exists()
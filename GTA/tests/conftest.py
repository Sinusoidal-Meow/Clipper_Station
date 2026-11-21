"""Test configuration for ClipForge."""

import pytest
from pathlib import Path

@pytest.fixture
def brand():
    return "gta"

@pytest.fixture
def sample_transcript():
    return [
        {"start": 0, "end": 3, "text": "Welcome everyone, what's happening today?", "words": []},
        {"start": 8, "end": 12, "text": "Oh my god, did you see that play?!", "words": []},
        {"start": 25, "end": 30, "text": "Wait for the finish, this is insane!", "words": []},
    ]

@pytest.fixture
def sample_audio_features():
    return [
        {"start": 8, "end": 12, "loudness": 0.85},
    ]
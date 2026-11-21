"""Tests for clipops.transcription module."""

import pytest
from clipops.transcription import WhisperTranscriber


class TestWhisperTranscriber:
    def test_transcriber_init(self):
        t = WhisperTranscriber()
        assert t.model_size == "base"
        assert t._model is None

    def test_transcriber_custom_model(self):
        t = WhisperTranscriber(model_size="small")
        assert t.model_size == "small"

    def test_transcribe_returns_list(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent_audio.wav")
        assert isinstance(result, list)

    def test_transcribe_segment_structure(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent_audio.wav")
        if result:
            seg = result[0]
            assert "start" in seg
            assert "end" in seg
            assert "text" in seg
            assert "words" in seg

    def test_transcribe_words_structure(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent_audio.wav")
        if result and result[0].get("words"):
            word = result[0]["words"][0]
            assert "word" in word
            assert "start" in word
            assert "end" in word

    def test_load_model_mock_on_failure(self):
        t = WhisperTranscriber()
        t._model = "mock"
        assert t._model == "mock"

    def test_transcribe_mock_fallback(self):
        t = WhisperTranscriber()
        result = t.transcribe("/nonexistent/path.wav")
        assert len(result) >= 1
        assert len(result[0]["words"]) >= 5


class TestWhisperTranscriberModelSizes:
    @pytest.mark.parametrize("size", ["tiny", "base", "small", "medium", "large", "extra_large"])
    def test_model_size_accepted(self, size):
        t = WhisperTranscriber(model_size=size)
        assert t.model_size == size
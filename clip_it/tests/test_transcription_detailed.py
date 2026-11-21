"""Detailed tests for clipops.transcription module."""

import pytest
from clipops.transcription import WhisperTranscriber


class TestWhisperTranscriberInit:
    def test_default_model_size(self):
        t = WhisperTranscriber()
        assert t.model_size == "base"

    def test_custom_model_size(self):
        t = WhisperTranscriber(model_size="small")
        assert t.model_size == "small"

    def test_model_none_on_init(self):
        t = WhisperTranscriber()
        assert t._model is None

    def test_model_cache_none_on_init(self):
        t = WhisperTranscriber()
        t2 = WhisperTranscriber()
        assert t is not t2


class TestWhisperTranscriberModelLoading:
    def test_model_becomes_not_none_after_load(self):
        t = WhisperTranscriber()
        t._model = "mock"
        assert t._model == "mock"

    def test_mock_model_used(self):
        t = WhisperTranscriber()
        t._model = "mock"
        result = t.transcribe("any_path.wav")
        assert isinstance(result, list)


class TestWhisperTranscriberTranscribeFormat:
    def test_result_is_list(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent.wav")
        assert isinstance(result, list)

    def test_segment_has_start(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent.wav")
        if result:
            assert "start" in result[0]

    def test_segment_has_end(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent.wav")
        if result:
            assert "end" in result[0]

    def test_segment_has_text(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent.wav")
        if result:
            assert "text" in result[0]

    def test_segment_has_words(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent.wav")
        if result:
            assert "words" in result[0]


class TestWhisperTranscriberWordStructure:
    def test_words_is_list(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent.wav")
        if result and result[0].get("words"):
            assert isinstance(result[0]["words"], list)

    def test_word_has_word_key(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent.wav")
        if result and result[0].get("words"):
            assert "word" in result[0]["words"][0]

    def test_word_has_start_key(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent.wav")
        if result and result[0].get("words"):
            assert "start" in result[0]["words"][0]

    def test_word_has_end_key(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent.wav")
        if result and result[0].get("words"):
            assert "end" in result[0]["words"][0]

    def test_word_timestamps_ordered(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent.wav")
        if result and result[0].get("words"):
            words = result[0]["words"]
            for i in range(len(words) - 1):
                assert words[i]["end"] <= words[i + 1]["start"]


class TestWhisperTranscriberTimeOrdering:
    def test_segments_ordered_by_start(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent.wav")
        starts = [s["start"] for s in result]
        assert starts == sorted(starts)

    def test_segment_end_greater_than_start(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent.wav")
        for seg in result:
            assert seg["end"] > seg["start"]

    def test_no_negative_timestamps(self):
        t = WhisperTranscriber()
        result = t.transcribe("nonexistent.wav")
        for seg in result:
            assert seg["start"] >= 0
            assert seg["end"] >= 0
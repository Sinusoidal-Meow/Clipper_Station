"""Local transcription with Whisper."""

from typing import List, Dict, Any, Optional

class WhisperTranscriber:
    """Transcribe audio using local Whisper model."""

    def __init__(self, model_size: str = "base", device: str = "cpu", model: Any = None):
        self.model_size = model_size
        self.device = device
        self.model = model
        if model is None and device != "mock":
            self._load_model()

    def _load_model(self):
        try:
            from faster_whisper import WhisperModel
            self.model = WhisperModel(self.model_size, device=self.device)
        except ImportError:
            pass

    def transcribe(self, audio_path: str, language: str = "en") -> List[Dict]:
        """Transcribe audio file and return segments."""
        if self.model is None:
            return []

        segments, _ = self.model.transcribe(audio_path, language=language)
        result = []
        for seg in segments:
            result.append({
                "start": seg.start,
                "end": seg.end,
                "text": seg.text.strip(),
                "words": []
            })
        return result
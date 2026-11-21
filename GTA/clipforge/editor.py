"""Video editing and caption rendering."""

from pathlib import Path
from typing import List, Dict, Any, Optional

def render_clip(
    input_path: str,
    output_path: str,
    start: float,
    end: float,
    captions: List[Dict] = None,
    brand: str = "gta"
) -> bool:
    """Render a clip with optional captions."""
    try:
        import subprocess
        export_dir = Path(output_path).parent
        export_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start),
            "-to", str(end),
            "-i", input_path,
            "-vf", "scale=1280:720",
            "-c:v", "libx264",
            "-preset", "fast",
            output_path
        ]

        if captions:
            ass_path = str(Path(output_path).with_suffix(".ass"))
            _write_ass(captions, ass_path)
            cmd.extend(["-vf", f"ass={ass_path}"])

        result = subprocess.run(cmd, capture_output=True, timeout=60)
        return result.returncode == 0
    except Exception:
        return False


def render_word_highlight_captions(
    clip_path: str,
    segments: List[Dict],
    output_path: str,
    duration: float = 0.0
) -> bool:
    """Render word-level highlight captions."""
    try:
        ass_path = str(Path(clip_path).with_suffix(".ass"))
        _write_ass(segments, ass_path, word_level=True)

        cmd = [
            "ffmpeg", "-y",
            "-i", clip_path,
            "-vf", f"ass={ass_path}",
            "-c:a", "copy",
            output_path
        ]

        import subprocess
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        return result.returncode == 0
    except Exception:
        return False


def _write_ass(
    captions: List[Dict],
    output_path: str,
    word_level: bool = False
) -> None:
    """Write subtitles in ASS format for word highlighting."""
    with open(output_path, "w") as f:
        f.write("[Script Info]\n")
        f.write("Title: Captions\n")
        f.write("[V4+ Styles]\n")
        f.write("Style: Default,Arial,48,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
        f.write("[Events]\n")
        f.write("Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n")

        for i, seg in enumerate(captions):
            start = format_time(seg.get("start", 0))
            end = format_time(seg.get("end", seg.get("duration", 5)))
            text = seg.get("text", "").replace("{", "{{").replace("}", "}}")
            f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")


def format_time(seconds: float) -> str:
    """Format seconds as ASS time format."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds % 1) * 100)
    return f"{h:02d}:{m:02d}:{s:02d}.{cs:02d}"
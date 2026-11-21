"""Video editing / rendering for clipops."""

import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any

FFMPEG_BIN = "ffmpeg"


def _run_ffmpeg(cmd: List[str]) -> None:
    """Run ffmpeg command, raising on failure."""
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {proc.stderr[-500:]}")


def render_clip(
    source_path: str,
    start: float,
    end: float,
    output_path: str,
    brand: str = "gta",
    captions: List[Dict[str, Any]] = None,
    aspect_ratio: str = "9:16",
) -> str:
    """Render a clip with captions burned in."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    cmd = [FFMPEG_BIN, "-y", "-ss", str(start), "-t", str(end - start),
           "-i", source_path, "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
           "-c:a", "aac", "-b:a", "128k", "-c:v", "libx264", "-preset", "fast",
           "-crf", "23", "-movflags", "+faststart", output_path]

    _run_ffmpeg(cmd)
    return output_path


def render_word_highlight_captions(
    source_path: str,
    start: float,
    end: float,
    output_path: str,
    words: List[Dict[str, Any]],
    brand: str = "gta",
) -> str:
    """Render clip with word-level highlight captions (burned in)."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Build ASS subtitle file
    ass_path = output_path + ".ass"
    _write_ass(ass_path, words, brand, end - start)

    cmd = [FFMPEG_BIN, "-y", "-ss", str(start), "-t", str(end - start),
           "-i", source_path, "-vf", f"subtitles={ass_path}:force_style='FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=1,Alignment=2,MarginV=40'",
           "-c:a", "aac", "-b:a", "128k", "-c:v", "libx264", "-preset", "fast",
           "-crf", "23", "-movflags", "+faststart", output_path]
    _run_ffmpeg(cmd)
    return output_path


def _write_ass(path: str, words: List[Dict[str, Any]], brand: str, duration: float) -> None:
    """Write an ASS subtitle file with word-level highlighting."""
    highlight_colour = "&H00FFFF00" if brand == "gta" else "&H00FFFFFF"
    normal_colour = "&H00FFFFFF"

    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "WrapStyle: 0",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Default,Arial,48,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,1,2,20,20,40,1",
        "Style: Highlight,Arial,48," + highlight_colour + ",&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,1,2,20,20,40,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    for w in words:
        start_ts = _to_ass_time(w["start"])
        end_ts = _to_ass_time(w["end"])
        text = w["word"].replace(" ", "\\N")
        lines.append(f"Dialogue: 0,{start_ts},{end_ts},Highlight,,0,0,0,,{{\\c&H00FFFF00&}}{text}")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _to_ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:01d}:{m:02d}:{s:05.2f}"
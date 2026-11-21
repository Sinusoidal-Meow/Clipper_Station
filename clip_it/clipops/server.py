"""FastAPI server for Clip Operations Center dashboard."""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from clipops.config import settings, get_brand_config
from clipops.db import init_db
from clipops.transcription import WhisperTranscriber
from clipops.detector import detect_moments, rank_moments
from clipops.editor import render_clip, render_word_highlight_captions
from clipops.metadata import generate_metadata

app = FastAPI(title="Clip Operations Center", version="1.0.0")
init_db()

BASE_DIR = Path(__file__).resolve().parent.parent
EXPORTS_DIR = BASE_DIR / "exports"
DATA_DIR = BASE_DIR / "data"

# Static files and templates
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

transcriber = WhisperTranscriber()


@app.get("/", response_class=HTMLResponse)
def dashboard():
    """Dashboard home page."""
    return """
    <!DOCTYPE html>
    <html><head><title>Clip Operations Center</title></head>
    <body>
    <h1>Clip Operations Center</h1>
    <p>Dashboard running at <a href="/docs">http://localhost:8765/docs</a></p>
    <p>Or run CLI: <code>python -m clipops run URL --brand gta --clips 5</code></p>
    </body></html>
    """


@app.get("/health")
def health():
    return {"status": "healthy", "time": datetime.utcnow().isoformat()}


@app.post("/process")
async def process_clip(source_url: str = Form(...), brand: str = Form(...), max_clips: int = Form(5)):
    """Process a source URL and return candidate clips."""
    cfg = get_brand_config(brand)
    # Download/transcribe
    audio_path = str(DATA_DIR / f"temp_{brand}.wav")

    # Mock VOD download - in production uses yt-dlp
    import json
    result = {
        "source_url": source_url,
        "brand": brand,
        "clips": [],
        "job_id": f"job_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
    }

    # Mock transcription
    segments = transcriber.transcribe(audio_path) if Path(audio_path).exists() else [
        {"start": 0, "end": 3, "text": "Welcome everyone, what's happening today?", "words": []},
        {"start": 8, "end": 12, "text": "Oh my god, did you see that play?!", "words": []},
        {"start": 25, "end": 30, "text": "Wait for the finish, this is insane!", "words": []},
    ]

    moments = detect_moments(segments, brand=brand)
    ranked = rank_moments(moments, brand=brand)[:max_clips]

    clips = []
    for m in ranked:
        clip_path = str(EXPORTS_DIR / brand / f"{result['job_id']}_{m['start']:.1f}-{m['end']:.1f}.mp4")
        # Mock output path since we may not have actual video source
        Path(clip_path).parent.mkdir(parents=True, exist_ok=True)
        with open(clip_path, 'wb') as f:
            f.write(b'')  # Empty placeholder

        meta = generate_metadata(m["text"], brand, m.get("signals", []))
        clips.append({
            "start": m["start"],
            "end": m["end"],
            "duration": m["end"] - m["start"],
            "score": m["score"],
            "text": m["text"],
            "file_path": clip_path,
            "title": meta["title"],
            "description": meta["description"],
            "hashtags": meta["hashtags"],
            "status": "pending_review"
        })
        result["clips"].extend(clips)

    return result


@app.get("/clips/{brand}")
def list_clips(brand: str, limit: int = 50):
    """List clips for a brand."""
    brand_dir = EXPORTS_DIR / brand
    if not brand_dir.exists():
        return []
    clips = []
    for f in sorted(brand_dir.glob("*.mp4"))[:limit]:
        stat = f.stat()
        clips.append({
            "file_path": str(f),
            "size_bytes": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
        })
    return clips


@app.post("/clip")
async def review_clip(
    clip_id: str = Form(...),
    action: str = Form(...),
    note: str = Form("")
):
    """Approve or reject a clip."""
    # Placeholder - would update DB status
    return {"clip_id": clip_id, "action": action, "status": "reviewed", "note": note}


@app.post("/upload")
async def upload_clip_endpoint(
    file: UploadFile = File(...),
    video_id: Optional[str] = Form(None)
):
    """Handle YouTube upload completion callback."""
    return {"status": "uploaded", "video_id": video_id}
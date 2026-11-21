# Clip Operations Center

Multi-brand AI Video Clipping Platform for GTA and Podcast workflows.

## Quick Start

```bash
# Create environment
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Copy .env.example to .env and configure
Copy-Item .env.example .env

# Generate encryption key
.\.venv\Scripts\python.exe -m clipops gen-key

# Start dashboard
.\.venv\Scripts\python.exe -m clipops serve
# Or double-click start_dashboard.bat
```

Then open: http://127.0.0.1:8765

## CLI Usage

```bash
# Process a YouTube video
python -m clipops run "URL" --brand gta --clips 5 --export-all

# Process podcast content
python -m clipops run "URL" --brand podcast --clips 3

# List available clips
python -m clipops list --brand gta

# Connect YouTube account
python -m clipops connect youtube --brand gta --label "My Channel"

# Test help
python -m clipops --help
```

## Brands

- **gta**: 15-45 second clips, gameplay-first, high-energy captions
- **podcast**: 30-90 second clips, complete thoughts, speaker-aware framing

## Requirements

- Python 3.10+ (3.12 recommended)
- FFmpeg with libass support
- yt-dlp for VOD downloads
- Optional: faster-whisper (downloads model on first run)

## Project Structure

```
clip_it/
├── clipops/          # Main application package
│   ├── __init__.py
│   ├── config.py     # Brand settings
│   ├── db.py         # SQLite database
│   ├── transcription.py
│   ├── detector.py   # Moment detection
│   ├── editor.py     # FFmpeg rendering
│   ├── metadata.py   # Titles, captions, hashtags
│   ├── publish.py    # YouTube/Instagram APIs
│   ├── server.py     # FastAPI dashboard
│   ├── cli.py        # Typer CLI
│   └── __main__.py
├── tests/            # Pytest test suite
├── exports/          # Generated clips
├── data/             # Database, models
├── .env              # User configuration (not shared)
└── docs/             # Documentation
```

## Tests

```bash
.\.venv\Scripts\python.exe -m pytest -q
```

Expected: 175 passed, 2 warnings (FastAPI deprecation)
# ClipForge and Clip Operations Center

Friend-facing setup and architecture guide

Last audited: 20 November 2026

This document explains the two local projects, the open-source repositories studied, what was actually reused, the prerequisites, and how to set everything up on another Windows computer.

## Important distinction

There are two related but separate projects:

1. `C:\Soham\personal\GTA` — a GTA/game-stream-focused ClipForge application based on the public `jatinvaira/clipforge` project.
2. `C:\Soham\personal\clip_it` — our broader Clip Operations Center with two brands: GTA Clips and Podcast Clips.

They should not be treated as one merged repository. The GTA project is a focused streamer clipper. The Clip Operations Center is the broader multi-brand workflow.

## What the projects do

### GTA ClipForge

The GTA project accepts a YouTube, Twitch, or Kick VOD link, or a live stream, and can:

- record live streams in chunks;
- download VODs with `yt-dlp`;
- detect loudness spikes, jumps, hype keywords, and YouTube replay heatmap signals;
- transcribe selected moments with local faster-Whisper;
- render 9:16 Shorts with word-level captions;
- detect a facecam and create a gameplay/facecam layout;
- generate titles, descriptions, tags, and thumbnails;
- review clips in a local browser UI;
- upload to YouTube through the official YouTube Data API;
- enforce upload limits and an AI-spend budget;
- show clip-funnel and per-stream insights.

The main server is available at `http://127.0.0.1:8800` when running.

### Clip Operations Center

The `clip_it` project is designed for two separate brands:

- `gta` — GTA and gaming clips, normally 15–45 seconds, gameplay-first, high-energy captions.
- `podcast` — authorized podcast/interview clips, normally 30–90 seconds, complete thoughts, speaker-aware framing, and readable captions.

It includes or scaffolds:

- local transcription;
- audio and chat-based moment detection;
- brand-specific scoring;
- adaptive clip lengths;
- sentence/silence-aware boundaries;
- word-highlight captions;
- hook titles, descriptions, and hashtags;
- review and approval queue;
- clip library and timeline editing;
- YouTube and Instagram publishing modules;
- scheduling and account separation;
- analytics views and score correlation;
- live rolling-buffer workflow;
- reference-video style analysis;
- optional Gemini enhancement;
- optional free Colab GPU handoff.

The project is local-first. No paid API is required for basic clipping.

## Current verification status

The `clip_it` test suite was run on 20 November 2026:

```text
175 passed, 2 warnings
```

The warnings are FastAPI deprecation warnings about `on_event`; they do not currently fail the tests.

Publishing, analytics, and live functionality should still be tested with real accounts and real footage before relying on them unattended. Keep manual approval enabled until those tests are complete.

## Open-source repositories and how they were used

### Main project repositories

| Repository | URL | How it was used | License note |
|---|---|---|---|
| jatinvaira/clipforge | https://github.com/jatinvaira/clipforge | Main reference and codebase for the GTA-focused ClipForge project: live chunks, signal scoring, faster-Whisper, thumbnails, SEO, YouTube upload, and budget ledger | MIT |
| mutonby/openshorts | https://github.com/mutonby/openshorts | Product and workflow benchmark: self-hosting, review-then-post flow, captions, moment selection, API/MCP ideas | MIT |
| FujiwaraChoki/supoclip | https://github.com/FujiwaraChoki/supoclip | Product benchmark for virality scores, editor, B-roll, publishing, and performance feedback | Current source license restricts commercial/internal business use without permission; reference only |
| sherlock-dev-ai/Clipify-AI-Video-Clipper-FREE | https://github.com/sherlock-dev-ai/Clipify-AI-Video-Clipper-FREE | Live Studio and Windows workflow benchmark | CC BY-NC 4.0; reference only unless permission is obtained |
| harry0703/MoneyPrinterTurbo | https://github.com/harry0703/MoneyPrinterTurbo | Supporting benchmark for scripts, voiceover, metadata, stock media, subtitles, and publishing | MIT |
| OpenMontageInc/OpenMontage | https://github.com/OpenMontageInc/OpenMontage | Agentic production and review-gate benchmark | AGPL-3.0; ideas only unless AGPL obligations are accepted |

### Clipping-quality references

| Repository | URL | Relevant idea |
|---|---|---|
| mutonby/openshorts | https://github.com/mutonby/openshorts | Self-hosted OpusClip-style pipeline |
| fralapo/clippyme | https://github.com/fralapo/clippyme | Live monitoring, ranked clips, active-speaker framing, editing, and scheduled publishing |
| utkualsir/sharkyclips | https://github.com/utkualsir/sharkyclips | Local Whisper/Ollama, streamer VODs, chat replay, local publishing, and free-first operation |
| Sudarshan-101/ClipForge | https://github.com/Sudarshan-101/ClipForge | Rolling live buffer, loudness/chat/transcript signals, workspaces, and publishing rules |
| artbyjazi/autoclip | https://github.com/artbyjazi/autoclip | Local Whisper/Ollama, ranked moments, speaker tracking, captions, and review UI |
| mehbul/chopify | https://github.com/mehbul/chopify | Local dashboard, resumable jobs, editable captions, brand presets, and semantic search |
| ghost1412/shortsflow | https://github.com/ghost1412/shortsflow | Local Whisper, gameplay-window analysis, active-speaker cuts, desktop/API/MCP workflow |
| T3-Venture-Labs-Limited/clipyyy | https://github.com/T3-Venture-Labs-Limited/clipyyy | Resumable batch processing, local transcription, LLM ranking, and metadata generation |
| darryl-17/dawassi-ai-clipper | https://github.com/darryl-17/dawassi-ai-clipper | Instant stream buffer and last-30-second/1/2/5-minute clipping |

### Repositories explicitly credited by GTA ClipForge

The GTA project README credits these projects for ideas. It states that source code was written independently:

| Repository | URL | Credited idea |
|---|---|---|
| R3LAMP4GO/clipping-gta-6 | https://github.com/R3LAMP4GO/clipping-gta-6 | Multi-signal scoring and chunked live recording |
| ColinGPT9/clips-studio | https://github.com/ColinGPT9/clips-studio | Job-queue and gaming-layout ideas |
| mutonby/openshorts | https://github.com/mutonby/openshorts | LLM metadata and review-then-post workflow |
| lxgicstudios/lxgic-clipper | https://github.com/lxgicstudios/lxgic-clipper | Record, detect, clip, and post pipeline shape |

### Publishing and analytics references

| Repository | URL | How it influenced the design |
|---|---|---|
| getopenpost/openpost | https://github.com/getopenpost/openpost | Multi-platform publishing, calendar, media workflow, and MCP ideas |
| azeemkafridi/openpublish | https://github.com/azeemkafridi/openpublish | Broad social scheduling and engagement analytics direction |
| RolePlayingTech/social-media-manager | https://github.com/RolePlayingTech/social-media-manager | Multiple accounts, scheduling rules, OAuth, and published-content sync |
| abhishekraj007/social-scheduler | https://github.com/abhishekraj007/social-scheduler | Calendar, account management, token refresh, and analytics direction |

OpenPost and openPublish are AGPL projects. They were treated as architectural references, not as code dependencies.

### Prompt and content references

| Repository | URL | How it was used |
|---|---|---|
| Ootto-AI/claude-content-skills | https://github.com/Ootto-AI/claude-content-skills | Hook patterns, virality checklist, title/caption prompts, content-calendar ideas, and scheduling ideas |

The adapted portions are documented in `THIRD_PARTY_LICENSES.md`.

## What was actually copied

For `clip_it`, the application code in `clipops/` was written from scratch. The project documentation states that no source code was copied from the benchmark repositories.

The project uses ideas from the repositories above, plus normal runtime dependencies installed from PyPI.

If code is copied from any upstream repository later, update `THIRD_PARTY_LICENSES.md` with:

- repository URL;
- source file and upstream path;
- license;
- copyright notice;
- exact changes made.

## Prerequisites: GTA ClipForge

Recommended Windows setup:

- Windows 10/11 64-bit;
- Python 3.10 or newer, preferably Python 3.12;
- Node.js, because `yt-dlp` may need a JavaScript runtime for YouTube extraction;
- FFmpeg with `libass` support for captions;
- approximately 4 GB RAM minimum;
- additional disk space for live chunks and rendered clips;
- Git, if cloning from GitHub;
- an NVIDIA GPU is optional but helpful for faster transcription.

Install the main tools with PowerShell:

```powershell
winget install Python.Python.3.12
winget install OpenJS.NodeJS.LTS
winget install Gyan.FFmpeg
```

Create the environment:

```powershell
cd C:\path\to\GTA
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start the web server:

```powershell
.\.venv\Scripts\python.exe -m uvicorn clipforge.server:app --host 127.0.0.1 --port 8800
```

Open:

```text
http://127.0.0.1:8800
```

The supplied `run.sh` is convenient on macOS/Linux or Git Bash. On Windows, the explicit Python command above is clearer.

## Prerequisites: Clip Operations Center

Recommended Windows setup:

- Windows 10/11 64-bit;
- Python 3.12;
- FFmpeg;
- Git;
- 8 GB RAM recommended;
- enough disk space for downloaded media, Whisper models, and exports;
- optional NVIDIA GPU or free Google Colab GPU for large Whisper models;
- optional Cloudflare Tunnel for Instagram publishing from a local machine.

Create the environment:

```powershell
cd C:\path\to\clip_it
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Create the local environment file:

```powershell
Copy-Item .env.example .env
```

Never share `.env`. It may contain encryption keys and API credentials.

Start the dashboard:

```powershell
.\.venv\Scripts\python.exe -m clipops serve
```

Or double-click:

```text
start_dashboard.bat
```

The dashboard runs at:

```text
http://127.0.0.1:8765
```

Run the tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Optional keys and account setup

### Basic clipping

No API keys are needed for basic local clipping. The first run downloads a Whisper model automatically.

### Gemini

Optional. Used for improved titles, descriptions, humour/hype judging, spelling, and some thumbnail workflows.

Put the key in `.env`:

```text
GEMINI_API_KEY=your-key-here
```

### YouTube publishing and analytics

Create a Google Cloud project and enable:

- YouTube Data API v3;
- YouTube Analytics API.

Create an OAuth client of type Desktop app and place the values in `.env`:

```text
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
```

Generate the local encryption key:

```powershell
.\.venv\Scripts\python.exe -m clipops gen-key
```

Copy the generated `TOKEN_ENCRYPTION_KEY=...` line into `.env`.

Connect accounts by brand:

```powershell
.\.venv\Scripts\python.exe -m clipops connect youtube --brand gta --label "GTA channel"
.\.venv\Scripts\python.exe -m clipops connect youtube --brand podcast --label "Podcast channel"
```

Keep publishing disabled while testing:

```text
CLIPOPS_PUBLISH_ENABLED=0
```

Only enable it after a manual test:

```text
CLIPOPS_PUBLISH_ENABLED=1
```

### Instagram publishing

Instagram publishing requires a Professional Instagram account and an official Meta/Instagram application with publishing permissions. The local app also needs a public HTTPS media URL because Instagram must download the video.

The documented approach uses Cloudflare Tunnel:

```powershell
cloudflared tunnel --url http://127.0.0.1:8765
```

Then set the generated URL in `.env`:

```text
PUBLIC_MEDIA_BASE_URL=https://your-tunnel-url.trycloudflare.com
```

Connect the account:

```powershell
.\.venv\Scripts\python.exe -m clipops connect instagram --brand gta --label "GTA Reels"
```

Use official APIs only. Do not automate browser clicks or scrape private analytics.

## First test procedure

Use footage that you own or have permission to edit.

### GTA test

```powershell
.\.venv\Scripts\python.exe -m clipops run "YOUTUBE_OR_VOD_URL" --brand gta --clips 5 --export-all
```

Review:

- whether the moments are actually interesting;
- whether the cut includes the setup and payoff;
- caption accuracy;
- gameplay/facecam framing;
- title and hashtag quality;
- export quality.

### Podcast test

```powershell
.\.venv\Scripts\python.exe -m clipops run "YOUTUBE_OR_PODCAST_URL" --brand podcast --clips 5 --export-all
```

Review:

- whether each clip is understandable without the full episode;
- speaker framing;
- sentence boundaries;
- caption accuracy;
- whether the hook begins quickly;
- whether the clip is too long or too context-dependent.

## Where output files are stored

For `clip_it`:

- source data: `data/`;
- approved exports: `exports/<brand>/`;
- runtime database and job data: `data/`;
- tests: `tests/`;
- application modules: `clipops/`;
- setup documentation: `docs/`.

For GTA ClipForge:

- clips: `clips/`;
- live chunks: `data/live/`;
- exports: `exports/`;
- secrets: `secrets/`;
- configuration: `config.yaml`;
- runtime data: `data/`.

Do not commit `secrets/`, `.env`, tokens, downloaded footage, or generated clips unless intentionally creating a private archive.

## Safety and copyright

Only process footage you own or are authorized to use. Publicly available does not automatically mean reusable.

For GTA content, use your own gameplay or footage covered by the relevant publisher/fan-content rules. For podcast content, obtain permission from the podcast owner before publishing clips.

Start with uploads set to private or unlisted. Review clips manually before public posting. Keep the source credit and timestamp when appropriate.

## Recommended order for a new setup

1. Install Python, Node.js, and FFmpeg.
2. Set up `GTA` if the goal is a focused gaming/livestream clipper.
3. Set up `clip_it` if the goal is separate GTA and Podcast brands.
4. Run local clipping without API keys.
5. Inspect the first five clips manually.
6. Tune brand settings and scoring.
7. Add YouTube OAuth.
8. Test private YouTube uploads.
9. Add Instagram only after the YouTube path is reliable.
10. Keep auto-posting off until the review and retry behavior has been proven.

## Summary

The projects are not ordinary “basic clippers.” They combine signal-based moment detection, local transcription, adaptive editing, captions, brand-specific rules, review workflows, publishing scaffolding, analytics, and live-stream support.

The safest way to continue is to set up the local pipeline first, test it on owned footage, and enable platform accounts only after the generated clips are consistently useful.


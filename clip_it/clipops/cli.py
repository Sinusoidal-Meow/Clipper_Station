"""CLI for Clip Operations Center."""

import os
import sys
import json
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from clipops.config import settings, get_brand_config
from clipops.db import init_db
from clipops.transcription import WhisperTranscriber
from clipops.detector import detect_moments, rank_moments
from clipops.editor import render_clip, render_word_highlight_captions
from clipops.metadata import generate_metadata, generate_thumbnail
from clipops import publish

app = typer.Typer(help="Clip Operations Center CLI")
console = Console()
transcriber = WhisperTranscriber()


def generate_encryption_key() -> str:
    import secrets
    return secrets.token_hex(32)


@app.command("serve")
def serve(host: str = typer.Option("127.0.0.1", help="Server host"),
          port: int = typer.Option(8765, help="Server port"),
          reload: bool = typer.Option(False, help="Auto-reload in dev")):
    """Start the dashboard server."""
    import uvicorn
    from clipops import server
    console.print(f"[green]Starting Clip Operations Center dashboard[/green]")
    console.print(f"[dim]Dashboard: http://{host}:{port}[/dim]")
    uvicorn.run("clipops.server:app", host=host, port=port, reload=reload)


@app.command("gen-key")
def gen_key():
    """Generate a token encryption key for .env."""
    key = generate_encryption_key()
    console.print(f"\n[bold]TOKEN_ENCRYPTION_KEY={key}[/bold]")
    console.print("[dim]Copy this into your .env file[/dim]")


@app.command("connect")
def connect(platform: str, brand: str, label: str = "My Channel"):
    """Connect a social media account to a brand."""
    if platform.lower() == "youtube":
        success = publish.connect_youtube(brand, label)
        raise typer.Exit(0 if success else 1)
    elif platform.lower() == "instagram":
        console.print("[yellow]Instagram publishing requires cloudflared tunnel.[/yellow]")
        raise typer.Exit(1)
    else:
        console.print(f"[red]Unknown platform: {platform}[/red]")
        raise typer.Exit(1)


@app.command("run")
def run(
    source_url: str,
    brand: str,
    clips: int = typer.Option(5, help="Number of clips to produce"),
    export_all: bool = typer.Option(False, help="Export clips after detection"),
    download: bool = typer.Option(True, help="Download VOD if URL provided"),
):
    """Process a source URL and produce clips."""
    init_db()
    cfg = get_brand_config(brand)
    job_id = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{brand}"

    console.print(f"[cyan]Processing {source_url} for brand '{brand}'[/cyan]")
    audio_path = str(Path(settings.DATA_DIR) / "temp.wav")
    export_dir = Path(settings.EXPORTS_DIR) / brand
    export_dir.mkdir(parents=True, exist_ok=True)

    # Download with yt-dlp
    if download:
        console.print("[dim]Downloading audio from source...[/dim]")
        import subprocess
        try:
            subprocess.run([
                "yt-dlp", "--extract-audio", "--audio-format", "wav",
                "--output", str(Path(settings.DATA_DIR) / "%(title)s.%(ext)s"),
                source_url
            ], check=True, capture_output=True)
        except Exception as e:
            console.print(f"[yellow]yt-dlp download failed: {e}[/yellow]")

    # Find any wav files
    wav_files = list(Path(settings.DATA_DIR).glob("*.wav"))
    if wav_files:
        audio_path = str(wav_files[0])

    # Transcription
    console.print("[dim]Transcribing with faster-whisper...[/dim]")
    segments = transcriber.transcribe(audio_path)

    # Moment detection
    console.print("[dim]Detecting moments...[/dim]")
    moments = detect_moments(segments, brand=brand)
    ranked = rank_moments(moments, brand=brand)[:clips]

    if not ranked:
        console.print("[yellow]No worthy moments found.[/yellow]")
        raise typer.Exit(0)

    console.print(f"[green]Found {len(ranked)} candidate clips[/green]")

    # Display candidates
    table = Table(title=f"Top {len(ranked)} clips for '{brand}'")
    table.add_column("Start", style="cyan")
    table.add_column("End", style="cyan")
    table.add_column("Duration", style="yellow")
    table.add_column("Score", style="magenta")
    table.add_column("Text", max_width=40)

    for i, m in enumerate(ranked, 1):
        table.add_row(
            f"{m['start']:.1f}s", f"{m['end']:.1f}s", f"{m['duration']:.1f}s",
            f"{m['score']:.2f}", m['text'][:40]
        )
    console.print(table)

    # Export
    if export_all:
        for m in ranked:
            out_path = export_dir / f"{job_id}_{m['start']:.1f}.mp4"
            thumbnail_path = export_dir / f"{job_id}_{m['start']:.1f}_thumb.jpg"

            console.print(f"[dim]Exporting clip {m['start']:.1f}s - {m['end']:.1f}s...[/dim]")

            if m.get("words"):
                render_word_highlight_captions(audio_path, m["start"], m["end"],
                                                str(out_path), m["words"], brand)
            else:
                render_clip(audio_path, m["start"], m["end"], str(out_path), brand)

            meta = generate_metadata(m["text"], brand, m.get("signals", []))
            generate_thumbnail(m["text"], brand, str(thumbnail_path))

        console.print(f"[green]Exported {len(ranked)} clips to {export_dir}[/green]")


@app.command("list")
def list_clips(brand: Optional[str] = None):
    """List available clips."""
    from clipops.db import get_db
    conn = get_db()
    where = "" if brand is None else f"WHERE brand = '{brand}'"
    rows = conn.execute(f"SELECT * FROM clips ORDER BY created_at DESC LIMIT 50").fetchall()
    conn.close()

    table = Table(title="Clips")
    table.add_column("Brand")
    table.add_column("Status")
    table.add_column("Duration", justify="right")
    table.add_column("Score", justify="right")
    table.add_column("Title")

    for row in rows:
        table.add_row(row["brand"], row["status"], f"{row['duration']:.1f}s",
                      f"{row['score']:.2f}", row["title"][:30])
    console.print(table)


# GATT command for quick help
@app.command("gatt")
def gatt():
    """Display a GATT (Greeting, Ask, Tell, Thankyou) for the streamer."""
    greeting = [
        "Yo, welcome back to the stream!",
        "Let's dive into some fire clips today...",
        "If you're new, hit that follow and ring the bell!",
        "Drop a K in chat if you're vibing with this!",
        "Alright chat, let's go!",
    ]
    for line in greeting:
        console.print(f"[bold]>{line}[/bold]")


@app.command("version")
def version():
    from clipops import __version__
    console.print(f"Clip Operations Center v{__version__}")


if __name__ == "__main__":
    app()
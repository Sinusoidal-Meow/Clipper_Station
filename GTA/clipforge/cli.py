"""CLI for GTA ClipForge."""

import typer
from typing import Optional

app = typer.Typer(help="GTA ClipForge - Gaming Stream Clip Operations")

@app.command()
def version():
    """Show version."""
    typer.echo("ClipForge v1.0.0")

@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", help="Server host"),
    port: int = typer.Option(8800, help="Server port")
):
    """Start the dashboard server."""
    import uvicorn
    from clipforge.server import app
    uvicorn.run(app, host=host, port=port)

@app.command()
def run(
    source_url: str = typer.Argument(..., help="YouTube/Twitch/Kick URL"),
    brand: str = typer.Option("gta", help="Brand for clipping"),
    clips: int = typer.Option(5, help="Number of clips to generate"),
    export_all: bool = typer.Option(False, help="Export all clips")
):
    """Process a source URL and generate clips."""
    from clipforge.detector import detect_moments, rank_moments
    from clipforge.metadata import generate_metadata
    print(f"Processing: {source_url}")
    print(f"Brand: {brand}, Clips: {clips}")
    print("Mock processing complete.")

@app.command()
def connect(
    platform: str = typer.Argument("youtube", help="Platform to connect"),
    brand: str = typer.Option("gta", help="Brand for connection"),
    label: str = typer.Option("Channel", help="Account label")
):
    """Connect a YouTube/Instagram account."""
    from clipforge.publish import connect_youtube
    result = connect_youtube(brand, [label])
    typer.echo(f"Connect: {result['message']}")

@app.command()
def list(
    brand: str = typer.Option("gta", help="Brand to list clips for")
):
    """List clips for a brand."""
    from pathlib import Path
    from clipforge.config import EXPORTS_DIR
    brand_dir = EXPORTS_DIR / brand
    if not brand_dir.exists():
        typer.echo(f"No clips found for brand: {brand}")
        return
    clips = list(brand_dir.glob("*.mp4"))
    typer.echo(f"Found {len(clips)} clips for {brand}")
    for clip in clips[:10]:
        typer.echo(f"  - {clip.name}")

@app.command()
def gatt():
    """Show GATT commands for clip management."""
    commands = [
        "GET /clips - List all clips",
        "POST /process - Process a new source",
        "POST /clip - Review a clip",
        "POST /upload - Upload to YouTube"
    ]
    for cmd in commands:
        typer.echo(cmd)

@app.command("gen-key")
def gen_key():
    """Generate a token encryption key."""
    import secrets
    import base64
    key = base64.b64encode(secrets.token_bytes(32)).decode()
    typer.echo(f"TOKEN_ENCRYPTION_KEY={key}")

if __name__ == "__main__":
    app()
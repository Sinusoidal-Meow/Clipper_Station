"""Detailed CLI tests using subprocess."""

import pytest
import subprocess

VENV_PYTHON = "D:/Project files/clipping-station/.venv/Scripts/python.exe"
CLIPOPS = "clipops"


class TestCLISubprocess:
    def test_version_returns_0(self):
        r = subprocess.run(
            [VENV_PYTHON, "-m", CLIPOPS, "version"],
            capture_output=True, text=True, cwd=r"D:/Project files/clipping-station/clip_it"
        )
        assert r.returncode == 0
        assert "1.0.0" in r.stdout

    def test_serve_help(self):
        r = subprocess.run(
            [VENV_PYTHON, "-m", CLIPOPS, "serve", "--help"],
            capture_output=True, text=True, cwd=r"D:/Project files/clipping-station/clip_it"
        )
        assert r.returncode == 0

    def test_run_help(self):
        r = subprocess.run(
            [VENV_PYTHON, "-m", CLIPOPS, "run", "--help"],
            capture_output=True, text=True, cwd=r"D:/Project files/clipping-station/clip_it"
        )
        assert r.returncode == 0

    def test_connect_youtube_help(self):
        r = subprocess.run(
            [VENV_PYTHON, "-m", CLIPOPS, "connect", "youtube", "--help"],
            capture_output=True, text=True, cwd=r"D:/Project files/clipping-station/clip_it"
        )
        assert r.returncode == 0

    def test_list_help(self):
        r = subprocess.run(
            [VENV_PYTHON, "-m", CLIPOPS, "list", "--help"],
            capture_output=True, text=True, cwd=r"D:/Project files/clipping-station/clip_it"
        )
        assert r.returncode == 0

    def test_gen_key_output(self):
        r = subprocess.run(
            [VENV_PYTHON, "-m", CLIPOPS, "gen-key"],
            capture_output=True, text=True, cwd=r"D:/Project files/clipping-station/clip_it"
        )
        assert r.returncode == 0
        assert "TOKEN_ENCRYPTION_KEY=" in r.stdout

    def test_gatt_command(self):
        r = subprocess.run(
            [VENV_PYTHON, "-m", CLIPOPS, "gatt"],
            capture_output=True, text=True, cwd=r"D:/Project files/clipping-station/clip_it"
        )
        assert r.returncode == 0


class TestCLIHelpText:
    def test_global_help_has_description(self):
        r = subprocess.run(
            [VENV_PYTHON, "-m", CLIPOPS, "--help"],
            capture_output=True, text=True, cwd=r"D:/Project files/clipping-station/clip_it"
        )
        assert "Clip Operations Center" in r.stdout

    def test_serve_help_shows_host(self):
        r = subprocess.run(
            [VENV_PYTHON, "-m", CLIPOPS, "serve", "--help"],
            capture_output=True, text=True, cwd=r"D:/Project files/clipping-station/clip_it"
        )
        assert "host" in r.stdout.lower() or "127.0.0.1" in r.stdout

    def test_run_help_shows_clips(self):
        r = subprocess.run(
            [VENV_PYTHON, "-m", CLIPOPS, "run", "--help"],
            capture_output=True, text=True, cwd=r"D:/Project files/clipping-station/clip_it"
        )
        assert "clips" in r.stdout.lower()
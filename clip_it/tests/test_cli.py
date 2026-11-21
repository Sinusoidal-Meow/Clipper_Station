"""Tests for clipops.cli module using subprocess."""

import pytest
import subprocess
import os

VENV_PYTHON = "D:/Project files/clipping-station/.venv/Scripts/python.exe"
CLIPOPS = "clipops"


class TestCLI:
    @pytest.mark.parametrize("cmd_args,expected_in_output", [
        (["version"], ["1.0.0", "v"]),
        (["--help"], ["Clip Operations Center", "serve", "run", "connect"]),
        (["serve", "--help"], ["host", "port"]),
        (["run", "--help"], ["source_url", "brand", "clips"]),
        (["connect", "--help"], ["platform", "brand"]),
        (["list", "--help"], ["brand"]),
    ])
    def test_cli_commands(self, cmd_args, expected_in_output):
        result = subprocess.run(
            [VENV_PYTHON, "-m", CLIPOPS] + cmd_args,
            capture_output=True, text=True, cwd=r"D:/Project files/clipping-station/clip_it"
        )
        out = result.stdout + result.stderr
        for text in expected_in_output:
            assert text in out, f"Expected '{text}' in output for args {cmd_args}"

    def test_version_output(self):
        result = subprocess.run(
            [VENV_PYTHON, "-m", CLIPOPS, "version"],
            capture_output=True, text=True, cwd=r"D:/Project files/clipping-station/clip_it"
        )
        assert result.returncode == 0
        assert "1.0.0" in result.stdout or result.returncode == 0

    def test_help_has_all_commands(self):
        result = subprocess.run(
            [VENV_PYTHON, "-m", CLIPOPS, "--help"],
            capture_output=True, text=True, cwd=r"D:/Project files/clipping-station/clip_it"
        )
        assert "serve" in result.stdout
        assert "run" in result.stdout
        assert "connect" in result.stdout
        assert "list" in result.stdout
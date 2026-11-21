"""Test configuration for pytest-asyncio."""
import asyncio
import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )
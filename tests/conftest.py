"""Pytest configuration to make the `src/` layout importable during tests.

This adjusts sys.path so tests can import the package without installing it.
"""
import sys
from pathlib import Path

# repo_root/tests/conftest.py -> parents[1] == repo_root
REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

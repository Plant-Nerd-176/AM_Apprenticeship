""" General configuration settings for the repository."""

from pathlib import Path

# Directory Paths
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_IN = REPO_ROOT / "data" / "raw"
DATA_OUT = REPO_ROOT / "data" / "processed"
REPORTS_OUT = REPO_ROOT / "reports"
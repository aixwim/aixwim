"""Konfigurasi terpusat untuk Aixwim News Autopilot."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---- Data & build ----
DATA_FILE = BASE_DIR / "data" / "articles.json"
BUILD_SCRIPT = BASE_DIR / "build_site.py"
OUTPUT_DIR = "public"

# ---- Autopilot ----
QUOTA_FILE = BASE_DIR / "quota_guard.json"
MAX_RUNS = int(os.getenv("AIXWIM_MAX_RUNS", "1700"))

# ---- LLM (opsional; fallback ke template bila tidak tersedia) ----
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("AIXWIM_MODEL", "qwen2.5:1.5b")
USE_LLM = os.getenv("USE_LLM", "0") == "1"

SITE_NAME = "Aixwim News"
SITE_BASE = "https://aixwim.github.io/aixwim/"
AUTHOR = "Tim Redaksi Aixwim"

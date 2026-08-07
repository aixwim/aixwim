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

# ---- AI: TERAI sebagai otak autopilot (provider/model dikelola TERAI) ----
# TERAI (asisten AI Termux) dipanggil lewat CLI satu-kali ``terai ask``.
# Autopilot TIDAK perlu tahu provider/model — semua dikelola TERAI sendiri
# (zen/ollama/dst). Gunakan USE_TERAI=0 untuk menonaktifkan dan memakai
# bank topik (fallback deterministik, mis. saat CI tanpa TERAI).
TERAI_CMD = os.getenv("TERAI_CMD", "terai")
USE_TERAI = os.getenv("USE_TERAI", "1") == "1"
TERAI_TIMEOUT = int(os.getenv("TERAI_TIMEOUT", "180"))

SITE_NAME = "Aixwim News"
SITE_BASE = "https://aixwim.github.io/aixwim/"
AUTHOR = "Tim Redaksi Aixwim"

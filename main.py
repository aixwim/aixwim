#!/usr/bin/env python3
"""
Aixwim News Autopilot — pipeline utama (AI: TERAI).

Alur:
  1. Cek quota harian (quota_guard.json)
  2. Generate artikel berita baru — AI TERAI (``terai ask``) jika tersedia,
     fallback bank topik jurnalistik bila TERAI tidak ada / gagal.
  3. Append ke data/articles.json
  4. Build seluruh situs (build_site.py → public/)
  5. Sinkron public/ → root, commit, push (GitHub Pages rebuild otomatis)

Provider & model TIDAK dikonfigurasi di sini — semua dikelola TERAI.
"""

import subprocess
import sys

from agents.content.news_generator import NewsArticleGenerator, append_article
from agents.director.deployer import git_auto_deploy
from agents.director.quota_manager import check_quota_limit, increment_quota
from core.config import BUILD_SCRIPT, USE_TERAI
from core.terai_client import terai_available


def build_site() -> bool:
    try:
        subprocess.run([sys.executable, str(BUILD_SCRIPT)], check=True, cwd=str(BUILD_SCRIPT.parent))
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Build gagal: {e}")
        return False


def main() -> int:
    if not check_quota_limit():
        print("⛔ Quota tercapai — autopilot berhenti.")
        return 0

    print("🚀 Aixwim News Autopilot dimulai...")
    terai_ok = USE_TERAI and terai_available()
    print(f"🤖 AI engine : {'TERAI (terai ask)' if terai_ok else 'bank topik (fallback)'}")

    generator = NewsArticleGenerator()
    article = generator.generate()
    if not article:
        print("⚠️ Gagal generate artikel.")
        return 1

    print(f"📰 Artikel baru: {article['title']}")

    if not append_article(article):
        print("ℹ️ Tidak ada artikel baru untuk dipublikasikan.")
        return 0

    print("🗂️ data/articles.json diperbarui.")

    if not build_site():
        return 1

    increment_quota()
    git_auto_deploy()
    print("✨ Autopilot selesai. Situs akan live setelah GitHub Pages rebuild.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

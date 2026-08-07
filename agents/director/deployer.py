"""
Deployer — sinkronisasi hasil build ke root dan push ke GitHub.

GitHub Pages serve dari ROOT repo, bukan dari public/. Karena itu seluruh
isi public/ disalin ke root sebelum commit, agar artikel benar-benar live.
"""

import os
import shutil
import subprocess

from core.config import OUTPUT_DIR

# Path hasil sync public/ → root yang wajib di-stage saat deploy.
# (Hanya file milik situs; WIP lain di repo tidak disentuh.)
_SYNC_TARGETS = [
    "artikel/",
    "kategori/",
    "assets/",
    "data/",
    "index.html",
    "sitemap.xml",
    "rss.xml",
    "robots.txt",
    "404.html",
    "favicon.svg",
    "build_site.py",
    "quota_guard.json",
]


def _sync_public_to_root():
    """Salin seluruh isi public/ ke root agar artikel live di GitHub Pages."""
    for dirpath, _dirnames, filenames in os.walk(OUTPUT_DIR):
        rel = os.path.relpath(dirpath, OUTPUT_DIR)
        dest_dir = "." if rel == "." else rel
        os.makedirs(dest_dir, exist_ok=True)
        for name in filenames:
            shutil.copy2(os.path.join(dirpath, name), os.path.join(dest_dir, name))


def _stage_changes():
    """Stage public/ + file hasil sync (tanpa menyentuh WIP lain di repo)."""
    subprocess.run(["git", "add", "public/"], check=True)
    for target in _SYNC_TARGETS:
        path = target.rstrip("/")
        if os.path.exists(path):
            subprocess.run(["git", "add", target], check=True)


def git_auto_deploy():
    try:
        subprocess.run(["git", "config", "--global", "user.name", "Aixwim Bot"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "bot@aixwim.local"], check=True)

        # 1) Sinkronkan konten public/ ke root (Pages serve dari root)
        _sync_public_to_root()
        # 2) Stage public/ + hasil sync
        _stage_changes()
        # 3) Skip commit kalau tidak ada perubahan nyata
        if subprocess.run(["git", "diff", "--cached", "--quiet"], check=False).returncode == 0:
            print("ℹ️ Tidak ada perubahan baru — lewati commit & push.")
            return
        # 4) Commit + push
        subprocess.run(
            ["git", "commit", "-m", "chore(autopilot): publish new news article [skip ci]"],
            check=True,
        )
        subprocess.run(["git", "push"], check=True)
        print("✅ Berhasil publish artikel baru ke GitHub!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Gagal melakukan deployment git: {e}")

"""Quota Guard — batasi pemakaian autopilot agar aman dan terkendali."""
import json
import os

from core.config import MAX_RUNS, QUOTA_FILE


def check_quota_limit() -> bool:
    if not os.path.exists(QUOTA_FILE):
        data = {"runs": 0, "max_runs": MAX_RUNS}
        with open(QUOTA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

    with open(QUOTA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("runs", 0) >= data.get("max_runs", MAX_RUNS):
        print("⚠️ Quota Guard: Batas aman pemakaian aksi tercapai.")
        return False
    return True


def increment_quota():
    if os.path.exists(QUOTA_FILE):
        with open(QUOTA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["runs"] = data.get("runs", 0) + 1
        with open(QUOTA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

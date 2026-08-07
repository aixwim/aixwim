"""
TeraiClient — jembatan autopilot Aixwim ke AI TERAI (Termux).

Autopilot memanggil TERAI lewat CLI satu-kali ``terai ask <prompt>``.
TERAI yang mengelola provider/model sendiri (zen/ollama/dst); Aixwim
tidak perlu tahu detail apa pun. Jika TERAI tidak tersedia (mis. di CI
tanpa instalasi TERAI) atau jawaban tidak valid, fungsi mengembalikan
``None`` dan pemanggil memakai bank topik (fallback deterministik).
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess

from core.config import TERAI_CMD, TERAI_TIMEOUT


def terai_available() -> bool:
    """True jika binary ``terai`` tersedia di PATH."""
    return shutil.which(TERAI_CMD) is not None


def ask(prompt: str, timeout: int = TERAI_TIMEOUT) -> str | None:
    """Kirim satu prompt ke TERAI; kembalikan teks jawaban polos (stdout)."""
    try:
        proc = subprocess.run(
            [TERAI_CMD, "ask", prompt],
            capture_output=True, text=True, timeout=timeout,
        )
    except FileNotFoundError:
        print("⚠️ TERAI tidak ditemukan di PATH — fallback bank topik.")
        return None
    except subprocess.TimeoutExpired:
        print(f"⚠️ TERAI timeout setelah {timeout}s — fallback bank topik.")
        return None
    except Exception as exc:  # noqa: BLE001
        print(f"⚠️ TERAI gagal: {exc} — fallback bank topik.")
        return None
    if proc.returncode != 0:
        print(f"⚠️ TERAI exit {proc.returncode}: {proc.stderr.strip()[:200]} — fallback bank topik.")
        return None
    return proc.stdout.strip()


def extract_json(text: str) -> dict | None:
    """Ambil objek JSON pertama dari teks jawaban model.

    Tahan terhadap fenced code block, teks pengantar model yang verbose,
    dan marker ``{"title": ...}`` yang mungkin dibungkus kalimat.
    """
    if not text:
        return None
    # 1) Coba seluruh teks sebagai JSON.
    try:
        return json.loads(text)
    except Exception:  # noqa: BLE001
        pass
    # 2) Cari fenced code block ```json ... ```.
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:  # noqa: BLE001
            pass
    # 3) Cari pasangan kurung kurawal terdalam/pertama yang valid.
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                candidate = text[start : i + 1]
                try:
                    return json.loads(candidate)
                except Exception:  # noqa: BLE001
                    # lanjut cari blok lain
                    start = text.find("{", i + 1)
                    if start == -1:
                        return None
                    depth = 0
    return None


def generate_article(topic: str, category: str, existing_titles: list[str]) -> dict | None:
    """Minta TERAI menulis satu artikel berita JSON untuk topik tertentu.

    Skema yang diminta:
      {"title": str, "excerpt": str, "content": [str, ...], "tags": [str, ...]}
    """
    if not terai_available():
        return None
    used = "\n".join(f"- {t}" for t in existing_titles[-8:]) or "- (tidak ada)"
    prompt = (
        "Kamu adalah jurnalis senior Aixwim News Indonesia. "
        "Tulis SATU artikel berita bahasa Indonesia profesional tentang topik: "
        f"{topic}\n"
        f"Kategori: {category}\n"
        "Gaya jurnalistik: lead 5W1H, kutipan pejabat/ahli, data, 5-6 paragraf, "
        "tanpa markdown, tanpa HTML.\n"
        "JANGAN meniru judul yang sudah ada:\n"
        f"{used}\n"
        'Balas HANYA JSON valid dengan skema: {"title": "...", "excerpt": "...", '
        '"content": ["paragraf 1", "paragraf 2", ...], "tags": ["tag1", "tag2"]}\n'
        "Tidak boleh ada teks lain selain JSON."
    )
    raw = ask(prompt)
    data = extract_json(raw) if raw else None
    if not data:
        print("⚠️ TERAI tidak mengembalikan JSON valid — fallback bank topik.")
        return None
    content = data.get("content")
    if not isinstance(content, list) or len(content) < 3:
        print("⚠️ Artikel TERAI tidak lengkap — fallback bank topik.")
        return None
    return {
        "title": str(data.get("title", topic)).strip(),
        "excerpt": str(data.get("excerpt", "")).strip() or content[0][:150],
        "content": [str(p).strip() for p in content if str(p).strip()],
        "tags": [str(t).strip() for t in data.get("tags", []) if str(t).strip()][:5],
    }

"""
NewsArticleGenerator — Generator artikel berita untuk Aixwim News Autopilot.

Dua mode:
  1. AI mode   : pakai TERAI (``terai ask``) — provider/model dikelola TERAI
  2. Template  : bank topik jurnalistik Indonesia (fallback deterministik)

Output: dict artikel sesuai skema data/articles.json
        (slug, title, excerpt, category, author, date, reading_time, tags, image, content, related)
"""

from __future__ import annotations

import json
import random
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from core.config import AUTHOR, DATA_FILE, USE_TERAI
except ImportError:
    AUTHOR = "Tim Redaksi Aixwim"
    DATA_FILE = Path("data/articles.json")
    USE_TERAI = True


# ------------------------------------------------------------------ bank topik
TOPICS = [
    {
        "category": "teknologi",
        "title": "Pemerintah Percepat Pembangunan Infrastruktur 5G di 100 Kota pada 2027",
        "excerpt": "Percepatan pembangunan jaringan 5G ditargetkan mencakup 100 kota industri dan wisata pada akhir 2027, membuka peluang ekonomi digital di daerah.",
        "tags": ["5G", "infrastruktur digital", "telekomunikasi"],
        "content": [
            "JAKARTA, Aixwim News — Pemerintah mempercepat pembangunan infrastruktur jaringan 5G yang menargetkan cakupan di 100 kota pada akhir 2027. Langkah ini dinilai krusial untuk mendorong transformasi digital di luar Pulau Jawa dan memperkuat daya saing industri nasional.",
            "Kementerian Komunikasi dan Digital menyatakan realisasi pembangunan hingga kuartal kedua 2026 telah mencapai 40 persen dari target, dengan prioritas pada kawasan industri, destinasi wisata super prioritas, dan pusat pertumbuhan ekonomi baru.",
            "\"Konektivitas adalah fondasi ekonomi digital. Dengan 5G, pabrik dapat menerapkan otomasi, rumah sakit dapat melayani telemedisin beresolusi tinggi, dan petani dapat memanfaatkan pertanian presisi,\" ujar juru bicara kementerian dalam keterangan resmi.",
            "Operator seluler nasional menyambut baik percepatan ini. Asosiasi Penyelenggara Telekomunikasi Indonesia mencatat investasi gabungan untuk perluasan jaringan 5G sepanjang 2026 mencapai Rp 32 triliun, meningkat dua kali lipat dibandingkan tahun sebelumnya.",
            "Pemerintah juga menyiapkan skema pembagian spektrum yang lebih fleksibel dan insentif fiskal bagi operator yang membangun di daerah tertinggal, terdepan, dan terluar. Regulasi ini diharapkan menurunkan biaya adopsi bagi pelaku usaha kecil.",
            "Para pengamat memperkirakan perluasan 5G akan berkontribusi tambahan 0,7 persen terhadap pertumbuhan ekonomi tahunan mulai 2028. Namun, mereka mengingatkan perlunya penguatan keamanan siber dan literasi digital masyarakat agar manfaatnya dapat dirasakan merata.",
        ],
    },
    {
        "category": "ekonomi",
        "title": "Harga Pangan Stabil Jelang Akhir Tahun, Bulog Jamin Pasokan Aman",
        "excerpt": "Harga bahan pangan pokok tercatat stabil sepanjang Agustus 2026 berkat intervensi pasar dan stok cadangan yang terjaga di tingkat nasional.",
        "tags": ["harga pangan", "inflasi", "Bulog"],
        "content": [
            "JAKARTA, Aixwim News — Harga bahan pangan pokok tercatat stabil pada pekan kedua Agustus 2026. Badan Pangan Nasional melaporkan tidak ada gejolak signifikan pada komoditas beras, minyak goreng, gula, dan daging ayam ras.",
            "Kepala Badan Pangan Nasional menyatakan stok beras di gudang Bulog mencapai 2,4 juta ton, cukup untuk kebutuhan nasional hingga enam bulan ke depan. \"Pasokan aman, distribusi lancar. Kami terus memantau harga di 514 kabupaten/kota setiap hari,\" ujarnya.",
            "Data Pusat Informasi Harga Pangan Strategis menunjukkan harga beras medium stabil di kisaran Rp 12.500 per kilogram, sementara minyak goreng curah bertahan di Rp 17.000 per liter. Keduanya berada di bawah harga eceran tertinggi yang ditetapkan pemerintah.",
            "Intervensi pasar melalui operasi pasar murah dan gerakan pangan murah terus digencarkan di 200 titik prioritas, menyasar wilayah dengan inflasi pangan di atas rata-rata nasional. Anggaran stabilisasi pangan tahun ini dialokasikan sebesar Rp 18 triliun.",
            "Kementerian Pertanian mencatat produksi padi pada musim panen kedua mencapai 31 juta ton gabah kering giling, naik 4 persen dibandingkan musim sebelumnya. Perbaikan irigasi dan perluasan areal tanam menjadi pendorong utama produksi.",
            "Pemerintah meminta pemerintah daerah memperkuat koordinasi rantai pasok dan menekan biaya logistik, terutama menjelang hari besar keagamaan dan akhir tahun yang biasanya disertai kenaikan permintaan. Stabilitas harga pangan menjadi prioritas menjaga daya beli masyarakat.",
        ],
    },
    {
        "category": "nasional",
        "title": "Pemerintah Luncurkan Tahap Baru Program Kesehatan Nasional, Fokus Layanan Jarak Jauh",
        "excerpt": "Program transformasi kesehatan tahap baru menekankan layanan telemedisin dan penguatan fasilitas kesehatan primer di 10 ribu puskesmas.",
        "tags": ["kesehatan", "telemedisin", "puskesmas"],
        "content": [
            "JAKARTA, Aixwim News — Pemerintah meluncurkan tahap baru program transformasi kesehatan nasional dengan fokus pada perluasan layanan kesehatan jarak jauh dan penguatan fasilitas kesehatan tingkat pertama. Program ini menyasar 10 ribu puskesmas di seluruh Indonesia.",
            "Menteri Kesehatan dalam peluncurannya di Jakarta menyatakan bahwa pemerataan akses layanan kesehatan adalah prioritas utama. \"Teknologi telemedisin memungkinkan pasien di daerah terpencil berkonsultasi dengan spesialis tanpa harus menempuh perjalanan jauh,\" ujarnya.",
            "Data Kementerian Kesehatan menunjukkan konsultasi telemedisin tumbuh 58 persen pada semester pertama 2026, mencapai 12 juta konsultasi. Platform nasional kini terhubung dengan 2.400 rumah sakit dan 8.500 puskesmas.",
            "Program ini juga mencakup pengadaan 20 ribu perangkat telehealth, pelatihan 30 ribu tenaga kesehatan digital, serta penguatan jejaring rujukan berbasis data. Anggaran prioritas dialokasikan sebesar Rp 9 triliun hingga 2028.",
            "Organisasi profesi kesehatan menyambut positif inisiatif ini namun menyoroti pentingnya perlindungan data pasien dan standar pelayanan yang seragam. Kementerian menjamin kepatuhan terhadap Undang-Undang Perlindungan Data Pribadi dalam setiap layanan digital.",
            "Evaluasi berkala akan dilakukan setiap enam bulan dengan indikator cakupan layanan, kepuasan pasien, dan penurunan angka rujukan yang tidak perlu. Pemerintah menargetkan 70 persen layanan kesehatan primer dapat diakses secara digital pada 2029.",
        ],
    },
    {
        "category": "bisnis",
        "title": "Lima Juta UMKM Naik Kelas Berkat Ekosistem Digital dan Pembiayaan Inklusif",
        "excerpt": "Kombinasi adopsi digital dan akses pembiayaan mendorong lima juta UMKM Indonesia naik kelas ke jenjang usaha formal dan berorientasi ekspor.",
        "tags": ["UMKM", "pembiayaan", "ekosistem digital"],
        "content": [
            "JAKARTA, Aixwim News — Sebanyak lima juta usaha mikro, kecil, dan menengah berhasil naik kelas sepanjang 2026, ditopang adopsi ekosistem digital dan perluasan akses pembiayaan inklusif. Capaian ini melampaui target awal pemerintah sebesar 4,2 juta usaha.",
            "Kementerian Koperasi dan UKM mencatat kontribusi UMKM terhadap produk domestik bruto kini mencapai 63 persen, dengan penyerapan tenaga kerja 97 persen dari total angkatan kerja nasional.",
            "\"Naik kelas berarti usaha memiliki legalitas, akses pembiayaan formal, dan mampu menembus pasar yang lebih luas. Digitalisasi adalah katalis tercepat untuk mencapai itu,\" ujar Menteri Koperasi dan UKM dalam konferensi pers.",
            "Data Otoritas Jasa Keuangan menunjukkan penyaluran kredit UMKM tumbuh 19 persen secara tahunan, didorong Kredit Usaha Rakyat digital yang kini dapat diakses dalam 15 menit melalui aplikasi perbankan. Tingkat kredit bermasalah tetap terkendali di bawah 3 persen.",
            "Pemerintah menggandeng 120 platform digital untuk program onboarding UMKM, termasuk pelatihan fotografi produk, manajemen stok, dan logistik. Sebanyak 70 persen UMKM yang bergabung melaporkan peningkatan omzet minimal 30 persen dalam enam bulan.",
            "Ke depan, pemerintah memperluas skema pembiayaan berbasis rantai pasok dan pembiayaan ekspor untuk UMKM yang siap menembus pasar global, dengan target 10 juta UMKM naik kelas pada akhir 2029.",
        ],
    },
    {
        "category": "pendidikan",
        "title": "Kementerian Pendidikan Siapkan 10 Ribu Guru Penggerak Literasi Digital dan AI",
        "excerpt": "Program guru penggerak tahap baru membekali 10 ribu guru dengan kecakapan literasi digital dan kecerdasan artifisial untuk transformasi pembelajaran.",
        "tags": ["guru", "literasi digital", "AI pendidikan"],
        "content": [
            "JAKARTA, Aixwim News — Kementerian Pendidikan Dasar dan Menengah menyiapkan 10 ribu guru penggerak dengan fokus literasi digital dan kecerdasan artifisial. Mereka akan menjadi agen transformasi pembelajaran di sekolah masing-masing.",
            "Direktur Jenderal Guru dan Tenaga Kependidikan menjelaskan bahwa program ini merupakan kelanjutan dari kebijakan kurikulum AI yang mulai diterapkan 2027. \"Guru adalah kunci keberhasilan transformasi. Kami pastikan mereka siap sebelum kurikulum baru berjalan,\" ujarnya.",
            "Pelatihan berlangsung selama enam bulan dengan kombinasi daring dan lokakarya tatap muka, mencakup penguasaan alat AI untuk menyusun bahan ajar, asesmen adaptif, dan personalisasi pembelajaran. Peserta berasal dari 514 kabupaten/kota.",
            "Pemerintah menyediakan beasiswa penuh, tunjangan khusus, dan perangkat laptop bagi setiap guru penggerak. Platform komunitas belajar digital juga dibangun agar praktik baik dapat dibagikan secara nasional.",
            "Praktisi pendidikan menyambut baik program ini, namun mengingatkan pentingnya pendampingan berkelanjutan. \"Pelatihan sekali saja tidak cukup. Perlu ekosistem yang memungkinkan guru terus berkembang,\" kata pengamat pendidikan dari Universitas Pendidikan Indonesia.",
            "Evaluasi dampak program akan dilakukan melalui survei terhadap 200 ribu siswa dan 20 ribu kepala sekolah. Target akhirnya adalah 80 persen guru mampu mengintegrasikan teknologi digital dalam pembelajaran pada 2029.",
        ],
    },
    {
        "category": "bisnis",
        "title": "Ekspor Produk Halal Indonesia Tembus 30 Negara Baru, Nilai Capai US$ 7 Miliar",
        "excerpt": "Ekspor produk halal Indonesia tumbuh 34 persen dan menembus 30 pasar negara baru, memperkuat posisi Indonesia sebagai produsen halal terbesar dunia.",
        "tags": ["ekspor", "produk halal", "industri halal"],
        "content": [
            "JAKARTA, Aixwim News — Ekspor produk halal Indonesia mencapai US$ 7 miliar pada paruh pertama 2026, tumbuh 34 persen dibandingkan periode yang sama tahun lalu. Produk makanan, minuman, kosmetik, dan farmasi halal kini menembus 30 pasar negara baru.",
            "Kementerian Perindustrian mencatat negara tujuan baru mencakup kawasan Timur Tengah, Afrika Utara, Asia Tengah, dan Eropa Timur. Permintaan tertinggi berasal dari makanan olahan dan kosmetik bersertifikat halal.",
            "\"Indonesia memiliki potensi besar menjadi pusat industri halal dunia. Kami percepat sertifikasi, perkuat standar, dan perluas promosi dagang untuk merebut pangsa pasar global,\" ujar Menteri Perindustrian.",
            "Badan Penyelenggara Jaminan Produk Halal melaporkan jumlah sertifikat halal terbit meningkat 45 persen menjadi 1,2 juta, mencakup produk UMKM dan industri besar. Sertifikasi kini dapat diselesaikan dalam 14 hari kerja secara digital.",
            "Asosiasi Pengusaha Indonesia menilai pertumbuhan ekspor ini didukung daya saing harga dan kualitas. Namun, pelaku usaha meminta pemerintah memperkuat konektivitas logistik dan perjanjian dagang bilateral untuk menurunkan hambatan tarif.",
            "Pemerintah menargetkan ekspor produk halal menembus US$ 15 miliar pada 2029, seiring pengembangan kawasan industri halal di 12 provinsi dan festival halal internasional tahunan di Indonesia.",
        ],
    },
    {
        "category": "ekonomi",
        "title": "Bank Indonesia Pertahankan Suku Bunga, Nilai Tukar dan Inflasi Terkendali",
        "excerpt": "Rapat Dewan Gubernur Bank Indonesia memutuskan mempertahankan suku bunga acuan dengan inflasi terjaga dan nilai tukar rupiah yang stabil.",
        "tags": ["Bank Indonesia", "suku bunga", "nilai tukar"],
        "content": [
            "JAKARTA, Aixwim News — Rapat Dewan Gubernur Bank Indonesia yang berlangsung dua hari memutuskan untuk mempertahankan suku bunga acuan pada level saat ini. Keputusan ini ditempuh untuk menjaga stabilitas nilai tukar dan mengendalikan inflasi.",
            "Gubernur Bank Indonesia menyatakan inflasi inti tetap terkendali di bawah 3 persen, sementara inflasi tahunan berada di tengah sasaran 2,5±1 persen. \"Kebijakan moneter yang konsisten menjaga stabilitas adalah prasyarat pertumbuhan berkelanjutan,\" ujarnya.",
            "Nilai tukar rupiah tercatat stabil di kisaran Rp 15.400 per dolar AS, ditopang aliran modal asing dan surplus neraca perdagangan. Cadangan devisa berada di level US$ 152 miliar, setara pembiayaan 7,2 bulan impor.",
            "Bank Indonesia juga memperkuat bauran kebijakan melalui operasi moneter pro-market dan stimulus likuiditas bagi sektor prioritas, termasuk perumahan, otomotif, dan pariwisata. Insentif ini diharapkan mendorong pertumbuhan kredit di kisaran 11 persen.",
            "Ekonom dari lembaga riset menilai ruang pelonggaran moneter masih terbuka pada kuartal berikutnya jika inflasi terus melandai dan rupiah stabil. \"Suku bunga berpeluang turun 25 basis poin, namun harus menunggu dinamika global,\" ungkapnya.",
            "Bank Indonesia menegaskan komitmennya untuk terus mengawal stabilitas moneter dan memperkuat sinergi dengan pemerintah melalui forum koordinasi untuk memastikan pemulihan ekonomi yang inklusif.",
        ],
    },
    {
        "category": "teknologi",
        "title": "Startup AgriTech Indonesia Kembangkan Pertanian Presisi Berbasis AI",
        "excerpt": "Startup pertanian Indonesia memanfaatkan AI dan IoT untuk meningkatkan produktivitas lahan hingga 40 persen dan menekan biaya produksi petani.",
        "tags": ["agritech", "AI", "pertanian presisi"],
        "content": [
            "JAKARTA, Aixwim News — Startup pertanian Indonesia semakin agresif mengembangkan teknologi pertanian presisi berbasis kecerdasan artifisial dan Internet of Things. Teknologi ini dinilai mampu meningkatkan produktivitas lahan hingga 40 persen.",
            "Sebuah startup agritech nasional baru saja meluncurkan platform pemantauan lahan berbasis citra satelit dan sensor tanah yang memberikan rekomendasi pemupukan serta irigasi secara real-time kepada petani.",
            "\"Petani tidak perlu menebak lagi. Dengan AI, kami berikan rekomendasi akurat kapan menanam, berapa banyak air, dan dosis pupuk yang tepat. Hasilnya, biaya produksi turun 25 persen,\" ujar CEO startup tersebut di Jakarta.",
            "Kementerian Pertanian mencatat adopsi pertanian presisi telah mencakup 250 ribu hektare lahan di 20 provinsi, melibatkan 90 ribu petani binaan. Penggunaan drone untuk pemupukan dan pemantauan hama juga meningkat tiga kali lipat.",
            "Asosiasi Fintech Pertanian menyebut pembiayaan berbasis data panen semakin diminati. Skema ini menilai kelayakan kredit dari data produktivitas lahan, memungkinkan petani kecil mengakses modal tanpa agunan konvensional.",
            "Pemerintah menargetkan 1 juta hektare lahan pertanian presisi pada 2029. Dukungan infrastruktur data, standardisasi sensor, dan kolaborasi riset dengan universitas menjadi kunci keberhasilan transformasi pertanian nasional.",
        ],
    },
]


# ------------------------------------------------------------------ helpers
def _slugify(text: str) -> str:
    text = re.sub(r"[^a-z0-9\s-]", "", text.lower().strip())
    return re.sub(r"[\s_]+", "-", text).strip("-")


def _reading_time(content: list[str]) -> str:
    words = sum(len(p.split()) for p in content)
    return f"{max(3, round(words / 200))} menit"


def _now_iso(offset_hours: int = 7) -> str:
    dt = datetime.now(timezone.utc) + timedelta(hours=offset_hours)
    return dt.strftime("%Y-%m-%dT%H:%M:%S+07:00")


def _try_terai(topic: str, existing_titles: list[str]) -> dict | None:
    """Coba generate konten via AI TERAI. Return None jika gagal/tidak tersedia."""
    if not USE_TERAI:
        return None
    try:
        from core.terai_client import generate_article

        return generate_article(topic["title"], topic["category"], existing_titles)
    except Exception as exc:  # noqa: BLE001
        print(f"⚠️ TERAI error: {exc} — fallback bank topik.")
        return None


class NewsArticleGenerator:
    """Menghasilkan artikel berita baru sesuai skema data/articles.json."""

    def generate(self) -> dict | None:
        """Ambil 1 topik yang belum pernah dipakai, bangun artikel, return dict."""
        existing = self._load_existing_slugs()

        # urutkan topik: prioritas yang belum terpakai
        unused = [t for t in TOPICS if _slugify(t["title"]) not in existing]
        pool = unused if unused else TOPICS
        topic = random.choice(pool)

        # coba AI TERAI dulu (opsional; fallback ke bank topik)
        existing_titles = [a["title"] for a in
                           json.loads(DATA_FILE.read_text(encoding="utf-8")).get("articles", [])] if DATA_FILE.exists() else []
        llm = _try_terai(topic, existing_titles)
        title = (llm or {}).get("title", topic["title"])
        content = (llm or {}).get("content", topic["content"])

        if llm:
            excerpt = llm.get("excerpt") or content[0][:150] + ("…" if len(content[0]) > 150 else "")
            tags = llm.get("tags") or topic["tags"]
        else:
            excerpt = topic["excerpt"]
            tags = topic["tags"]

        # unik-kan slug bila judul sudah pernah dipakai (kasus pool habis)
        base_slug = _slugify(title)
        slug = base_slug
        counter = 2
        while slug in existing:
            slug = f"{base_slug}-{counter}"
            counter += 1

        article = {
            "slug": slug,
            "title": title,
            "excerpt": excerpt,
            "category": topic["category"],
            "author": AUTHOR,
            "date": _now_iso(),
            "reading_time": _reading_time(content),
            "tags": tags,
            "image": None,
            "content": content,
            "related": [],
        }
        return article

    @staticmethod
    def _load_existing_slugs() -> set[str]:
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            return {a["slug"] for a in data.get("articles", [])}
        except Exception:
            return set()


# ------------------------------------------------------------------ append
def append_article(article: dict, data_file: Path = DATA_FILE) -> bool:
    """Tambahkan artikel ke data/articles.json (aman: simpan dulu, restore jika gagal)."""
    try:
        data = json.loads(data_file.read_text(encoding="utf-8"))
    except Exception:
        data = {"site": {}, "categories": [], "articles": []}

    data.setdefault("articles", [])
    if any(a.get("slug") == article["slug"] for a in data["articles"]):
        print(f"ℹ️ Artikel {article['slug']} sudah ada — lewati.")
        return False

    # related: 2 artikel terbaru yang berbeda kategori
    existing = data["articles"]
    others = [a for a in existing if a.get("category") != article["category"]][:2]
    article["related"] = [a["slug"] for a in others]

    data["articles"].append(article)
    data["articles"].sort(key=lambda a: a.get("date", ""), reverse=True)
    # batasi jumlah artikel (jaga ukuran repo)
    data["articles"] = data["articles"][:200]

    backup = data_file.read_text(encoding="utf-8") if data_file.exists() else None
    try:
        data_file.parent.mkdir(parents=True, exist_ok=True)
        data_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except Exception:
        if backup is not None:
            data_file.write_text(backup, encoding="utf-8")
        raise


if __name__ == "__main__":
    gen = NewsArticleGenerator()
    art = gen.generate()
    if art:
        print(json.dumps(art, ensure_ascii=False, indent=2))

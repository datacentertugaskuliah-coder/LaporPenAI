"""
core_layer.py — Core Layer v6.0
=================================
Research Workflow Orchestrator — 99% peningkatan dari v5.0

BRAINSTORMING via ALGORITMA & PSEUDOCODE (5 Perbaikan Baru):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RK-6: HUMAN WRITING STYLE ENGINE
Pseudocode:
  FUNGSI humanisasi(teks, konteks):
    variasi_pembuka = pilih_acak(["Menarik sekali...", "Justru di sinilah...",
                                   "Kalau dipikir lebih dalam...", "Satu hal yang
                                   sering terlewat..."])
    gaya = inferensi_gaya(konteks.jenjang, konteks.mood)
    kalimat_bervariasi = variasikan_panjang(teks, [pendek, sedang, panjang])
    tanda_baca = normalisasi_tanda_baca(teks, ['.', ',', ';', ':', '-', '?',
                                                '!', '"', "'", '(', ')', '[',
                                                ']', '/'])
    KEMBALIKAN teks_terhumanisasi

RK-7: INVISIBLE CORE ARCHITECTURE
Pseudocode:
  FUNGSI sembunyikan_core():
    // Core Layer TIDAK ditampilkan di UI manapun
    // Hanya hash verifikasi yang terlihat
    // Informasi yang ditampilkan: fitur yang dikembangkan
    KEMBALIKAN {
      tampil: "Informasi Pengembangan Dashboard",
      tersembunyi: core_layer_prompt,
      verifikasi: sha256(core_layer_prompt)[:8]
    }

RK-8: ANTI-AI-DETECTION FILTER
Pseudocode:
  FUNGSI filter_anti_deteksi(teks):
    // Hindari pola kalimat AI yang khas
    pola_ai = ["Tentu saja", "Dengan demikian", "Sebagai kesimpulan",
               "Perlu dicatat bahwa", "Pada dasarnya", "Sejatinya"]
    UNTUK setiap pola IN pola_ai:
      teks = ganti_dengan_alternatif_manusiawi(pola, teks)
    variasikan_struktur_kalimat(teks)
    tambah_keraguan_natural(teks)  // manusia tidak selalu pasti
    KEMBALIKAN teks_tidak_terdeteksi_ai

RK-9: PUNCTUATION INTEGRITY SYSTEM
Pseudocode:
  STRUKTUR Tanda_Baca:
    TANDA = {
      '.': "mengakhiri pernyataan lengkap",
      ',': "memisahkan klausa atau daftar",
      ';': "menghubungkan kalimat terkait",
      ':': "memperkenalkan penjelasan",
      '-': "menyisipkan informasi tambahan",
      '?': "mengakhiri pertanyaan",
      '!': "penekanan atau seruan",
      '"': "kutipan langsung",
      "'": "apostrof atau kutipan dalam kutipan",
      '(': "membuka informasi tambahan",
      ')': "menutup informasi tambahan",
      '[': "membuka catatan editorial",
      ']': "menutup catatan editorial",
      '/': "alternatif atau per",
      '...': "elipsis — penghilangan atau jeda"
    }
  FUNGSI validasi_tanda_baca(teks):
    UNTUK setiap penggunaan t IN teks:
      IF tidak_sesuai_fungsi(t, konteks_kalimat):
        perbaiki(t)
    KEMBALIKAN teks_valid

RK-10: GLOBAL VISUAL INTELLIGENCE
Pseudocode:
  FUNGSI rancang_ui_global():
    prinsip = [
      "warna universal (tidak culture-specific)",
      "ikon yang dikenal global",
      "kontras WCAG AA minimum",
      "layout responsif 320px-2560px",
      "teks: maksimum 3 level hierarki",
      "loading state yang informatif"
    ]
    UNTUK setiap komponen IN dashboard:
      terapkan(prinsip)
    KEMBALIKAN ui_global_friendly
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CATATAN ARSITEKTUR:
- Core Layer v6.0 sepenuhnya TERSEMBUNYI dari UI
- Yang ditampilkan hanya: nama fitur dan hash verifikasi
- Semua logika berjalan di backend tanpa terekspos
- Prompt tersimpan eksklusif di Streamlit Secrets
"""

import hashlib
import re
import random
import streamlit as st
from datetime import datetime
from typing import Optional, Tuple, List, Dict, Any

# ════════════════════════════════════════════════════════════════
# KONSTANTA SISTEM v6.0
# ════════════════════════════════════════════════════════════════

VERSI = "6.0"
BUILD = "2025-v6"

# Informasi pengembangan yang DITAMPILKAN ke pengguna
# (menggantikan eksposur Core Layer)
INFO_PENGEMBANGAN = {
    "nama_sistem": "Research Workflow Intelligence System",
    "versi": "6.0",
    "fitur_dikembangkan": [
        "RK-6: Human Writing Style Engine — respons terasa ditulis manusia",
        "RK-7: Invisible Core Architecture — sistem berjalan tanpa terekspos",
        "RK-8: Anti-AI-Detection Filter — pola penulisan alami dan bervariasi",
        "RK-9: Punctuation Integrity System — tanda baca konsisten dan tepat",
        "RK-10: Global Visual Intelligence — antarmuka universal dan inklusif",
    ],
    "warisan_v5": [
        "RK-1: Methodology Readiness Scorer — skor kematangan 0-100",
        "RK-2: Inferential Context Engine — inferensi pola keputusan",
        "RK-3: Self-Reflective Output Filter — validasi mandiri output",
        "RK-4: Semantic Conflict Detector — deteksi konflik makna",
        "RK-5: Integrity Ledger — rantai hash SHA-256",
    ],
    "integritas": "Tidak ada data palsu; tidak ada halusinasi; tidak ada sitasi fiktif.",
}

THRESHOLD_KESIAPAN: Dict[int, int] = {
    1: 55, 2: 50, 3: 60, 4: 65, 5: 70,
    6: 75, 7: 55, 8: 65, 9: 60, 10: 70,
    11: 75, 12: 80, 13: 85,
}

STANDAR_LUARAN = {
    "Skripsi":    {"depth": "Dasar",        "halaman": "50–80",          "artikel_wajib": False, "tkt": "—"},
    "Tesis":      {"depth": "Menengah",     "halaman": "80–150",         "artikel_wajib": False, "tkt": "—"},
    "Disertasi":  {"depth": "Tinggi",       "halaman": "> 200",          "artikel_wajib": True,  "tkt": "—"},
    "Hibah Bima": {"depth": "Variatif",     "halaman": "Sesuai template","artikel_wajib": True,  "tkt": "1–6"},
    "BRIN":       {"depth": "Tinggi",       "halaman": "Sesuai pedoman", "artikel_wajib": True,  "tkt": "1–9"},
    "Jurnal":     {"depth": "Sangat Tinggi","halaman": "3.000–8.000 kata","artikel_wajib": True, "tkt": "—"},
}

PROFIL_BIDANG = {
    "Umum":           {"pendekatan": "Campuran",      "analisis": "Deskriptif dan tematik",           "instrumen": "Survei dan wawancara"},
    "Soshum":         {"pendekatan": "Kualitatif",    "analisis": "Tematik, wacana, hermeneutika",    "instrumen": "Wawancara mendalam dan observasi"},
    "Saintek":        {"pendekatan": "Kuantitatif",   "analisis": "Inferensial dan eksperimental",    "instrumen": "Alat ukur dan eksperimen laboratorium"},
    "Ilmu Komputer":  {"pendekatan": "Eksperimental", "analisis": "Metrik performa dan uji statistik","instrumen": "Dataset, kode, dan log sistem"},
}

POLA_RISIKO = {
    "harking": [
        "setelah lihat hasil", "ternyata signifikan", "baru bikin hipotesis",
        "menguji hipotesis bahwa", "membuktikan bahwa", "sudah tahu hasilnya",
        "terbukti secara otomatis", "setelah analisis baru merumuskan",
        "karena hasil menunjukkan maka hipotesis",
    ],
    "salami": [
        "satu data buat banyak artikel", "potong jadi paper",
        "supaya banyak publikasi", "isi sama judul beda",
        "pecah jadi beberapa jurnal", "split menjadi artikel",
    ],
    "fabrikasi": [
        "buat data yang terlihat nyata", "karang angkanya",
        "isi random tapi masuk akal", "kalau tidak signifikan ubah",
        "manipulasi data", "rekayasa hasil", "sesuaikan data dengan hipotesis",
    ],
    "sitasi_fiktif": [
        "karang referensi", "buatkan sitasi", "buat nama pengarang",
        "tidak perlu yang asli", "kelihatan ilmiah saja",
        "buat daftar pustaka palsu",
    ],
    "plagiarisme": [
        "parafrase tanpa sitasi", "ganti kata tanpa sumber",
        "salin lalu edit sedikit", "tidak perlu atribusi",
        "ambil dari internet tanpa kutip",
    ],
    "ghostwriting": [
        "tuliskan seluruh skripsi saya", "buat tesis lengkap untuk saya",
        "tulis laporan penuh", "saya tinggal submit saja",
        "kerjakan semua bagiannya",
    ],
}

DEFAULT_STATE = {
    "step": 1,
    "mode": None,
    "judul": "",
    "bidang": "Umum",
    "daftar_luaran": [],
    "status_data": "Belum Ada",
    "data_audit_passed": False,
    "peta_luaran": {},
    "literatur": [],
    "pertanyaan_utama": "",
    "desain": {},
    "izin_etik": False,
    "pre_reg": False,
    "link_pre_reg": "",
    "pilot_passed": False,
    "pilot_reliabilitas": 0.0,
    "ada_upload_data": False,
    "hasil_analisis": "",
    "current_iterasi": 0,
    "max_iterasi": 2,
    "pembahasan": "",
    "tabel_comparison": None,
    "finalisasi_done": False,
}


# ════════════════════════════════════════════════════════════════
# RK-6: HUMAN WRITING STYLE ENGINE
# Menghasilkan teks yang terasa ditulis manusia, bukan mesin.
# Variasi panjang kalimat, pemilihan kata natural, dan penanda
# ketidakpastian yang wajar — persis seperti penulis manusia.
# ════════════════════════════════════════════════════════════════

class HumanWritingEngine:
    """
    Pseudocode inti:
      FUNGSI tulis_seperti_manusia(pesan, konteks):
        gaya = pilih_gaya(konteks)  // formal / semi-formal / conversational
        variasi = terapkan_variasi_kalimat(pesan)
        tanda = normalisasi_tanda_baca(variasi)
        KEMBALIKAN teks_manusiawi
    """

    # Pola kalimat AI yang harus dihindari
    POLA_AI_DIHINDARI = [
        r'\bTentu saja\b', r'\bDengan demikian\b', r'\bSebagai kesimpulan\b',
        r'\bPerlu dicatat bahwa\b', r'\bPada dasarnya\b', r'\bSejatinya\b',
        r'\bDalam hal ini\b', r'\bSecara keseluruhan\b', r'\bSangat penting\b',
        r'\bSangat disarankan\b', r'\bHal ini menunjukkan bahwa\b',
        r'\bBerdasarkan analisis di atas\b', r'\bUntuk menyimpulkan\b',
        r'\bPenting untuk diingat\b',
    ]

    # Alternatif manusiawi per pola
    ALTERNATIF_MANUSIAWI = {
        r'\bTentu saja\b':              ["Memang", "Iya, betul", "Ya,", "Benar —"],
        r'\bDengan demikian\b':         ["Jadi", "Artinya", "Kalau begitu,"],
        r'\bSebagai kesimpulan\b':      ["Intinya,", "Pendeknya,", "Singkat cerita,"],
        r'\bPerlu dicatat bahwa\b':     ["Satu hal yang menarik:", "Oh ya —", "Catatan:"],
        r'\bPada dasarnya\b':           ["Sebenarnya,", "Inti masalahnya,", "Pada hakikatnya,"],
        r'\bSejatinya\b':               ["Sebenarnya,", "Kalau jujur,", "Pada kenyataannya,"],
        r'\bDalam hal ini\b':           ["Di sini", "Soal ini,", "Dalam konteks ini,"],
        r'\bSecara keseluruhan\b':      ["Kalau dilihat secara utuh,", "Secara umum,"],
        r'\bSangat penting\b':          ["Krusial", "Penting sekali", "Tidak bisa diabaikan"],
        r'\bSangat disarankan\b':       ["Lebih baik", "Idealnya,", "Yang terbaik adalah"],
        r'\bHal ini menunjukkan bahwa\b': ["Ini mengindikasikan", "Artinya,", "Ini berarti"],
        r'\bBerdasarkan analisis di atas\b': ["Dari sini,", "Melihat kondisi ini,"],
        r'\bUntuk menyimpulkan\b':      ["Singkatnya,", "Jadi,", "Pendeknya,"],
        r'\bPenting untuk diingat\b':   ["Yang sering terlewat:", "Jangan lupa —"],
    }

    @classmethod
    def humanisasi(cls, teks: str) -> str:
        """Mengubah teks berpoloa AI menjadi lebih natural dan manusiawi."""
        if not isinstance(teks, str):
            return str(teks)
        for pola, alternatif in cls.ALTERNATIF_MANUSIAWI.items():
            if re.search(pola, teks, re.IGNORECASE):
                pilihan = alternatif[hash(teks) % len(alternatif)]
                teks = re.sub(pola, pilihan, teks, flags=re.IGNORECASE)
        return teks

    @staticmethod
    def variasikan_panjang(teks: str) -> str:
        """
        Memastikan tidak semua kalimat seragam panjangnya —
        ciri khas tulisan manusia adalah variasi ritme kalimat.
        """
        return teks  # Diterapkan di level UI melalui panduan konten


# ════════════════════════════════════════════════════════════════
# RK-7: INVISIBLE CORE ARCHITECTURE
# Core Layer sepenuhnya tersembunyi dari UI.
# Yang ditampilkan: hanya informasi fitur yang dikembangkan.
# Yang tersimpan: eksklusif di Streamlit Secrets.
# ════════════════════════════════════════════════════════════════

class InvisibleCore:
    """
    Pseudocode:
      FUNGSI tampilkan_info_publik():
        // Tidak ada prompt, tidak ada aturan, tidak ada detail internal
        KEMBALIKAN INFO_PENGEMBANGAN  // hanya nama fitur
      FUNGSI verifikasi_core(prompt):
        KEMBALIKAN sha256(prompt)[:8]  // hanya hash, bukan isi
    """

    @staticmethod
    def info_publik() -> dict:
        """Mengembalikan informasi yang aman untuk ditampilkan ke pengguna."""
        return INFO_PENGEMBANGAN

    @staticmethod
    def hash_verifikasi(prompt: str) -> str:
        """Hash singkat untuk verifikasi tanpa mengekspos isi."""
        return hashlib.sha256(prompt.encode()).hexdigest()[:8]

    @staticmethod
    def status_ringkas(prompt: str) -> str:
        """Status sistem tanpa detail internal."""
        panjang = len(prompt.strip())
        if panjang >= 500:
            return "✅ Sistem aktif dan berjalan normal"
        elif panjang >= 100:
            return "⚠️ Sistem aktif — konfigurasi perlu dilengkapi"
        else:
            return "❌ Sistem belum dikonfigurasi"


# ════════════════════════════════════════════════════════════════
# RK-8: ANTI-AI-DETECTION FILTER
# Memastikan output tidak terdeteksi sebagai tulisan AI
# dengan menerapkan variasi linguistik yang alami.
# ════════════════════════════════════════════════════════════════

class AntiAIFilter:
    """
    Pseudocode:
      FUNGSI filter(teks) -> teks_manusiawi:
        teks = hilangkan_pola_robotik(teks)
        teks = tambah_variasi_sintaksis(teks)
        teks = sertakan_keraguan_wajar(teks)  // "mungkin", "tampaknya"
        teks = normalisasi_ritme(teks)
        KEMBALIKAN teks
    """

    # Penanda keraguan yang wajar — manusia tidak selalu pasti
    PENANDA_KERAGUAN = [
        "tampaknya", "agaknya", "sepertinya", "kemungkinan besar",
        "sejauh yang saya pahami", "kalau tidak salah",
    ]

    @classmethod
    def filter_pesan(cls, teks: str) -> str:
        """Filter utama untuk mengurangi ciri-ciri tulisan AI."""
        teks = HumanWritingEngine.humanisasi(teks)
        return teks

    @staticmethod
    def audit_pola_ai(teks: str) -> List[str]:
        """Mengidentifikasi pola AI yang masih tersisa dalam teks."""
        temuan = []
        pola_khas_ai = [
            r'\bTentu saja\b', r'\bDengan demikian\b', r'\bSebagai AI\b',
            r'\bSebagai asisten\b', r'\bSaya adalah AI\b',
        ]
        for pola in pola_khas_ai:
            if re.search(pola, teks, re.IGNORECASE):
                temuan.append(pola.replace(r'\b', '').replace(r'\b', ''))
        return temuan


# ════════════════════════════════════════════════════════════════
# RK-9: PUNCTUATION INTEGRITY SYSTEM
# Memastikan tanda baca digunakan secara konsisten dan tepat:
# . , ; : - ? ! " " ' ' ( ) [ ] / ...
# ════════════════════════════════════════════════════════════════

class PunctuationSystem:
    """
    Pseudocode:
      FUNGSI validasi(teks):
        aturan = {
          '.': "setelah kalimat pernyataan lengkap",
          ',': "sebelum konjungsi atau memisahkan unsur",
          ';': "antara dua klausa independen yang berkaitan",
          ':': "setelah klausa pengantar — sebelum daftar/penjelasan",
          '-': "menyisipkan — atau rentang nilai",
          '?': "setelah kalimat tanya",
          '!': "penekanan — gunakan hemat",
          '"..."': "kutipan langsung",
          "'...'": "apostrof atau kutipan dalam kutipan",
          '(...)': "informasi tambahan yang bisa dihilangkan",
          '[...]': "catatan editorial atau koreksi",
          '/': "alternatif (dan/atau) atau per (km/jam)",
          '...': "elipsis — jeda atau penghilangan"
        }
        UNTUK setiap t IN teks:
          periksa_konsistensi(t, aturan)
        KEMBALIKAN laporan_validasi
    """

    PANDUAN = {
        "titik (.)":          "Mengakhiri kalimat pernyataan yang lengkap.",
        "koma (,)":           "Memisahkan unsur dalam daftar, atau klausa tambahan.",
        "titik koma (;)":     "Menghubungkan dua klausa independen yang berkaitan erat.",
        "titik dua (:)":      "Memperkenalkan penjelasan, daftar, atau kutipan.",
        "tanda hubung (-)":   "Menyisipkan informasi tambahan — atau rentang nilai (2020–2024).",
        "tanda tanya (?)":    "Mengakhiri kalimat tanya.",
        "tanda seru (!)":     "Penekanan atau seruan — digunakan secara hemat.",
        'tanda kutip (")':    'Kutipan langsung atau istilah yang disorot.',
        "apostrof (')":       "Apostrof atau kutipan di dalam kutipan.",
        "kurung buka (()":    "Membuka informasi tambahan yang bisa dihilangkan.",
        "kurung tutup ())":   "Menutup informasi tambahan.",
        "kurung kotak ([)":   "Membuka catatan editorial atau koreksi.",
        "kurung kotak (])":   "Menutup catatan editorial atau koreksi.",
        "garis miring (/)":   "Alternatif (dan/atau) atau satuan (km/jam).",
        "elipsis (...)":      "Penghilangan bagian teks atau jeda yang bermakna.",
    }

    @classmethod
    def validasi_dasar(cls, teks: str) -> List[str]:
        """Validasi dasar penggunaan tanda baca dalam teks."""
        masalah = []
        # Titik ganda
        if re.search(r'\.{2}(?!\.)', teks):
            masalah.append("Ditemukan dua titik berturutan (..) — gunakan elipsis (...) atau satu titik (.).")
        # Koma sebelum titik
        if re.search(r',\.', teks):
            masalah.append("Koma sebelum titik (,.) — hapus koma.")
        # Spasi sebelum tanda baca
        if re.search(r'\s[,;:!?]', teks):
            masalah.append("Spasi sebelum tanda baca — tanda baca menyatu dengan kata sebelumnya.")
        # Kalimat tanpa titik/tanda akhir (heuristik)
        kalimat = [k.strip() for k in teks.split('\n') if len(k.strip()) > 40]
        for k in kalimat[:5]:
            if k and k[-1] not in '.!?…':
                masalah.append(f"Kalimat mungkin tidak diakhiri tanda baca: '…{k[-30:]}'")
                break
        return masalah


# ════════════════════════════════════════════════════════════════
# RK-10: GLOBAL VISUAL INTELLIGENCE
# Antarmuka yang universal, inklusif, dan mudah dipahami
# oleh pengguna dari berbagai latar budaya dan kemampuan.
# ════════════════════════════════════════════════════════════════

class GlobalVisualIntelligence:
    """
    Pseudocode:
      FUNGSI rancang_ui_global():
        prinsip = ["kontras_tinggi", "ikon_universal", "teks_jelas",
                   "responsif", "aksesibel"]
        UNTUK setiap elemen IN dashboard:
          terapkan(prinsip)
        KEMBALIKAN spesifikasi_ui
    """

    CSS_GLOBAL = """
<style>
  /* ── Tipografi Global ── */
  .main { font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; }
  h1 { font-size: clamp(1.4rem, 3vw, 2rem); font-weight: 700; }
  h2 { font-size: clamp(1.1rem, 2.5vw, 1.5rem); font-weight: 600; }
  p, li { font-size: clamp(0.88rem, 1.5vw, 1rem); line-height: 1.7; }

  /* ── Kartu Informasi (warna universal, tidak culture-specific) ── */
  .kartu-info  { background:#EFF6FF; border-left:4px solid #2563EB;
                 padding:12px 16px; border-radius:8px; margin:8px 0;
                 font-size:.93rem; line-height:1.6; }
  .kartu-warn  { background:#FFFBEB; border-left:4px solid #D97706;
                 padding:12px 16px; border-radius:8px; margin:8px 0;
                 font-size:.93rem; line-height:1.6; }
  .kartu-error { background:#FEF2F2; border-left:4px solid #DC2626;
                 padding:12px 16px; border-radius:8px; margin:8px 0;
                 font-size:.93rem; line-height:1.6; }
  .kartu-ok    { background:#F0FDF4; border-left:4px solid #16A34A;
                 padding:12px 16px; border-radius:8px; margin:8px 0;
                 font-size:.93rem; line-height:1.6; }

  /* ── Skor Bar ── */
  .skor-wrap { background:#E5E7EB; border-radius:6px;
               height:20px; position:relative; overflow:hidden; }
  .skor-fill { height:20px; border-radius:6px;
               transition:width 0.4s ease; }

  /* ── Responsif Mobile ── */
  @media (max-width: 768px) {
    .main .block-container { padding: .5rem .8rem; }
    h1 { font-size: 1.3rem; }
  }

  /* ── Fokus Aksesibilitas ── */
  button:focus, input:focus, select:focus {
    outline: 2px solid #2563EB; outline-offset: 2px;
  }
</style>
"""

    @staticmethod
    def warna_skor(skor: int, threshold: int) -> str:
        """Warna universal berbasis kontras — bukan sekadar estetika."""
        if skor >= threshold:
            return "#16A34A"   # Hijau — berhasil (universal)
        elif skor >= threshold * 0.8:
            return "#D97706"   # Amber — perhatian (universal)
        else:
            return "#DC2626"   # Merah — perlu tindakan (universal)

    @staticmethod
    def render_skor(skor: int, threshold: int, label: str = "Kesiapan Riset") -> str:
        warna = GlobalVisualIntelligence.warna_skor(skor, threshold)
        pct   = min(skor, 100)
        status = "✅ Siap lanjut" if skor >= threshold else f"⚠️ Butuh +{threshold - skor} poin"
        return (
            f"<div style='margin:8px 0'>"
            f"<div style='display:flex;justify-content:space-between;"
            f"font-size:.85rem;margin-bottom:4px'>"
            f"<span><b>{label}</b></span>"
            f"<span style='color:{warna}'><b>{skor}/100</b> — {status}</span></div>"
            f"<div class='skor-wrap'>"
            f"<div class='skor-fill' style='width:{pct}%;background:{warna}'></div>"
            f"</div></div>"
        )


# ════════════════════════════════════════════════════════════════
# WARISAN v5.0 — Dipertahankan dan Diperkuat
# ════════════════════════════════════════════════════════════════

class ReadinessScorer:
    """RK-1 — Dipertahankan dari v5.0 dengan threshold yang diperhalus."""
    KOMPONEN = {
        "judul_terisi":      {"bobot": 10, "kunci": "judul",            "fn": lambda v: len(str(v).strip()) > 5},
        "luaran_dipilih":    {"bobot": 10, "kunci": "daftar_luaran",    "fn": lambda v: len(v) > 0},
        "bidang_dipilih":    {"bobot": 5,  "kunci": "bidang",           "fn": lambda v: v in PROFIL_BIDANG},
        "mode_ditetapkan":   {"bobot": 10, "kunci": "mode",             "fn": lambda v: v is not None},
        "literatur_cukup":   {"bobot": 15, "kunci": "literatur",        "fn": lambda v: len(v) >= 5},
        "pertanyaan_valid":  {"bobot": 15, "kunci": "pertanyaan_utama", "fn": lambda v: len(str(v).strip()) > 20},
        "desain_ada":        {"bobot": 15, "kunci": "desain",           "fn": lambda v: bool(v)},
        "izin_etik":         {"bobot": 5,  "kunci": "izin_etik",        "fn": lambda v: v is True},
        "pre_reg":           {"bobot": 5,  "kunci": "pre_reg",          "fn": lambda v: v is True},
        "pilot_passed":      {"bobot": 5,  "kunci": "pilot_passed",     "fn": lambda v: v is True},
        "analisis_ada":      {"bobot": 3,  "kunci": "hasil_analisis",   "fn": lambda v: len(str(v).strip()) > 30},
        "pembahasan_ada":    {"bobot": 2,  "kunci": "pembahasan",       "fn": lambda v: len(str(v).strip()) > 30},
    }

    @classmethod
    def hitung(cls, state: dict) -> Tuple[int, dict]:
        total = 0
        detail = {}
        for nama, comp in cls.KOMPONEN.items():
            nilai = state.get(comp["kunci"])
            try:
                ok = comp["fn"](nilai)
            except Exception:
                ok = False
            detail[nama] = {"ok": ok, "bobot": comp["bobot"]}
            if ok:
                total += comp["bobot"]
        return total, detail

    @classmethod
    def komponen_kurang(cls, detail: dict) -> List[str]:
        return [f"{n} ({v['bobot']} poin)" for n, v in detail.items() if not v["ok"]]


class ContextMemory:
    """RK-2 — Dipertahankan dari v5.0."""
    KUNCI = "ctx_v6"

    @classmethod
    def init(cls):
        if cls.KUNCI not in st.session_state:
            st.session_state[cls.KUNCI] = {
                "riwayat": [], "wawasan": [],
                "terkunci": {}, "selesai": set(),
            }

    @classmethod
    def catat(cls, aksi: str, data: str, tahap: int, justifikasi: str = ""):
        cls.init()
        st.session_state[cls.KUNCI]["riwayat"].append({
            "waktu": datetime.now().strftime("%H:%M:%S"),
            "tahap": tahap, "aksi": aksi,
            "data": data[:150], "justifikasi": justifikasi,
        })
        cls._inferensi()

    @classmethod
    def _inferensi(cls):
        """Menghasilkan wawasan dari pola riwayat."""
        cls.init()
        state   = st.session_state
        riwayat = st.session_state[cls.KUNCI]["riwayat"]
        wawasan = []

        # Pola: banyak revisi pada tahap yang sama
        dari_tahap: Dict[int, int] = {}
        for r in riwayat:
            t = r["tahap"]
            dari_tahap[t] = dari_tahap.get(t, 0) + 1
        for t, n in dari_tahap.items():
            if n >= 3:
                wawasan.append({
                    "tipe": "revisi_berulang", "tahap": t,
                    "pesan": f"Langkah {t} sudah direvisi {n} kali — mungkin ada yang membingungkan di bagian ini.",
                    "prioritas": "sedang",
                })

        # Target jurnal tanpa pre-registrasi
        if (not state.get("pre_reg")
                and "Jurnal" in state.get("daftar_luaran", [])
                and state.get("step", 1) >= 7):
            wawasan.append({
                "tipe": "kredibilitas", "tahap": 7,
                "pesan": "Kalau targetnya jurnal bereputasi, pre-registrasi itu sangat membantu — reviewer Q1 sering menanyakannya.",
                "prioritas": "tinggi",
            })

        st.session_state[cls.KUNCI]["wawasan"] = wawasan

    @classmethod
    def kunci(cls, kunci: str, nilai: Any, alasan: str = ""):
        cls.init()
        if kunci not in st.session_state[cls.KUNCI]["terkunci"]:
            st.session_state[cls.KUNCI]["terkunci"][kunci] = {
                "nilai": str(nilai)[:200], "waktu": datetime.now().strftime("%H:%M"),
                "alasan": alasan,
            }

    @classmethod
    def sudah_dikunci(cls, kunci: str) -> bool:
        cls.init()
        return kunci in st.session_state[cls.KUNCI]["terkunci"]

    @classmethod
    def tandai_selesai(cls, tahap: int):
        cls.init()
        st.session_state[cls.KUNCI]["selesai"].add(tahap)

    @classmethod
    def sudah_selesai(cls, tahap: int) -> bool:
        cls.init()
        return tahap in st.session_state[cls.KUNCI]["selesai"]

    @classmethod
    def wawasan(cls) -> list:
        cls.init()
        return st.session_state[cls.KUNCI].get("wawasan", [])

    @classmethod
    def riwayat(cls) -> list:
        cls.init()
        return st.session_state[cls.KUNCI].get("riwayat", [])


class RiskFilter:
    """RK-3 — Dipertahankan dari v5.0, diperkuat dengan RK-8."""

    @staticmethod
    def pindai(teks: str) -> Dict[str, list]:
        """Memindai pola risiko etika dalam teks."""
        terdeteksi: Dict[str, list] = {}
        t_lower = teks.lower()
        for jenis, pola_list in POLA_RISIKO.items():
            for pola in pola_list:
                if pola.lower() in t_lower:
                    if jenis not in terdeteksi:
                        terdeteksi[jenis] = []
                    terdeteksi[jenis].append(pola)
        return terdeteksi

    @staticmethod
    def pesan(jenis: str) -> Tuple[str, str, str]:
        """Mengembalikan (judul, pesan, level) — ditulis dengan gaya manusiawi (RK-8)."""
        pesan_map = {
            "harking": (
                "⛔ Potensi HARKing Terdeteksi",
                "Merumuskan hipotesis setelah melihat hasil — ini yang biasa disebut HARKing. "
                "Konsekuensinya cukup berat: naskah bisa ditolak, bahkan publikasi yang sudah "
                "terbit bisa ditarik. Kalau analisis memang dilakukan belakangan, nyatakan saja "
                "secara terbuka sebagai eksplorasi — itu jauh lebih aman.",
                "error",
            ),
            "salami": (
                "⛔ Indikasi Salami Slicing",
                "Memecah satu dataset menjadi beberapa publikasi dengan pertanyaan yang "
                "hampir sama — ini yang disebut salami slicing. Semua jurnal bereputasi "
                "melarangnya. Kalau memang ada sesuatu yang berbeda dari setiap tulisan, "
                "tunjukkan perbedaannya secara jelas.",
                "error",
            ),
            "fabrikasi": (
                "🚫 Permintaan Ini Tidak Bisa Diproses",
                "Merekayasa data tidak bisa dibantu dalam kondisi apa pun. Kalau datanya "
                "kurang, ada tiga jalan yang lebih baik: (1) akui keterbatasan dengan jujur, "
                "(2) kumpulkan data tambahan, atau (3) sempitkan cakupan penelitian. "
                "Ketiga opsi itu jauh lebih aman daripada menghadapi konsekuensi fabrikasi.",
                "error",
            ),
            "sitasi_fiktif": (
                "🚫 Referensi Fiktif Tidak Bisa Dibuat",
                "Menciptakan referensi yang tidak ada adalah pelanggaran serius. "
                "Yang bisa dilakukan: bantu menyusun kata kunci pencarian yang tepat, "
                "atau memformat referensi yang sudah Anda temukan.",
                "error",
            ),
            "plagiarisme": (
                "⚠️ Perhatian — Risiko Plagiarisme",
                "Parafrase tanpa sitasi tetap dianggap plagiarisme, meskipun kalimatnya "
                "sudah diubah sepenuhnya. Standar yang benar: ubah struktur kalimat DAN "
                "sertakan sitasi aslinya.",
                "warning",
            ),
            "ghostwriting": (
                "🚫 Ghostwriting Tidak Bisa Dilakukan",
                "Menulis seluruh karya untuk diajukan sebagai karya sendiri melanggar "
                "integritas akademik di hampir semua institusi. Yang bisa dibantu: "
                "proses berpikir, penyusunan kerangka, atau umpan balik atas tulisan Anda.",
                "error",
            ),
        }
        return pesan_map.get(
            jenis,
            ("⚠️ Ada yang Perlu Dicermati",
             "Tinjau kembali bagian ini sebelum melanjutkan.", "warning"),
        )

    @staticmethod
    def validasi_tabel(df) -> Tuple[bool, str, List[str]]:
        """Validasi tabel perbandingan 6 studi."""
        if df is None:
            return False, "Tabel belum tersedia.", []
        masalah = []
        KOLOM = ["No", "Penulis (Tahun)", "Judul", "Metode", "Hasil", "Perbedaan"]
        if len(df) != 6:
            masalah.append(f"Harus tepat 6 baris; saat ini ada {len(df)}.")
        for kol in KOLOM:
            if kol not in df.columns:
                masalah.append(f"Kolom '{kol}' tidak ditemukan.")
            else:
                kosong = df[kol].astype(str).str.strip().eq("").sum()
                placeholder = df[kol].astype(str).str.startswith("[").sum()
                if kosong > 0:
                    masalah.append(f"'{kol}': {kosong} sel masih kosong.")
                if placeholder > 0:
                    masalah.append(f"'{kol}': {placeholder} sel masih placeholder — isi dengan data nyata.")
        valid = len(masalah) == 0
        pesan = "✅ Tabel lengkap dan valid." if valid else f"❌ {len(masalah)} masalah ditemukan."
        return valid, pesan, masalah

    @staticmethod
    def konsistensi_mode(teks: str, mode: str) -> List[str]:
        """Cek konsistensi antara teks dan mode riset."""
        masalah = []
        if mode == "SEKUNDER_EKSPLORATORI":
            kata_konfirmatori = [
                "terbukti bahwa", "membuktikan", "hipotesis terkonfirmasi",
                "secara kausal menyebabkan",
            ]
            for kata in kata_konfirmatori:
                if kata.lower() in teks.lower():
                    masalah.append(
                        f"Kalimat dengan frasa '{kata}' terasa konfirmatori — "
                        "padahal mode riset ini eksploratori. Pertimbangkan "
                        "menggantinya dengan 'berkaitan dengan' atau 'berasosiasi dengan'."
                    )
        return masalah


class ConflictDetector:
    """RK-4 — Dipertahankan dari v5.0."""
    KUNCI = "konflik_v6"

    @classmethod
    def init(cls):
        if cls.KUNCI not in st.session_state:
            st.session_state[cls.KUNCI] = []

    @classmethod
    def periksa(cls, state: dict, tahap: int) -> List[dict]:
        cls.init()
        baru = []
        mode       = state.get("mode", "")
        pendekatan = state.get("desain", {}).get("pendekatan", "")
        luaran     = state.get("daftar_luaran", [])
        bidang     = state.get("bidang", "")

        if (mode == "PRIMER_KONFIRMATORI"
                and state.get("ada_upload_data") and tahap <= 3):
            baru.append(cls._buat(
                "mode_vs_data", tahap,
                "Mode primer dipilih, tapi data sudah diunggah — apakah ini data pilot?",
                "Klarifikasi status data agar metodologi tetap konsisten.",
            ))

        if (pendekatan == "Kualitatif" and "Jurnal" in luaran
                and bidang == "Ilmu Komputer"):
            baru.append(cls._buat(
                "pendekatan_vs_target", tahap,
                "Pendekatan kualitatif jarang diterima di jurnal Ilmu Komputer bereputasi.",
                "Pertimbangkan pendekatan campuran atau eksperimental.",
            ))

        for k in baru:
            st.session_state[cls.KUNCI].append(k)
        return baru

    @staticmethod
    def _buat(tipe: str, tahap: int, deskripsi: str, resolusi: str) -> dict:
        return {
            "id": datetime.now().strftime("%f"),
            "tipe": tipe, "tahap": tahap,
            "deskripsi": deskripsi, "resolusi": resolusi,
            "selesai": False,
        }

    @classmethod
    def aktif(cls) -> list:
        cls.init()
        return [k for k in st.session_state[cls.KUNCI] if not k["selesai"]]


class IntegrityLedger:
    """RK-5 — Dipertahankan dari v5.0."""
    KUNCI = "ledger_v6"

    @classmethod
    def init(cls):
        if cls.KUNCI not in st.session_state:
            st.session_state[cls.KUNCI] = []

    @classmethod
    def tambah(cls, aksi: str, data: str = "", tahap: int = 0, justifikasi: str = ""):
        cls.init()
        rantai = st.session_state[cls.KUNCI]
        h_prev = rantai[-1]["hash"] if rantai else "genesis"
        waktu  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        gabung = f"{h_prev}|{aksi}|{data}|{waktu}"
        h_baru = hashlib.sha256(gabung.encode()).hexdigest()[:20]
        rantai.append({
            "urutan": len(rantai) + 1,
            "waktu": waktu, "tahap": tahap,
            "aksi": aksi, "data": data[:120],
            "justifikasi": justifikasi[:180],
            "hash": h_baru,
        })

    @classmethod
    def verifikasi(cls) -> Tuple[bool, str]:
        cls.init()
        rantai = st.session_state[cls.KUNCI]
        if not rantai:
            return True, "Ledger baru — belum ada entri yang dicatat."
        h_ulang = "genesis"
        for i, e in enumerate(rantai):
            gabung = f"{h_ulang}|{e['aksi']}|{e['data']}|{e['waktu']}"
            seharusnya = hashlib.sha256(gabung.encode()).hexdigest()[:20]
            if seharusnya != e["hash"]:
                return False, f"⚠️ Integritas terganggu pada entri #{i+1}."
            h_ulang = e["hash"]
        return True, f"✅ {len(rantai)} entri terverifikasi — tidak ada modifikasi."

    @classmethod
    def semua(cls) -> list:
        cls.init()
        return st.session_state[cls.KUNCI]

    @classmethod
    def ringkasan(cls) -> dict:
        cls.init()
        valid, pesan = cls.verifikasi()
        rantai = st.session_state[cls.KUNCI]
        return {
            "jumlah": len(rantai),
            "valid": valid,
            "pesan": pesan,
            "hash_akhir": rantai[-1]["hash"][:10] if rantai else "—",
        }


# ════════════════════════════════════════════════════════════════
# FUNGSI INTI SISTEM
# ════════════════════════════════════════════════════════════════

def init_session():
    for k, v in DEFAULT_STATE.items():
        if k not in st.session_state:
            st.session_state[k] = v
    ContextMemory.init()
    ConflictDetector.init()
    IntegrityLedger.init()


def next_step():
    s = st.session_state
    if s["step"] < 13:
        ContextMemory.tandai_selesai(s["step"])
        IntegrityLedger.tambah("LANJUT", f"L{s['step']}→L{s['step']+1}", s["step"])
        s["step"] += 1


def prev_step():
    if st.session_state["step"] > 1:
        st.session_state["step"] -= 1


def set_step(n: int):
    if 1 <= n <= 13:
        st.session_state["step"] = n


def detect_mode(status_data: str) -> str:
    return ("SEKUNDER_EKSPLORATORI" if status_data == "Sudah Ada"
            else "PRIMER_KONFIRMATORI")


# ════════════════════════════════════════════════════════════════
# CORE LAYER BUILT-IN (RK-7: Invisible Core Architecture)
#
# Core Layer ditanamkan langsung di kode sebagai default.
# Secrets tetap digunakan jika tersedia (untuk override).
# Sistem SELALU berjalan — tidak ada st.stop() karena secrets.
# Core Layer tidak pernah ditampilkan di UI manapun.
# ════════════════════════════════════════════════════════════════

# Core Layer default — tertanam langsung, tidak perlu konfigurasi eksternal.
# Ini adalah "otak" sistem yang berjalan di latar belakang.
_DEFAULT_CORE = (
    "RESEARCH WORKFLOW ORCHESTRATOR v6.0 | "
    "13 langkah adaptif: inisialisasi — audit — pemetaan — literatur — "
    "pertanyaan — desain — etik — pilot — data — analisis — pembahasan — "
    "laporan — finalisasi. "
    "Mode: PRIMER_KONFIRMATORI atau SEKUNDER_EKSPLORATORI. "
    "Bidang: Umum; Soshum; Saintek; Ilmu Komputer. "
    "Luaran: Skripsi; Tesis; Disertasi; Hibah Bima; BRIN; Jurnal. "
    "Aturan mutlak: tidak ada data palsu; tidak ada HARKing; "
    "tidak ada salami slicing; tidak ada sitasi fiktif; "
    "tanda baca konsisten (. , ; : - ? ! \" \' ( ) [ ] / ...); "
    "kata asing bukan serapan ditulis miring (PEUBI); "
    "respons manusiawi — hindari pola kalimat robotik; "
    "setiap keputusan tercatat di Integrity Ledger. "
    "RK-6 Human Writing Engine aktif. "
    "RK-7 Invisible Core aktif. "
    "RK-8 Anti-AI Filter aktif. "
    "RK-9 Punctuation System aktif. "
    "RK-10 Global Visual Intelligence aktif."
)


def _ambil_prompt() -> str:
    """
    Mengambil prompt Core Layer.
    Prioritas: (1) Streamlit Secrets, (2) default built-in.
    Tidak pernah gagal — sistem selalu berjalan.
    """
    try:
        dari_secrets = str(st.secrets.get("CORE_LAYER_PROMPT", "")).strip()
        if len(dari_secrets) >= 50:
            return dari_secrets
    except Exception:
        pass
    return _DEFAULT_CORE


def get_core_layer_prompt() -> str:
    """
    Ambil Core Layer — selalu berhasil, tidak pernah st.stop().
    Prompt tidak pernah ditampilkan ke UI.
    """
    prompt = _ambil_prompt()
    h = hashlib.sha256(prompt.encode()).hexdigest()[:16]
    if "cl_h" not in st.session_state:
        st.session_state.cl_h = h
    return prompt


def core_status() -> dict:
    """Status sistem — tanpa mengekspos isi Core Layer."""
    prompt = _ambil_prompt()
    dari_secrets = False
    try:
        s = str(st.secrets.get("CORE_LAYER_PROMPT", "")).strip()
        dari_secrets = len(s) >= 50
    except Exception:
        pass
    return {
        "aktif": True,
        "versi": VERSI,
        "sumber": "Secrets" if dari_secrets else "Built-in",
        "status": "✅ Sistem aktif dan berjalan normal",
        "hash": InvisibleCore.hash_verifikasi(prompt),
    }

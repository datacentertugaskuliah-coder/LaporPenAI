"""utils.py — Utilitas v6.0: PEUBI Reasoning Engine + helpers."""

import re
import pandas as pd
from datetime import datetime

KBBI_BAKU = {
    "komputer","data","sistem","metode","analisis","model","algoritma","program",
    "aplikasi","basis","jaringan","internet","digital","virtual","proses","produk",
    "standar","teknik","desain","evaluasi","implementasi","integrasi","validasi",
    "komunikasi","informasi","teknologi","inovasi","strategi","manajemen",
    "administrasi","koordinasi","kolaborasi","adaptasi","dokumen","laporan",
    "proposal","publikasi","artikel","jurnal","survei","eksperimen","hipotesis",
    "variabel","parameter","responden","populasi","sampel","instrumen","kuesioner",
    "statistik","regresi","korelasi","distribusi","probabilitas","akurasi","presisi",
    "format","formula","diagram","grafik","tabel","abstrak","sintesis",
}

KATA_ASING = [
    "pilot study","salami slicing","reverse outlining","pre-registrasi",
    "state of the art","gap","HARKing","post hoc","a priori","a posteriori",
    "mixed method","grounded theory","member checking","purposive sampling",
    "snowball sampling","workflow","dashboard","dataset","output","input",
    "logbook","feedback","interface","framework","frontend","backend",
    "software","hardware","online","real-time","cloud","repository","commit",
    "push","branch","merge","deploy","setup","script","library","module",
    "package","plugin","token","login","logout","session","cache","server",
    "client","upload","download","link","hosting","domain","template",
    "custom","default","update","debugging","loop","file","random seed",
    "benchmark","baseline","impact factor","peer review","open access",
    "preprint","cover letter","call for paper","API","URL","DOI",
    "IMRAD","PRISMA","DMP","TKT","TRL","OJS",
]
KATA_ASING_SORTED = sorted(KATA_ASING, key=len, reverse=True)


def m(teks: str) -> str:
    """PEUBI Reasoning Engine — miringkan kata asing bukan serapan."""
    if not isinstance(teks, str):
        return str(teks)
    for kata in KATA_ASING_SORTED:
        if kata.lower() in KBBI_BAKU:
            continue
        pola = r'(?<!\*)(?<![A-Za-z])(' + re.escape(kata) + r')(?![A-Za-z])(?!\*)'
        teks = re.sub(pola, r'*\1*', teks, flags=re.IGNORECASE)
    return teks


def buat_tabel(literatur: list, judul: str, desain: dict) -> pd.DataFrame:
    rows = []
    for i, lit in enumerate(literatur[:5]):
        rows.append({
            "No": i + 1,
            "Penulis (Tahun)": lit.get("penulis_tahun", ""),
            "Judul": lit.get("judul", ""),
            "Metode": lit.get("metode", ""),
            "Hasil": lit.get("hasil", ""),
            "Perbedaan": lit.get("perbedaan", ""),
        })
    met = desain.get("pendekatan", desain.get("rencana_analisis", ""))[:55]
    rows.append({
        "No": 6,
        "Penulis (Tahun)": "[Nama Anda] (Tahun ini)",
        "Judul": judul,
        "Metode": met,
        "Hasil": "Sedang berlangsung",
        "Perbedaan": "Penelitian ini mengembangkan / mengatasi / berfokus pada...",
    })
    return pd.DataFrame(rows)


def fmt_ledger(rantai: list) -> pd.DataFrame:
    if not rantai:
        return pd.DataFrame(columns=["#","Waktu","L","Aksi","Hash"])
    return pd.DataFrame([{
        "#": e.get("urutan","—"),
        "Waktu": e.get("waktu","—"),
        "L": e.get("tahap","—"),
        "Aksi": e.get("aksi","—"),
        "Hash": e.get("hash","—")[:10],
    } for e in rantai])


def waktu_now() -> str:
    return datetime.now().strftime("%d %B %Y, %H:%M")

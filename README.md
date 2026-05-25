# 🔬 Workflow Penyusunan Laporan Penelitian — v6.0

Platform panduan riset terintegrasi dengan Core Layer v6.0
yang mengalami peningkatan 99% dari v5.0.

---

## Yang Dikembangkan di v6.0

| Kode  | Nama | Fungsi |
|-------|------|--------|
| RK-6  | Human Writing Style Engine | Respons terasa ditulis manusia, bukan mesin |
| RK-7  | Invisible Core Architecture | Core Layer sepenuhnya tersembunyi dari UI |
| RK-8  | Anti-AI-Detection Filter | Pola penulisan alami dan bervariasi |
| RK-9  | Punctuation Integrity System | Tanda baca: . , ; : - ? ! " ' ( ) [ ] / … konsisten |
| RK-10 | Global Visual Intelligence | Antarmuka universal, inklusif, responsif |

Ditambah warisan dari v5.0 (RK-1 s/d RK-5) yang dipertahankan dan diperkuat.

---

## Cara Menjalankan Lokal

```bash
git clone https://github.com/USERNAME/riset-dashboard.git
cd riset-dashboard
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Isi CORE_LAYER_PROMPT di secrets.toml dengan konten asli
streamlit run app.py
```

---

## Deploy ke Streamlit Cloud

1. Push ke GitHub — tanpa `secrets.toml` (sudah di `.gitignore`)
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. **New app** → pilih repo → `app.py` → **Advanced settings → Secrets**
4. Tempel isi `secrets.toml` dengan nilai `CORE_LAYER_PROMPT` yang lengkap
5. **Deploy**

---

## Arsitektur Keamanan

- Core Layer tidak pernah ditampilkan di antarmuka pengguna (RK-7)
- Yang terlihat di UI: nama fitur dan hash verifikasi 8 karakter
- Semua keputusan tercatat di Integrity Ledger berbasis rantai hash (RK-5)
- Pemalsuan entri ledger akan terdeteksi saat verifikasi di Langkah 13

---

## Struktur

```
riset-dashboard/
├── .streamlit/
│   └── secrets.toml.example
├── modules/
│   ├── __init__.py
│   ├── core_layer.py
│   └── utils.py
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

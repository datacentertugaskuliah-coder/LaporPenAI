# 🔬 Workflow Penyusunan Laporan Penelitian — v6.0

Platform panduan riset terintegrasi — **langsung berjalan tanpa konfigurasi.**

---

## Cara Menjalankan Lokal

```bash
git clone https://github.com/USERNAME/riset-dashboard.git
cd riset-dashboard
pip install -r requirements.txt
streamlit run app.py
```

Selesai. Tidak perlu mengisi secrets apapun.

---

## Deploy ke Streamlit Cloud

1. Push repo ke GitHub
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. **New app** → pilih repo → `app.py` → **Deploy**

Tidak perlu mengisi Secrets. Sistem langsung berjalan menggunakan
Core Layer built-in.

---

## Core Layer

Sistem menggunakan Core Layer built-in yang sudah tertanam di kode.
Core Layer tidak pernah ditampilkan di antarmuka pengguna (RK-7).

Jika ingin menggunakan Core Layer kustom, isi `CORE_LAYER_PROMPT`
di Streamlit Secrets (opsional — lihat `secrets.toml.example`).

---

## Yang Dikembangkan di v6.0

| Kode  | Nama | Fungsi |
|-------|------|--------|
| RK-6  | Human Writing Style Engine | Respons alami, tidak terdeteksi AI |
| RK-7  | Invisible Core Architecture | Core Layer tersembunyi, berjalan tanpa konfigurasi |
| RK-8  | Anti-AI-Detection Filter | Variasi pola penulisan yang natural |
| RK-9  | Punctuation Integrity System | Tanda baca: . , ; : - ? ! " ' ( ) [ ] / … konsisten |
| RK-10 | Global Visual Intelligence | Antarmuka universal dan responsif |

Ditambah warisan RK-1 s/d RK-5 dari v5.0.

---

## Struktur

```
riset-dashboard/
├── .streamlit/
│   └── secrets.toml.example   (opsional — hanya untuk Core Layer kustom)
├── modules/
│   ├── __init__.py
│   ├── core_layer.py          (Core Layer v6.0 — built-in)
│   └── utils.py
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

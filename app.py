"""
app.py — Workflow Penyusunan Laporan Penelitian v6.0
Mengintegrasikan Core Layer v6.0:
  RK-6  Human Writing Style Engine
  RK-7  Invisible Core Architecture
  RK-8  Anti-AI-Detection Filter
  RK-9  Punctuation Integrity System
  RK-10 Global Visual Intelligence
  + Warisan RK-1 s/d RK-5 dari v5.0
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from modules.core_layer import (
    init_session, next_step, prev_step, set_step, detect_mode,
    get_core_layer_prompt, core_status,
    ReadinessScorer, ContextMemory, RiskFilter,
    ConflictDetector, IntegrityLedger,
    GlobalVisualIntelligence as GVI, PunctuationSystem,
    AntiAIFilter, HumanWritingEngine,
    InvisibleCore, INFO_PENGEMBANGAN,
    STANDAR_LUARAN, PROFIL_BIDANG, THRESHOLD_KESIAPAN,
)
from modules.utils import m, buat_tabel, fmt_ledger, waktu_now

# ════════════════════════════════════════════════════════════════
# KONFIGURASI HALAMAN
# ════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Workflow Riset",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(GVI.CSS_GLOBAL, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# VALIDASI SISTEM (Core Layer tersembunyi — RK-7)
# ════════════════════════════════════════════════════════════════
_prompt = get_core_layer_prompt()
_cs     = core_status()

# ════════════════════════════════════════════════════════════════
# INISIALISASI
# ════════════════════════════════════════════════════════════════
init_session()
S = st.session_state   # alias ringkas

LANGKAH = [
    "Inisialisasi Proyek", "Audit Data", "Pemetaan Multi-Luaran",
    "Studi Literatur", "Pertanyaan Riset", "Desain Metodologi",
    "Izin Etik & Pre-registrasi", "Pilot Study", "Pengumpulan Data",
    "Analisis Data", "Pembahasan", "Penulisan Laporan", "Uji Mutu & Finalisasi",
]

# ════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🔬 Workflow Riset")
    st.caption("Sistem Kecerdasan Penyusunan Laporan Penelitian — v6.0")
    st.divider()

    # Status sistem (RK-7: hanya status, bukan isi Core Layer)
    sumber_label = _cs.get("sumber", "Built-in")
    st.markdown(
        f"{_cs['status']}  \n"
        f"Versi: `{_cs['versi']}` | Sumber: {sumber_label} | ID: `{_cs['hash']}`"
    )

    # Informasi pengembangan (menggantikan eksposur Core Layer)
    with st.expander("ℹ️ Fitur yang Dikembangkan", expanded=False):
        st.markdown("**Peningkatan Baru (v6.0):**")
        for f in INFO_PENGEMBANGAN["fitur_dikembangkan"]:
            st.markdown(f"- {f}")
        st.markdown("**Dipertahankan dari v5.0:**")
        for f in INFO_PENGEMBANGAN["warisan_v5"]:
            st.markdown(f"- {f}")
        st.caption(INFO_PENGEMBANGAN["integritas"])

    # Skor kesiapan riset (RK-1)
    if S.get("judul"):
        skor, detail = ReadinessScorer.hitung(dict(S))
        thresh = THRESHOLD_KESIAPAN.get(S["step"], 60)
        st.markdown(
            GVI.render_skor(skor, thresh),
            unsafe_allow_html=True,
        )

    # Wawasan inferensial (RK-2)
    w_list = ContextMemory.wawasan()
    if w_list:
        with st.expander(f"💡 Wawasan Sistem ({len(w_list)})", expanded=True):
            for w in w_list:
                kelas = "kartu-error" if w["prioritas"]=="tinggi" else "kartu-warn"
                st.markdown(
                    f'<div class="{kelas}">L{w["tahap"]}: {w["pesan"]}</div>',
                    unsafe_allow_html=True,
                )

    # Konflik aktif (RK-4)
    k_aktif = ConflictDetector.aktif()
    if k_aktif:
        with st.expander(f"⚠️ Perlu Perhatian ({len(k_aktif)})"):
            for k in k_aktif:
                st.markdown(
                    f'<div class="kartu-error"><b>{k["tipe"]}</b> (L{k["tahap"]}): '
                    f'{k["deskripsi"]}<br>→ {k["resolusi"]}</div>',
                    unsafe_allow_html=True,
                )

    # Integrity Ledger (RK-5)
    ring = IntegrityLedger.ringkasan()
    with st.expander(f"🔐 Rekam Jejak ({ring['jumlah']} entri)"):
        st.caption(ring["pesan"])
        if ring["jumlah"] > 0:
            st.caption(f"Hash akhir: `{ring['hash_akhir']}`")
            st.dataframe(fmt_ledger(IntegrityLedger.semua()[-5:]),
                         use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Navigasi Langkah")
    for i, label in enumerate(LANGKAH, 1):
        selesai = ContextMemory.sudah_selesai(i)
        aktif   = i == S["step"]
        ikon    = "✅" if selesai else ("▶️" if aktif else "⬜")
        tipe    = "primary" if aktif else "secondary"
        if st.button(f"{ikon} {i}. {label}", key=f"nav_{i}",
                     use_container_width=True, type=tipe):
            if i <= S["step"]:
                set_step(i)
                st.rerun()

    st.divider()
    if S.get("judul"):
        st.info(
            f"📄 **{S['judul'][:35]}{'…' if len(S['judul'])>35 else ''}**\n\n"
            f"Bidang: {S['bidang']}  \n"
            f"Mode: `{S.get('mode','—')}`  \n"
            f"Luaran: {', '.join(S.get('daftar_luaran',[]))}"
        )
    if st.button("🔄 Mulai Ulang", use_container_width=True):
        for k in list(S.keys()):
            del st.session_state[k]
        st.rerun()

# ════════════════════════════════════════════════════════════════
# HEADER UTAMA
# ════════════════════════════════════════════════════════════════
st.title(m("Workflow Penyusunan Laporan Penelitian"))
st.caption(
    "Platform panduan riset terintegrasi — "
    "13 langkah adaptif dengan validasi otomatis dan rekam jejak penuh."
)

# Progress bar Plotly (RK-10: visualisasi global)
tahap = S["step"]
pct   = (tahap - 1) / 12
fig_p = go.Figure(go.Bar(
    x=[pct], y=[""], orientation="h",
    marker_color="#2563EB", width=0.6,
))
fig_p.add_annotation(
    x=min(pct / 2, 0.45), y=0,
    text=f"  Langkah {tahap}/13 — {LANGKAH[tahap-1]}",
    showarrow=False, font=dict(color="white", size=12, family="Inter, sans-serif"),
    xanchor="left",
)
fig_p.update_layout(
    height=38, margin=dict(l=0,r=0,t=0,b=0),
    xaxis=dict(range=[0,1], visible=False),
    yaxis=dict(visible=False),
    plot_bgcolor="#E5E7EB", paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_p, use_container_width=True, config={"displayModeBar": False})

# Navigasi atas
if tahap > 1:
    ca, cb, cc = st.columns([1, 1, 4])
    ca.button("⬅ Sebelumnya", on_click=prev_step, use_container_width=True)
    if tahap < 13:
        cb.button("Selanjutnya ➡", on_click=next_step,
                  use_container_width=True, type="primary")
st.divider()


# ════════════════════════════════════════════════════════════════
# HELPER
# ════════════════════════════════════════════════════════════════



def cek_risiko_teks(teks: str, tahap_n: int) -> bool:
    """Jalankan RiskFilter dan tampilkan hasilnya. Kembalikan True jika ada risiko kritis."""
    ada_kritis = False
    risiko = RiskFilter.pindai(teks)
    for jenis in risiko:
        jd, ps, level = RiskFilter.pesan(jenis)
        kartu(f"**{jd}**  \n{ps}", tipe="error" if level=="error" else "warn")
        if level == "error":
            ada_kritis = True
    return ada_kritis

def kartu(teks: str, tipe: str = "info") -> None:
    """Menampilkan kartu informasi dengan gaya global (RK-10)."""
    kelas_map = {"info": "kartu-info", "warn": "kartu-warn",
                 "error": "kartu-error", "ok": "kartu-ok"}
    kelas = kelas_map.get(tipe, "kartu-info")
    # Terapkan humanisasi (RK-6 + RK-8) dan PEUBI (RK-9)
    teks_h = HumanWritingEngine.humanisasi(m(teks))
    st.markdown(f'<div class="{kelas}">{teks_h}</div>', unsafe_allow_html=True)


def panel_skor_lokal_v2(tahap_n: int) -> bool:
    skor, detail = ReadinessScorer.hitung(dict(S))
    thresh = THRESHOLD_KESIAPAN.get(tahap_n, 60)
    st.markdown(GVI.render_skor(skor, thresh, "Kesiapan Riset Anda"),
                unsafe_allow_html=True)
    if skor < thresh:
        kurang = ReadinessScorer.komponen_kurang(detail)
        if kurang:
            with st.expander("Komponen yang perlu dilengkapi"):
                for k in kurang:
                    st.markdown(f"- {k}")
    return skor >= thresh


# ════════════════════════════════════════════════════════════════
# LANGKAH 1 — Inisialisasi Proyek
# ════════════════════════════════════════════════════════════════
if S["step"] == 1:
    st.header("Langkah 1: Inisialisasi Proyek")
    panel_skor_lokal_v2(1)
    kartu(
        "📌 Langkah ini menetapkan fondasi seluruh riset Anda. "
        "Pilihan di sini — terutama status data — akan menentukan mode riset "
        "dan alur validasi selanjutnya.",
        "info",
    )

    with st.form("f1"):
        judul = st.text_input(
            "Judul Penelitian", value=S["judul"],
            placeholder="Contoh: Pengaruh X terhadap Y pada konteks Z"
        )
        c1, c2 = st.columns(2)
        with c1:
            bidang = st.selectbox(
                "Bidang Ilmu", list(PROFIL_BIDANG.keys()),
                index=list(PROFIL_BIDANG.keys()).index(S["bidang"]),
            )
            profil_b = PROFIL_BIDANG[bidang]
            st.caption(
                f"Pendekatan lazim: **{profil_b['pendekatan']}**  \n"
                f"Analisis: {profil_b['analisis']}"
            )
        with c2:
            status_data = st.radio(
                "Status Data", ["Belum Ada", "Sudah Ada"],
                index=0 if S["status_data"] == "Belum Ada" else 1,
                help=(
                    "'Sudah Ada' → mode SEKUNDER_EKSPLORATORI — klaim konfirmatori dilarang.  \n"
                    "'Belum Ada' → mode PRIMER_KONFIRMATORI — desain bebas sesuai rencana."
                ),
            )
        luaran = st.multiselect(
            "Luaran yang Diharapkan",
            list(STANDAR_LUARAN.keys()),
            default=S["daftar_luaran"],
        )
        if luaran:
            with st.expander("Lihat standar tiap luaran"):
                for lu in luaran:
                    std = STANDAR_LUARAN[lu]
                    st.markdown(
                        f"**{lu}** — Kedalaman: {std['depth']} | "
                        f"Halaman: {std['halaman']} | "
                        f"Artikel wajib: {'Ya' if std['artikel_wajib'] else 'Tidak'} | "
                        f"TKT/TRL: {std['tkt']}"
                    )
        kirim = st.form_submit_button("💾 Simpan dan Lanjutkan", type="primary")

    if kirim:
        galat = []
        if not judul.strip():
            galat.append("Judul penelitian tidak boleh kosong.")
        if not luaran:
            galat.append("Pilih minimal satu luaran.")
        if galat:
            for g in galat:
                st.error(g)
        else:
            S["judul"]          = judul.strip()
            S["bidang"]         = bidang
            S["status_data"]    = status_data
            S["daftar_luaran"]  = luaran
            S["mode"]           = detect_mode(status_data)
            ContextMemory.kunci("mode", S["mode"], "Ditetapkan L1 — berdasar status data.")
            ContextMemory.catat("INISIALISASI", S["mode"], 1, "Parameter awal proyek.")
            IntegrityLedger.tambah("INISIALISASI", S["judul"], 1, f"Mode={S['mode']}")
            ConflictDetector.periksa(dict(S), 1)
            kartu(f"✅ Proyek disimpan. Mode riset: **{S['mode']}**", "ok")
            next_step()
            st.rerun()


# ════════════════════════════════════════════════════════════════
# LANGKAH 2 — Audit Data
# ════════════════════════════════════════════════════════════════
elif S["step"] == 2:
    st.header(m("Langkah 2: Audit Data"))

    if S["mode"] == "SEKUNDER_EKSPLORATORI":
        kartu(
            "⚠️ Mode ini mengharuskan Anda jujur soal asal data. "
            "Tiga hal yang perlu dikonfirmasi: izin penggunaan, anonimisasi, "
            "dan kesadaran bahwa analisis bersifat eksploratori — bukan konfirmatori.",
            "warn",
        )
        tab1, tab2 = st.tabs([m("Unggah *File*"), "Deklarasi Manual"])
        with tab1:
            uf = st.file_uploader(m("*File* CSV atau Excel"), type=["csv","xlsx"])
            if uf:
                try:
                    df_a = (pd.read_csv(uf) if uf.name.endswith(".csv")
                            else pd.read_excel(uf))
                    st.dataframe(df_a.head(8), use_container_width=True)
                    c1,c2,c3 = st.columns(3)
                    c1.metric("Baris", f"{len(df_a):,}")
                    c2.metric("Kolom", len(df_a.columns))
                    miss = int(df_a.isnull().sum().sum())
                    pct_miss = round(miss / max(df_a.size,1) * 100, 1)
                    c3.metric(m("*Missing Values*"), miss, f"{pct_miss}%",
                              delta_color="inverse")
                    if pct_miss > 30:
                        kartu(
                            f"Missing values cukup tinggi ({pct_miss}%). "
                            "Dokumentasikan penanganannya di bagian metodologi.", "warn"
                        )
                    S["ada_upload_data"] = True
                except Exception as e:
                    st.error(f"Gagal membaca file: {e}")
        with tab2:
            st.text_area("Deskripsi sumber data (asal, periode, pengumpul)", height=100)

        st.divider()
        cb1 = st.checkbox("✅ Saya memiliki izin sah untuk menggunakan data ini")
        cb2 = st.checkbox("✅ Data sudah dianonimkan atau tidak mengandung informasi sensitif tanpa proteksi")
        cb3 = st.checkbox(
            m("✅ Saya memahami bahwa analisis bersifat eksploratori — "
              "klaim konfirmatori tidak dapat dibuat dari data ini")
        )
        if st.button("✅ Konfirmasi dan Lanjutkan", type="primary"):
            if cb1 and cb2 and cb3:
                S["data_audit_passed"] = True
                ContextMemory.catat("AUDIT_SELESAI", "Sekunder", 2, "Izin dikonfirmasi.")
                IntegrityLedger.tambah("AUDIT_DATA", "Audit data sekunder selesai", 2)
                next_step(); st.rerun()
            else:
                st.error("Centang semua pernyataan untuk melanjutkan.")
    else:
        kartu("✅ Mode PRIMER_KONFIRMATORI — audit data tidak diperlukan. Silakan lanjutkan.", "ok")
        if st.button("Lanjutkan ➡", type="primary"):
            IntegrityLedger.tambah("AUDIT_SKIP", "Primer — tidak perlu audit", 2)
            next_step(); st.rerun()


# ════════════════════════════════════════════════════════════════
# LANGKAH 3 — Pemetaan Multi-Luaran
# ════════════════════════════════════════════════════════════════
elif S["step"] == 3:
    st.header(m("Langkah 3: Pemetaan Multi-Luaran"))
    kartu(
        "📌 Setiap luaran harus menjawab pertanyaan yang berbeda secara substansial "
        "dan/atau menggunakan subset data yang berbeda. "
        "Kalau dua luaran terlihat hampir identik, itu indikasi salami slicing — "
        "dan itu masalah serius di dunia publikasi.",
        "info",
    )

    peta = {}
    semua = True
    for lu in S["daftar_luaran"]:
        ada = S["peta_luaran"].get(lu, {})
        with st.expander(f"📄 {lu}", expanded=True):
            q = st.text_area("Pertanyaan riset unik untuk luaran ini",
                             value=ada.get("pertanyaan",""), key=f"q_{lu}", height=80)
            s = st.text_input("Subset atau fokus data",
                              value=ada.get("subset",""), key=f"s_{lu}")
            peta[lu] = {"pertanyaan": q.strip(), "subset": s.strip()}
            if not q.strip() or not s.strip():
                semua = False

    if st.button("🔍 Verifikasi Pemetaan", type="primary"):
        if not semua:
            st.error("Isi pertanyaan dan subset untuk semua luaran sebelum melanjutkan.")
        else:
            items = list(peta.values())
            ada_salami = any(
                items[i]["pertanyaan"].lower() == items[j]["pertanyaan"].lower()
                and items[i]["subset"].lower() == items[j]["subset"].lower()
                for i in range(len(items)) for j in range(i+1,len(items))
            )
            if ada_salami:
                _, ps, _ = RiskFilter.pesan("salami")
                kartu(ps, "error")
            else:
                S["peta_luaran"] = peta
                ContextMemory.catat("PEMETAAN", str(list(peta.keys())), 3)
                IntegrityLedger.tambah("PEMETAAN_LUARAN", f"{len(peta)} luaran", 3)
                kartu("✅ Pemetaan valid — tidak ada indikasi salami slicing.", "ok")
                next_step(); st.rerun()


# ════════════════════════════════════════════════════════════════
# LANGKAH 4 — Studi Literatur
# ════════════════════════════════════════════════════════════════
elif S["step"] == 4:
    st.header("Langkah 4: Studi Literatur Sistematis")
    panel_skor_lokal_v2(4)
    protokol = ("PRISMA" if any(lu in ["Disertasi","Jurnal"]
                                for lu in S["daftar_luaran"])
                else "Semi-sistematis")
    kartu(
        f"📌 Protokol yang disarankan untuk luaran Anda: **{protokol}**. "
        "Isi lima penelitian terdahulu yang paling relevan — bukan sembarang lima, "
        "tapi yang benar-benar Anda baca dan pahami isinya.",
        "info",
    )

    lit = []
    n_valid = 0
    for i in range(5):
        ada = S["literatur"][i] if len(S["literatur"]) > i else {}
        with st.expander(f"📚 Penelitian {i+1}", expanded=(i < 2)):
            c1, c2 = st.columns(2)
            with c1:
                pen = st.text_input("Penulis (Tahun)", value=ada.get("penulis_tahun",""),
                                    key=f"pen{i}", placeholder="Doe & Smith (2022)")
                jud = st.text_input("Judul", value=ada.get("judul",""), key=f"jud{i}")
                met = st.text_input("Metode", value=ada.get("metode",""), key=f"met{i}")
            with c2:
                has = st.text_area("Hasil Utama", value=ada.get("hasil",""),
                                   key=f"has{i}", height=90)
                per = st.text_input("Perbedaan dengan riset Anda",
                                    value=ada.get("perbedaan",""), key=f"per{i}")
            if pen.strip() and jud.strip():
                n_valid += 1
            lit.append({
                "penulis_tahun": pen.strip(), "judul": jud.strip(),
                "metode": met.strip(), "hasil": has.strip(), "perbedaan": per.strip(),
            })

    st.caption(f"Terisi: {n_valid} dari 5 penelitian")
    if st.button("💾 Simpan Literatur dan Lanjutkan", type="primary"):
        if n_valid < 5:
            st.error("Harap isi minimal penulis dan judul untuk semua 5 penelitian.")
        else:
            S["literatur"] = lit
            ContextMemory.catat("LITERATUR", f"{n_valid} studi", 4, protokol)
            IntegrityLedger.tambah("LITERATUR", f"{n_valid} studi ({protokol})", 4)
            kartu("✅ Literatur disimpan.", "ok")
            next_step(); st.rerun()


# ════════════════════════════════════════════════════════════════
# LANGKAH 5 — Pertanyaan Riset
# ════════════════════════════════════════════════════════════════
elif S["step"] == 5:
    st.header("Langkah 5: Perumusan Pertanyaan Riset")

    if S["mode"] == "SEKUNDER_EKSPLORATORI":
        kartu(
            "⚠️ Karena data sudah ada sebelum pertanyaan dirumuskan, "
            "gunakan frasa yang jujur mencerminkan eksplorasi: "
            "'mengidentifikasi', 'mendeskripsikan', 'mengeksplorasi'. "
            "Hindari 'membuktikan' atau 'menguji hipotesis bahwa'.",
            "warn",
        )
    else:
        kartu(
            "📌 Pertanyaan ini akan dikunci setelah langkah ini selesai. "
            "Artinya, tidak boleh diubah berdasarkan hasil analisis nanti — "
            "itu yang disebut HARKing, dan dampaknya serius.",
            "info",
        )

    pertanyaan = st.text_area(
        "Pertanyaan Riset Utama", value=S["pertanyaan_utama"], height=120,
        placeholder="Bagaimana pengaruh [X] terhadap [Y] pada [konteks Z]?",
    )

    # Deteksi HARKing proaktif (RK-3 + RK-8)
    if pertanyaan.strip():
        ada_kritis = cek_risiko_teks(pertanyaan, 5)
        # Periksa konsistensi tanda baca (RK-9)
        masalah_tb = PunctuationSystem.validasi_dasar(pertanyaan)
        for mt in masalah_tb:
            kartu(f"Catatan tanda baca: {mt}", "warn")

    if st.button("💾 Simpan dan Kunci Pertanyaan", type="primary"):
        if len(pertanyaan.strip()) < 20:
            st.error("Pertanyaan terlalu pendek — jelaskan variabel dan konteksnya.")
        else:
            S["pertanyaan_utama"] = pertanyaan.strip()
            ContextMemory.kunci("pertanyaan_utama", pertanyaan.strip(),
                                "Dikunci L5 — perubahan pasca-analisis = HARKing.")
            ContextMemory.catat("PERTANYAAN_DIKUNCI", pertanyaan[:80], 5)
            IntegrityLedger.tambah("PERTANYAAN_KUNCI", pertanyaan[:100], 5,
                                   "Kunci integritas pertanyaan riset.")
            kartu("✅ Pertanyaan dikunci dan tercatat dalam rekam jejak.", "ok")
            next_step(); st.rerun()


# ════════════════════════════════════════════════════════════════
# LANGKAH 6 — Desain Metodologi
# ════════════════════════════════════════════════════════════════
elif S["step"] == 6:
    st.header(m("Langkah 6: Desain Metodologi"))
    panel_skor_lokal_v2(6)

    profil_b = PROFIL_BIDANG.get(S["bidang"], {})
    kartu(
        f"🎯 Untuk bidang **{S['bidang']}**, pendekatan yang paling lazim adalah "
        f"**{profil_b.get('pendekatan','—')}** dengan analisis "
        f"{profil_b.get('analisis','—')}. "
        f"Instrumen yang biasa digunakan: {profil_b.get('instrumen','—')}.",
        "info",
    )

    if any(lu in ["Hibah Bima","BRIN"] for lu in S["daftar_luaran"]):
        kartu(
            "💡 Karena Anda menargetkan hibah/BRIN, cantumkan target TKT atau TRL "
            "sejak rancangan awal — reviewer akan mencarinya di proposal.",
            "info",
        )

    if S["mode"] == "PRIMER_KONFIRMATORI":
        with st.form("f6"):
            PEND = ["Kuantitatif","Kualitatif","Campuran","Eksperimental","Pengembangan Sistem"]
            idx_p = PEND.index(S["desain"].get("pendekatan","Kuantitatif")) if S["desain"].get("pendekatan") in PEND else 0
            c1, c2 = st.columns(2)
            with c1:
                pend = st.selectbox("Pendekatan", PEND, index=idx_p)
                samp = st.text_input("Populasi / Sampel", value=S["desain"].get("sampel",""))
            with c2:
                inst = st.text_area("Instrumen / Alat Ukur",
                                    value=S["desain"].get("instrumen",""), height=100)

            if S["bidang"] == "Ilmu Komputer":
                st.markdown(m("**Detail Ilmu Komputer**"))
                c3, c4 = st.columns(2)
                with c3:
                    ds   = st.text_input(m("*Dataset*"), value=S["desain"].get("dataset_info",""))
                    seed = st.text_input(m("*Random seed*"), value=S["desain"].get("random_seed","42"))
                with c4:
                    metr = st.text_input("Metrik evaluasi", value=S["desain"].get("metrik",""),
                                        placeholder="Akurasi, F1, AUC, RMSE…")
                    base = st.text_input(m("*Baseline*"), value=S["desain"].get("baseline",""))
            elif S["bidang"] == "Soshum":
                prot = st.text_area("Protokol wawancara / pedoman",
                                    value=S["desain"].get("protokol_w",""), height=80)

            kirim6 = st.form_submit_button("💾 Simpan Desain", type="primary")

        if kirim6:
            if not samp.strip():
                st.error("Populasi/sampel tidak boleh kosong.")
            else:
                desain = {"pendekatan": pend, "sampel": samp, "instrumen": inst}
                if S["bidang"] == "Ilmu Komputer":
                    desain.update({"dataset_info": ds,"random_seed": seed,
                                   "metrik": metr,"baseline": base})
                elif S["bidang"] == "Soshum":
                    desain["protokol_w"] = prot
                S["desain"] = desain
                ConflictDetector.periksa(dict(S), 6)
                ContextMemory.kunci("pendekatan", pend, "Ditetapkan L6.")
                ContextMemory.catat("DESAIN", pend, 6)
                IntegrityLedger.tambah("DESAIN", pend, 6, f"Bidang={S['bidang']}")
                kartu("✅ Desain metodologi disimpan.", "ok")
                next_step(); st.rerun()
    else:
        with st.form("f6s"):
            renc = st.text_area("Rencana Analisis Data Sekunder",
                                value=S["desain"].get("rencana_analisis",""), height=150)
            if st.form_submit_button("💾 Simpan", type="primary"):
                if not renc.strip():
                    st.error("Rencana analisis tidak boleh kosong.")
                else:
                    S["desain"] = {"rencana_analisis": renc.strip(),
                                   "pendekatan": "Analisis Sekunder"}
                    IntegrityLedger.tambah("DESAIN_SEK", "Rencana analisis sekunder", 6)
                    kartu("✅ Rencana analisis disimpan.", "ok")
                    next_step(); st.rerun()


# ════════════════════════════════════════════════════════════════
# LANGKAH 7 — Izin Etik & Pre-registrasi
# ════════════════════════════════════════════════════════════════
elif S["step"] == 7:
    st.header(m("Langkah 7: Izin Etik & Pre-registrasi"))

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Izin Etik")
        kartu(
            "Wajib jika penelitian melibatkan manusia sebagai partisipan, "
            "data sensitif, atau eksperimen biologis.",
            "info",
        )
        ie  = st.checkbox("✅ Izin etik sudah diperoleh", value=S["izin_etik"])
        st.text_input("Nomor izin etik (opsional)", key="no_etik")
    with c2:
        st.subheader(m("*Pre-registrasi*"))
        kartu(
            m("Pre-registrasi di OSF atau AsPredicted mendaftarkan hipotesis "
              "sebelum data dikumpulkan. Langkah ini terbukti meningkatkan "
              "kepercayaan reviewer — terutama untuk jurnal Q1 dan Q2."),
            "info",
        )
        pr  = st.checkbox(m("✅ *Pre-registrasi* sudah dilakukan"), value=S["pre_reg"])
        lpr = st.text_input(m("*Link pre-registrasi*"), value=S["link_pre_reg"])

    if st.button("Lanjutkan ➡", type="primary"):
        S["izin_etik"]    = ie
        S["pre_reg"]      = pr
        S["link_pre_reg"] = lpr
        if (S["mode"]=="PRIMER_KONFIRMATORI"
                and S["bidang"] in ["Soshum","Umum"] and not ie):
            kartu(
                "Penelitian Soshum/Umum yang melibatkan manusia umumnya "
                "memerlukan izin etik. Pastikan sudah diperoleh sebelum turun lapangan.",
                "warn",
            )
        ContextMemory.catat("ETIK_PREREG", f"Etik={ie} PreReg={pr}", 7)
        IntegrityLedger.tambah("ETIK_PREREG", f"Etik={ie} PreReg={pr}", 7)
        next_step(); st.rerun()


# ════════════════════════════════════════════════════════════════
# LANGKAH 8 — Pilot Study
# ════════════════════════════════════════════════════════════════
elif S["step"] == 8:
    st.header(m("Langkah 8: Pilot Study"))

    if S["mode"] == "PRIMER_KONFIRMATORI":
        kartu(
            m("Pilot study dengan sekitar 10% dari ukuran sampel target "
              "adalah investasi kecil yang nilainya besar — "
              "jauh lebih murah daripada mengulang seluruh pengumpulan data "
              "karena instrumen yang ternyata tidak valid. "
              "Threshold yang disarankan: Cronbach α ≥ 0,70."),
            "info",
        )
        with st.form("f8"):
            c1, c2 = st.columns(2)
            with c1:
                rel = st.slider(m("Reliabilitas (α / κ)"), 0.0, 1.0,
                                S.get("pilot_reliabilitas",0.7), 0.01)
                n_p = st.number_input(m("Jumlah partisipan *pilot*"), min_value=1, value=10)
            with c2:
                has_p = st.text_area(m("Ringkasan Hasil *Pilot*"), height=100)
                tind  = st.text_area("Tindakan Korektif", height=70)
            k8 = st.form_submit_button(m("💾 Simpan *Pilot Study*"), type="primary")

        if k8:
            if not has_p.strip():
                st.error(m("Hasil pilot tidak boleh kosong."))
            else:
                S["pilot_passed"]       = True
                S["pilot_reliabilitas"] = rel
                if rel < 0.70:
                    kartu(
                        f"Reliabilitas {rel:.2f} masih di bawah 0,70. "
                        "Pertimbangkan merevisi instrumen sebelum lanjut ke pengumpulan data penuh.",
                        "warn",
                    )
                ContextMemory.catat("PILOT", f"α={rel:.2f} n={n_p}", 8)
                IntegrityLedger.tambah("PILOT", f"α={rel:.2f}", 8, f"n={n_p}")
                kartu(f"✅ Pilot study selesai — α = {rel:.2f}.", "ok")
                next_step(); st.rerun()
    else:
        kartu(
            m("Mode SEKUNDER_EKSPLORATORI tidak memerlukan pilot study — "
              "data sudah tersedia."),
            "ok",
        )
        if st.button("Lanjutkan ➡", type="primary"):
            next_step(); st.rerun()


# ════════════════════════════════════════════════════════════════
# LANGKAH 9 — Pengumpulan Data
# ════════════════════════════════════════════════════════════════
elif S["step"] == 9:
    st.header(m("Langkah 9: Pengumpulan / Penyiapan Data"))
    iter_ke = S["current_iterasi"]
    if iter_ke > 0:
        kartu(
            f"Ini iterasi ke-{iter_ke} pengumpulan data tambahan. "
            "Pertanyaan riset tidak boleh diubah — kalau diubah, "
            "itu masuk kategori HARKing.",
            "warn",
        )

    if S["mode"] == "PRIMER_KONFIRMATORI":
        tab1, tab2 = st.tabs([m("Unggah *File*"), m("*Logbook* Manual")])
        with tab1:
            df_up = st.file_uploader(m("*File* CSV/Excel"), type=["csv","xlsx"],key="up9")
            if df_up:
                try:
                    df_d = (pd.read_csv(df_up) if df_up.name.endswith(".csv")
                            else pd.read_excel(df_up))
                    st.dataframe(df_d.head(8), use_container_width=True)
                    c1,c2,c3 = st.columns(3)
                    c1.metric("Baris", f"{len(df_d):,}")
                    c2.metric("Kolom", len(df_d.columns))
                    c3.metric(m("*Missing*"), int(df_d.isnull().sum().sum()))
                    ConflictDetector.periksa(dict(S), 9)
                    if st.button("💾 Simpan Data", type="primary"):
                        S["ada_upload_data"] = True
                        ContextMemory.catat("DATA", f"{len(df_d)}×{len(df_d.columns)}", 9)
                        IntegrityLedger.tambah("DATA", f"{len(df_d)} baris", 9)
                        kartu("✅ Data disimpan.", "ok")
                        next_step(); st.rerun()
                except Exception as e:
                    st.error(f"Gagal membaca file: {e}")
            else:
                if st.button(m("Lanjut tanpa *upload*")):
                    next_step(); st.rerun()
        with tab2:
            ent = st.text_area(m("Entri *logbook*"), height=120,
                               placeholder="Aktivitas hari ini, kendala, keputusan…")
            if st.button("Simpan Entri dan Lanjutkan"):
                ContextMemory.catat("LOGBOOK", ent[:100], 9)
                IntegrityLedger.tambah("LOGBOOK", ent[:100], 9)
                next_step(); st.rerun()
    else:
        kartu("✅ Data sekunder sudah tersedia — siap dianalisis.", "ok")
        if st.button("Lanjutkan ➡", type="primary"):
            next_step(); st.rerun()


# ════════════════════════════════════════════════════════════════
# LANGKAH 10 — Analisis Data
# ════════════════════════════════════════════════════════════════
elif S["step"] == 10:
    st.header(m("Langkah 10: Analisis Data"))
    panel_skor_lokal_v2(10)

    iter_ke = S["current_iterasi"]
    kartu(
        m(f"Iterasi ke-{iter_ke+1} dari maksimum {S['max_iterasi']+1}. "
          "Kalau hasil belum memadai dan data tambahan diperlukan, "
          "bisa kembali ke Langkah 9 — tapi pertanyaan riset tidak boleh diubah. "
          "Hasil yang tidak signifikan bukan kegagalan; itu adalah temuan."),
        "info",
    )

    with st.form("f10"):
        hasil = st.text_area(
            "Ringkasan Hasil Analisis", value=S["hasil_analisis"], height=200,
            placeholder="Temuan utama, nilai statistik, pola yang ditemukan…",
        )
        memadai = st.radio("Hasil sudah memadai?",
                           ["Ya — lanjut ke pembahasan",
                            "Belum — perlu data tambahan (iterasi)"])
        k10 = st.form_submit_button("💾 Simpan dan Lanjutkan", type="primary")

    if k10:
        ada_k = cek_risiko_teks(hasil, 10)
        masalah_mode = RiskFilter.konsistensi_mode(hasil, S.get("mode",""))
        for mm in masalah_mode:
            kartu(mm, "warn")

        # Audit tanda baca (RK-9)
        for mt in PunctuationSystem.validasi_dasar(hasil):
            kartu(f"Catatan tanda baca: {mt}", "warn")

        if not hasil.strip():
            st.error("Hasil analisis tidak boleh kosong.")
        elif not ada_k:
            S["hasil_analisis"] = hasil.strip()
            if "Belum" in memadai and iter_ke < S["max_iterasi"] and S["mode"]=="PRIMER_KONFIRMATORI":
                S["current_iterasi"] += 1
                ContextMemory.catat("ITERASI", f"Ke-{S['current_iterasi']}", 10)
                IntegrityLedger.tambah("ITERASI", f"Iterasi {S['current_iterasi']}", 10)
                kartu(
                    f"⚠️ Iterasi ke-{S['current_iterasi']} dimulai. "
                    "Kembali ke Langkah 9 untuk mengumpulkan data tambahan.",
                    "warn",
                )
                set_step(9); st.rerun()
            else:
                if "Belum" in memadai:
                    kartu("Batas iterasi tercapai. Akui keterbatasan ini secara jujur di pembahasan.", "warn")
                ContextMemory.catat("ANALISIS_SELESAI", hasil[:80], 10)
                IntegrityLedger.tambah("ANALISIS", hasil[:80], 10)
                kartu("✅ Analisis disimpan.", "ok")
                next_step(); st.rerun()


# ════════════════════════════════════════════════════════════════
# LANGKAH 11 — Pembahasan
# ════════════════════════════════════════════════════════════════
elif S["step"] == 11:
    st.header("Langkah 11: Pembahasan dan Sintesis")
    kartu(
        "📌 Struktur yang terbukti efektif: "
        "(1) jawab pertanyaan riset berdasarkan hasil; "
        "(2) bandingkan dengan literatur — di mana sama, di mana berbeda; "
        "(3) jelaskan mengapa hasilnya demikian; "
        "(4) akui keterbatasan secara jujur; "
        "(5) sampaikan implikasi teoretis dan praktis.",
        "info",
    )

    pb = st.text_area("Tuliskan Pembahasan", value=S["pembahasan"], height=300)

    if pb.strip():
        cek_risiko_teks(pb, 11)
        for mm in RiskFilter.konsistensi_mode(pb, S.get("mode","")):
            kartu(mm, "warn")
        ConflictDetector.periksa(dict(S), 11)
        # Tanda baca (RK-9)
        for mt in PunctuationSystem.validasi_dasar(pb):
            kartu(f"Catatan tanda baca: {mt}", "warn")

    if S["current_iterasi"] > 0:
        kartu(
            f"Jangan lupa menyebutkan bahwa dilakukan {S['current_iterasi']} "
            "iterasi pengumpulan data tambahan di bagian keterbatasan.",
            "warn",
        )

    if st.button("💾 Simpan Pembahasan dan Lanjutkan", type="primary"):
        if len(pb.strip()) < 50:
            st.error("Pembahasan terlalu singkat — kembangkan lebih lanjut.")
        else:
            S["pembahasan"] = pb.strip()
            ContextMemory.catat("PEMBAHASAN", pb[:80], 11)
            IntegrityLedger.tambah("PEMBAHASAN", pb[:80], 11)
            kartu("✅ Pembahasan disimpan.", "ok")
            next_step(); st.rerun()


# ════════════════════════════════════════════════════════════════
# LANGKAH 12 — Penulisan Laporan & Tabel Perbandingan
# ════════════════════════════════════════════════════════════════
elif S["step"] == 12:
    st.header("Langkah 12: Penulisan Laporan dan Tabel Perbandingan")
    panel_skor_lokal_v2(12)

    if not S["literatur"]:
        kartu("Literatur belum diisi — kembali ke Langkah 4 terlebih dahulu.", "error")
        if st.button("⬅ Kembali ke Langkah 4"):
            set_step(4); st.rerun()
        st.stop()

    st.subheader("Tabel Perbandingan 6 Studi")
    kartu(
        "📌 Tabel ini wajib berisi tepat 6 baris: 5 penelitian terdahulu "
        "ditambah 1 penelitian Anda. "
        "Kolom 'Perbedaan' harus spesifik — bukan sekadar 'lebih baik' atau "
        "'berbeda'. Tunjukkan apa yang membedakan secara konkret.",
        "info",
    )

    df_init = buat_tabel(S["literatur"], S["judul"], S["desain"])
    tbl = st.data_editor(df_init, key="tbl12", num_rows="fixed",
                         use_container_width=True)

    st.divider()
    st.subheader("Aturan Visual Wajib")
    st.caption(
        "Setiap tabel dan gambar dalam laporan harus memenuhi tiga syarat ini:  \n"
        "• **Judul** di atas tabel — format: *Tabel N. Judul yang Informatif.*  \n"
        "• **Deskripsi analitis** di dalam teks — bukan sekadar mengulang judul.  \n"
        "• **Rujukan eksplisit** dalam paragraf — contoh: 'seperti tampak pada Tabel 2…'"
    )
    cb1 = st.checkbox("✅ Semua tabel dan gambar memiliki judul informatif")
    cb2 = st.checkbox("✅ Semua tabel dan gambar ada deskripsi analitisnya di teks")
    cb3 = st.checkbox("✅ Semua tabel dan gambar dirujuk secara eksplisit di teks")

    if st.button("✅ Validasi dan Lanjutkan", type="primary"):
        valid, pesan, masalah = RiskFilter.validasi_tabel(tbl)
        if not valid:
            kartu(f"❌ {pesan}", "error")
            for mas in masalah:
                st.markdown(f"  - {mas}")
        elif not (cb1 and cb2 and cb3):
            st.error("Centang semua aturan visual sebelum melanjutkan.")
        else:
            S["tabel_comparison"] = tbl.to_dict()
            ContextMemory.catat("TABEL_VALID", "6 studi valid", 12)
            IntegrityLedger.tambah("TABEL", "6 baris tervalidasi", 12, "RK-3")
            kartu("✅ Tabel valid dan aturan visual terpenuhi.", "ok")
            next_step(); st.rerun()


# ════════════════════════════════════════════════════════════════
# LANGKAH 13 — Uji Mutu & Finalisasi
# ════════════════════════════════════════════════════════════════
elif S["step"] == 13:
    st.header(m("Langkah 13: Uji Mutu dan Finalisasi"))

    # Verifikasi Integrity Ledger (RK-5)
    valid_led, pesan_led = IntegrityLedger.verifikasi()
    kartu(f"🔐 Rekam Jejak: {pesan_led}", "ok" if valid_led else "error")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader(m("Uji Koherensi (*Reverse Outlining*)"))
        cb_alur  = st.checkbox(m("✅ Alur argumen logis dan koheren — *reverse outlining* selesai"))
        cb_kons  = st.checkbox("✅ Terminologi konsisten di seluruh dokumen")
        cb_jawab = st.checkbox("✅ Semua pertanyaan riset terjawab di hasil dan simpulan")
        cb_kausal = (True if S.get("mode") != "SEKUNDER_EKSPLORATORI"
                     else st.checkbox("✅ Tidak ada klaim kausal tanpa dukungan desain eksperimental"))
    with c2:
        st.subheader("Plagiarisme dan Etika")
        st.caption(m("Disarankan: *Turnitin*, *iThenticate*, atau Unicheck."))
        cb_plag  = st.checkbox(m("✅ Pemeriksaan plagiarisme selesai"))
        cb_sitas = st.checkbox("✅ Semua kutipan dan parafrase memiliki sitasi yang tepat")
        cb_hki   = st.checkbox("✅ HKI dan hak cipta sudah dipertimbangkan")

    # Konflik aktif
    k_aktif = ConflictDetector.aktif()
    if k_aktif:
        kartu(
            f"⚠️ Masih ada {len(k_aktif)} hal yang perlu diklarifikasi — "
            "lihat di sidebar sebelum finalisasi.",
            "warn",
        )

    st.divider()
    # Ringkasan proyek
    st.subheader("Ringkasan Proyek")
    ring_led = IntegrityLedger.ringkasan()
    df_ring = pd.DataFrame({
        "Parameter": [
            "Judul Penelitian", "Bidang Ilmu", "Mode Riset",
            "Luaran", "Iterasi Data", "Pre-registrasi",
            "Konflik Aktif", "Rekam Jejak", "Waktu Finalisasi",
        ],
        "Nilai": [
            S["judul"], S["bidang"], S.get("mode","—"),
            ", ".join(S["daftar_luaran"]),
            str(S["current_iterasi"]),
            "✅ Ya" if S["pre_reg"] else "⬜ Tidak",
            str(len(k_aktif)),
            ring_led["pesan"][:55],
            waktu_now() if all([cb_alur,cb_kons,cb_jawab,cb_kausal,
                                cb_plag,cb_sitas,cb_hki]) else "—",
        ],
    })
    st.dataframe(df_ring, use_container_width=True, hide_index=True)

    semua_ok = all([cb_alur,cb_kons,cb_jawab,cb_kausal,
                    cb_plag,cb_sitas,cb_hki, valid_led])

    if st.button("🏁 Finalisasi Laporan", type="primary", disabled=not semua_ok):
        S["finalisasi_done"] = True
        IntegrityLedger.tambah("FINALISASI", "Laporan final", 13, "Semua uji mutu terpenuhi.")
        kartu(
            "✅ **Laporan dinyatakan FINAL.** "
            "Semua uji mutu terpenuhi dan rekam jejak terverifikasi. "
            "Langkah berikutnya: diseminasi sesuai target luaran masing-masing.",
            "ok",
        )
        st.balloons()

    if not semua_ok:
        st.caption("Centang semua item di atas dan pastikan rekam jejak valid untuk mengaktifkan finalisasi.")

    if S.get("finalisasi_done"):
        st.divider()
        st.subheader("Panduan Diseminasi")
        panduan_dis = {
            "Jurnal":      m("**Jurnal**: *Submit* via sistem OJS jurnal target. Sertakan *cover letter* yang menjelaskan kontribusi spesifik. Pantau proses *peer review* dan siapkan respons revisi yang substantif."),
            "Hibah Bima":  "**Hibah Bima**: Unggah laporan ke portal Bima. Lengkapi semua luaran wajib yang dijanjikan — artikel, HKI, prototipe — sesuai kontrak.",
            "BRIN":        "**BRIN**: Unggah laporan tahunan ke portal BRIN. Cantumkan capaian TKT/TRL secara eksplisit beserta bukti pendukungnya.",
            "Skripsi":     "**Skripsi**: Serahkan ke perpustakaan institusi dan daftarkan ke Garuda Scholar.",
            "Tesis":       "**Tesis**: Repositori institusi, lalu pertimbangkan mengonversi satu bab menjadi artikel untuk Jurnal Sinta 2.",
            "Disertasi":   "**Disertasi**: Wajib minimal satu artikel di jurnal Q1 atau Q2 sebelum atau bersamaan dengan sidang. Daftarkan ke repositori nasional.",
        }
        for lu in S["daftar_luaran"]:
            st.markdown(f"- {panduan_dis.get(lu, f'**{lu}**: ikuti panduan resmi dari institusi atau lembaga pemberi dana.')}")

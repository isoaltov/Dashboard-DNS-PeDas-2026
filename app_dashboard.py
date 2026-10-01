import os
import pandas as pd
from PIL import Image
import streamlit as st

# =====================================================================
# 1. KONFIGURASI HALAMAN
# =====================================================================
st.set_page_config(
    page_title="Dashboard Analytics DNS .id",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================================
# 2. CSS KUSTOM UNTUK STYLING
# =====================================================================
st.markdown(
    """
<style>
    .kpi-title { font-size: 14px !important; color: #64748b; margin-bottom: -10px; font-weight: 600; }
    .kpi-value { font-size: 32px !important; font-weight: 800; color: #0f172a; }
    .kpi-desc { font-size: 13px !important; color: #94a3b8; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; }
</style>
""",
    unsafe_allow_html=True,
)


# =====================================================================
# 3. HELPER FUNCTION
# =====================================================================
def load_image(filename):
  """Memuat gambar secara aman dari beberapa direktori alternatif."""
  candidates = [
      os.path.join("dns_analytics_output", filename),
      os.path.join("04_Hasil_Keluaran", filename),
      os.path.join("..", "04_Hasil_Keluaran", filename),
      filename,
  ]
  for p in candidates:
    if os.path.exists(p):
      return Image.open(p)
  return None


# =====================================================================
# 4. HEADER UTAMA
# =====================================================================
st.title("📊 Dashboard Business Analytics DNS ccTLD .id")
st.caption(
    "Pesta Data Nasional (PeDaS) 2026 — Dibuat untuk Evaluasi Kinerja &"
    " Kapasitas Infrastruktur PANDI"
)
st.markdown("*(Status: Blind Review Compliant — Tim TIF Sukses Lancar Rejeki)*")
st.divider()

# =====================================================================
# 5. KPI GRID
# =====================================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
  st.metric(
      label="Total Paket Dianalisis",
      value="11.712.623",
      delta="Dalam 30 Menit (2,4 GB)",
      delta_color="off",
  )
with col2:
  st.metric(
      label="Latensi Internal PANDI",
      value="83,9 µs",
      delta="Sangat Responsif (< 0,1 ms)",
      delta_color="normal",
  )
with col3:
  st.metric(
      label="Paket UDP Terpotong (tc=1)",
      value="321.798",
      delta="Memicu 510K+ Koneksi TCP",
      delta_color="inverse",
  )
with col4:
  st.metric(
      label="Beban Kueri Pareto (Top 3)",
      value="27,23%",
      delta="1,59 Juta Kueri Parasit",
      delta_color="inverse",
  )

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================================
# 6. TABS UTAMA
# =====================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 1. Distorsi Pareto",
    "🛡️ 2. Amplifikasi DNSSEC",
    "🗑️ 3. Mitos NXDOMAIN",
    "🗄️ 4. Audit Profil Risiko Zona",
])

# --- TAB 1: PARETO ---
with tab1:
  st.subheader("Distorsi Beban Pareto 3 Domain Teratas")
  st.write(
      "Dari lebih dari 1,11 juta nama domain terdaftar, distribusi kueri sangat"
      " timpang. **HANYA 3 domain** merampas 27,23% kapasitas server nasional"
      " akibat kegagalan *caching* aplikasi klien."
  )

  col_img, col_text = st.columns([2, 1], gap="large")
  with col_img:
    img_pareto = load_image("fig4_pareto_domains.png")
    if img_pareto:
      st.image(img_pareto, use_container_width=True)
    else:
      st.warning("Gambar grafik Pareto belum dibuat.")

  with col_text:
        st.info(
            "**🔍 Analisis Akar Masalah:**\n\n"
            "Ketiga domain teratas menyerap beban masif:\n"
            "• `smartconnect.id`: 981.583 kueri (16,75%)\n"
            "• `axarva.id`: 341.427 kueri (5,82%)\n"
            "• `speedtest.rndlabbankmandiri.co.id`: 273.346 kueri (4,66% pada host speedtest, atau 278.116 kueri total keluarga subdomain `*.rndlabbankmandiri.co.id`)\n\n"
            "**Akar Masalah:** Aplikasi klien mengabaikan batas TTL (Time-To-Live) dan melakukan *blind polling* tanpa caching lokal."
        )
        st.success(
            "**💡 Rekomendasi Solusi Bisnis (P1):**\n\n"
            "**Edukasi Pemilik Domain:** Tim Kemitraan PANDI menegur pemilik ketiga domain melalui registrar terkait untuk memperbaiki caching aplikasinya.\n\n"
            "**Target KPI:** Kueri berulang turun ≥85%, langsung menghemat **~27% kapasitas nasional (~800 QPS)** secara instan tanpa biaya perangkat keras (Zero Cost / Rp0,-)."
        )

# --- TAB 2: DNSSEC ---
with tab2:
  st.subheader("Amplifikasi Protokol DNSSEC & Kelelahan TCP")
  st.write(
      "Penambahan tanda tangan kriptografi (DNSSEC) membuat ukuran paket melonjak"
      " drastis, melampaui batas buffer UDP 1.232 Byte sehingga paket terpotong"
      " dan memaksa klien beralih ke TCP."
  )

  col_img, col_text = st.columns([2, 1], gap="large")
  with col_img:
    img_dnssec = load_image("fig2_dnssec_amplification_and_latency.png")
    if img_dnssec:
      st.image(img_dnssec, use_container_width=True)
    else:
      st.warning("Gambar grafik DNSSEC belum dibuat.")

  with col_text:
        st.info(
            "**🔍 Analisis Akar Masalah:**\n\n"
            "• **Adopsi Tinggi:** 87,58% kueri meminta DNSSEC (`do=1`).\n\n"
            "• **Amplifikasi Ukuran:** Payload membengkak dari median 44 Byte (kueri) menjadi median 446 Byte (hingga rekor 2.126 Byte) pada respons bertanda tangan.\n\n"
            "• **Pemotongan UDP:** 321.798 paket (5,50%) terpotong (`tc=1`) karena melebihi buffer 1.232 B (RFC 8900).\n\n"
            "• **Beban TCP 2,6x Lebih Lambat:** Memicu 510.391 koneksi TCP yang memakan memori kernel server Anycast dan 2,6x lebih lambat (277,4 µs vs 106,7 µs)."
        )
        st.success(
            "**💡 Rekomendasi Solusi Bisnis (P2):**\n\n"
            "**Tuning Kernel Anycast:** Naikkan parameter OS `tcp_max_syn_backlog` dari 1.024 ke 16.384/32.768 agar port 53 bebas dari risiko *socket exhaustion*.\n\n"
            "**Migrasi Kriptografi:** Evaluasi adopsi kurva eliptik ECDSA P-256 (RFC 8624) yang lebih ringkas agar respons muat di bawah 1.232 Byte."
        )

# --- TAB 3: NXDOMAIN ---
with tab3:
  st.subheader("Taksonomi NXDOMAIN (Membongkar Mitos DDoS)")
  st.write(
      "Sebanyak 675.229 paket dijawab gagal (NXDOMAIN / 11,54%). Mayoritas"
      " mutlak (>95%) merupakan sampah operasional internet (domain"
      " kedaluwarsa, salah ketik, autodiscover), dengan anomali lonjakan sesaat"
      " di menit ke-12 (15:02 WIB) akibat scanning/fuzzing yang bukan serangan"
      " DDoS PRSD masif."
  )

  col_img, col_text = st.columns([2, 1], gap="large")
  with col_img:
    img_nxdomain = load_image("fig3_nxdomain_root_cause_and_sld.png")
    if img_nxdomain:
      st.image(img_nxdomain, use_container_width=True)
    else:
      st.warning("Gambar grafik NXDOMAIN belum dibuat.")

  with col_text:
        st.info(
            "**🔍 Analisis Akar Masalah:**\n\n"
            "• **58,3% Volume Kueri:** Domain kedaluwarsa/mati yang masih terus dicari sistem luar (`tracker.itscraftsoftware.my.id`).\n\n"
            "• **35,7% Nama Domain Unik (23% Volume):** Variasi salah ketik pengguna sesaat (*human typos / singletons*).\n\n"
            "• **Enterprise & Stale NS:** Kueri otomatis Microsoft Office 365 (`msoid.co.id`) dan rujukan nameserver mati (`ns1.bna.net.id`).\n\n"
            "• **Anomali Menit 15:02 WIB:** Lonjakan tajam sesaat akibat scanning/fuzzing dari 2 IP penguji, bukan DDoS PRSD yang mengancam server."
        )
        st.success(
            "**💡 Rekomendasi Solusi Bisnis (P3 - Solusi Rp0,-):**\n\n"
            "**Negative Caching RFC 2308:** Naikkan parameter *SOA Minimum TTL* dari 300 detik (5 menit) ke 1.800 detik (30 menit).\n\n"
            "**Target KPI:** Resolver ISP menahan jawaban NXDOMAIN 6x lebih lama, meredam 25%–35% kueri sampah berulang ke PANDI secara cuma-cuma tanpa belanja hardware!"
        )

# --- TAB 4: TABEL RISIKO ---
with tab4:
  st.subheader("Audit Profil Risiko 14 Ekstensi Zona .id")
  st.write(
      "Gunakan tabel interaktif di bawah ini untuk melihat zona (ekstensi) mana"
      " yang paling rawan terhadap error (NXDOMAIN) dan pemotongan paket (UDP"
      " Truncated). Klik pada nama kolom untuk mengurutkan data."
  )

  data = [
      {
          "Zona .id": ".sch.id",
          "Query (qr=0)": 142070,
          "Response (qr=1)": 141664,
          "NXDOMAIN (Vol)": 35167,
          "% NXDOMAIN": 24.82,
          "% Truncated (tc=1)": 23.01,
          "Profil Risiko": "Truncation Tinggi",
      },
      {
          "Zona .id": ".web.id",
          "Query (qr=0)": 236725,
          "Response (qr=1)": 235629,
          "NXDOMAIN (Vol)": 71181,
          "% NXDOMAIN": 30.21,
          "% Truncated (tc=1)": 19.80,
          "Profil Risiko": "NXDOMAIN & Truncation",
      },
      {
          "Zona .id": ".biz.id",
          "Query (qr=0)": 145701,
          "Response (qr=1)": 145111,
          "NXDOMAIN (Vol)": 45964,
          "% NXDOMAIN": 31.68,
          "% Truncated (tc=1)": 17.84,
          "Profil Risiko": "NXDOMAIN Tinggi",
      },
      {
          "Zona .id": ".desa.id",
          "Query (qr=0)": 22079,
          "Response (qr=1)": 22060,
          "NXDOMAIN (Vol)": 1807,
          "% NXDOMAIN": 8.19,
          "% Truncated (tc=1)": 16.38,
          "Profil Risiko": "Truncation Tinggi",
      },
      {
          "Zona .id": ".co.id",
          "Query (qr=0)": 1715520,
          "Response (qr=1)": 1706772,
          "NXDOMAIN (Vol)": 220465,
          "% NXDOMAIN": 12.92,
          "% Truncated (tc=1)": 12.42,
          "Profil Risiko": "Volume Terbesar",
      },
      {
          "Zona .id": ".my.id",
          "Query (qr=0)": 380140,
          "Response (qr=1)": 380068,
          "NXDOMAIN (Vol)": 78070,
          "% NXDOMAIN": 20.54,
          "% Truncated (tc=1)": 0.07,
          "Profil Risiko": "Terkendali",
      },
      {
          "Zona .id": ".or.id",
          "Query (qr=0)": 60290,
          "Response (qr=1)": 60281,
          "NXDOMAIN (Vol)": 7552,
          "% NXDOMAIN": 12.53,
          "% Truncated (tc=1)": 0.06,
          "Profil Risiko": "Terkendali",
      },
      {
          "Zona .id": ".ac.id",
          "Query (qr=0)": 212167,
          "Response (qr=1)": 212152,
          "NXDOMAIN (Vol)": 24131,
          "% NXDOMAIN": 11.37,
          "% Truncated (tc=1)": 0.05,
          "Profil Risiko": "Terkendali",
      },
      {
          "Zona .id": ".id (Langsung)",
          "Query (qr=0)": 2462926,
          "Response (qr=1)": 2462832,
          "NXDOMAIN (Vol)": 154941,
          "% NXDOMAIN": 6.29,
          "% Truncated (tc=1)": 0.02,
          "Profil Risiko": "Sangat Sehat",
      },
      {
          "Zona .id": ".net.id",
          "Query (qr=0)": 256841,
          "Response (qr=1)": 256819,
          "NXDOMAIN (Vol)": 24642,
          "% NXDOMAIN": 9.60,
          "% Truncated (tc=1)": 0.01,
          "Profil Risiko": "Terkendali",
      },
      {
          "Zona .id": ".go.id",
          "Query (qr=0)": 218168,
          "Response (qr=1)": 218151,
          "NXDOMAIN (Vol)": 9006,
          "% NXDOMAIN": 4.13,
          "% Truncated (tc=1)": 0.00,
          "Profil Risiko": "Sangat Sehat",
      },
      {
          "Zona .id": ".mil.id",
          "Query (qr=0)": 3890,
          "Response (qr=1)": 3890,
          "NXDOMAIN (Vol)": 1025,
          "% NXDOMAIN": 26.35,
          "% Truncated (tc=1)": 0.00,
          "Profil Risiko": "NXDOMAIN Tinggi",
      },
      {
          "Zona .id": ".ponpes.id",
          "Query (qr=0)": 2989,
          "Response (qr=1)": 2989,
          "NXDOMAIN (Vol)": 1278,
          "% NXDOMAIN": 42.76,
          "% Truncated (tc=1)": 0.00,
          "Profil Risiko": "NXDOMAIN Kritis",
      },
  ]

  df = pd.DataFrame(data)

  st.dataframe(
      df,
      column_config={
          "Query (qr=0)": st.column_config.NumberColumn(format="%d"),
          "Response (qr=1)": st.column_config.NumberColumn(format="%d"),
          "NXDOMAIN (Vol)": st.column_config.NumberColumn(format="%d"),
          "% NXDOMAIN": st.column_config.ProgressColumn(
              format="%.2f%%", min_value=0, max_value=50
          ),
          "% Truncated (tc=1)": st.column_config.ProgressColumn(
              format="%.2f%%", min_value=0, max_value=25
          ),
      },
      use_container_width=True,
      hide_index=True,
  )
  st.caption(
      "*Tips: Klik pada header kolom (misalnya '% Truncated' atau '% NXDOMAIN')"
      " untuk mengurutkan zona dari yang paling rawan hingga terendah.*"
  )

import streamlit as st
import pandas as pd
from PIL import Image
import os

# Konfigurasi Halaman (Harus diletakkan paling atas)
st.set_page_config(
    page_title="Dashboard Analytics DNS .id",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Kustom untuk memperbaiki jarak dan tampilan
st.markdown("""
<style>
    .kpi-title { font-size: 14px !important; color: #64748b; margin-bottom: -10px; font-weight: 600;}
    .kpi-value { font-size: 32px !important; font-weight: 800; color: #0f172a; }
    .kpi-desc { font-size: 13px !important; color: #94a3b8; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; }
</style>
""", unsafe_allow_html=True)

# Helper function untuk load gambar dengan aman
def load_image(filename):
    path = os.path.join("dns_analytics_output", filename)
    if os.path.exists(path):
        return Image.open(path)
    return None

# ======================== HEADER ========================
st.title("📊 Dashboard Business Analytics DNS ccTLD .id")
st.caption("Pesta Data Nasional (PeDaS) 2026 — Dibuat untuk Evaluasi Kinerja & Kapasitas Infrastruktur PANDI")
st.markdown("*(Status: Blind Review Compliant)*")
st.divider()

# ======================== KPI GRID ========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Paket Dianalisis", value="11.712.623", delta="Dalam 30 Menit (2,4 GB)", delta_color="off")
with col2:
    st.metric(label="Latensi Internal PANDI", value="83,9 µs", delta="Sangat Responsif (< 0.1 ms)", delta_color="normal")
with col3:
    st.metric(label="Paket UDP Terpotong (tc=1)", value="321.798", delta="Memicu 510K+ Koneksi TCP", delta_color="inverse")
with col4:
    st.metric(label="Beban Kueri Pareto (3 Domain)", value="27,23%", delta="Efisiensi yang hilang", delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)

# ======================== TABS ========================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 1. Distorsi Pareto", 
    "🛡️ 2. Amplifikasi DNSSEC", 
    "🗑️ 3. Mitos NXDOMAIN", 
    "🗄️ 4. Audit Profil Risiko Zona"
])

# --- TAB 1: PARETO ---
with tab1:
    st.subheader("Distorsi Beban Pareto 3 Domain Teratas")
    st.write("Dari lebih dari 1 juta nama domain terdaftar, distribusi kueri sangat timpang. **HANYA 3 domain** merampas 27,23% kapasitas server nasional akibat kegagalan *caching* aplikasi klien.")
    
    col_img, col_text = st.columns([2, 1], gap="large")
    with col_img:
        img_pareto = load_image("fig4_pareto_domains.png")
        if img_pareto:
            st.image(img_pareto, use_column_width=True)
        else:
            st.warning("Gambar grafik Pareto belum dibuat di folder dns_analytics_output.")
            
    with col_text:
        st.info("**🔍 Analisis Akar Masalah:**\n\nKetiga domain ini (`smartconnect.id`, `axarva.id`, `rndlabbankmandiri.co.id`) secara konstan ditanyakan berulang kali oleh resolver ISP. Ini mengindikasikan aplikasi mereka mengabaikan batas TTL (Time-To-Live) dan melakukan *polling* buta.")
        st.success("**💡 Rekomendasi Solusi:**\n\n**Edukasi Pemilik Domain:** Tim Kemitraan PANDI harus menegur pemilik 3 domain tersebut untuk memperbaiki aplikasi mereka. Perbaikan pada 3 domain ini saja akan menghemat 27% biaya bandwidth nasional PANDI.")

# --- TAB 2: DNSSEC ---
with tab2:
    st.subheader("Amplifikasi Protokol DNSSEC & Kelelahan TCP")
    st.write("Penambahan tanda tangan kriptografi (DNSSEC) membuat ukuran paket melonjak drastis, menyebabkan paket terpotong dan memaksa klien menggunakan protokol TCP yang menguras memori server.")
    
    col_img, col_text = st.columns([2, 1], gap="large")
    with col_img:
        img_dnssec = load_image("fig2_dnssec_amplification_and_latency.png")
        if img_dnssec:
            st.image(img_dnssec, use_column_width=True)
        else:
            st.warning("Gambar grafik DNSSEC belum dibuat.")
            
    with col_text:
        st.info("**🔍 Analisis Akar Masalah:**\n\nAdopsi DNSSEC mencapai 87,6%. Akibatnya, balasan membengkak dari 44 Byte menjadi 446 Byte (hingga batas 2.126 Byte). Pembengkakan ini melampaui batas UDP 1232 Byte, memotong 321.798 paket dan memicu 510K+ sesi TCP.")
        st.success("**💡 Rekomendasi Solusi:**\n\n**Tuning Kernel Server:** Infrastruktur PANDI harus meningkatkan alokasi parameter `tcp_max_syn_backlog` pada OS server Anycast agar tidak terjadi kegagalan (hang) saat menghadapi gelombang pendaftaran koneksi TCP.")

# --- TAB 3: NXDOMAIN ---
with tab3:
    st.subheader("Taksonomi NXDOMAIN (Membongkar Mitos DDoS)")
    st.write("675.229 paket dijawab gagal (NXDOMAIN). Ini BUKAN serangan siber/DDoS PRSD, melainkan murni anomali salah ketik, *autodiscover* Microsoft, dan domain mati.")
    
    col_img, col_text = st.columns([2, 1], gap="large")
    with col_img:
        img_nxdomain = load_image("fig3_nxdomain_root_cause_and_sld.png")
        if img_nxdomain:
            st.image(img_nxdomain, use_column_width=True)
        else:
            st.warning("Gambar grafik NXDOMAIN belum dibuat.")
            
    with col_text:
        st.info("**🔍 Analisis Akar Masalah:**\n\n35,7% kueri gagal adalah salah ketik sementara (typos). Sisa terbesarnya adalah *autodiscover* Microsoft Exchange (`msoid.co.id`) yang agresif, dan *nameserver* mati (`ns1.bna.net.id`) yang masih terus dicari oleh ISP.")
        st.success("**💡 Rekomendasi Solusi:**\n\n**Negative Caching (Rp0,-):** Naikkan parameter *SOA Minimum TTL* dari 300 detik menjadi 1800 detik. ISP akan menyimpan memori 'Domain Tidak Ditemukan' lebih lama dan berhenti mengirim kueri sampah ke PANDI.")

# --- TAB 4: TABEL RISIKO ---
with tab4:
    st.subheader("Audit Profil Risiko 14 Ekstensi Zona .id")
    st.write("Gunakan tabel interaktif di bawah ini untuk melihat zona (ekstensi) mana yang paling rawan terhadap error (NXDOMAIN) dan pemotongan paket (UDP Truncated). Klik pada nama kolom untuk mengurutkan data.")
    
    # Data Tabel berdasarkan hasil ekstraksi Python sebelumnya
    data = [
        {"Zona .id": ".sch.id", "Query (qr=0)": 142070, "Response (qr=1)": 141664, "NXDOMAIN (Vol)": 35167, "% NXDOMAIN": 24.82, "% Truncated (tc=1)": 23.01, "Profil Risiko": "Truncation Tinggi"},
        {"Zona .id": ".web.id", "Query (qr=0)": 236725, "Response (qr=1)": 235629, "NXDOMAIN (Vol)": 71181, "% NXDOMAIN": 30.21, "% Truncated (tc=1)": 19.80, "Profil Risiko": "NXDOMAIN Tinggi"},
        {"Zona .id": ".biz.id", "Query (qr=0)": 145701, "Response (qr=1)": 145111, "NXDOMAIN (Vol)": 45964, "% NXDOMAIN": 31.68, "% Truncated (tc=1)": 17.84, "Profil Risiko": "NXDOMAIN Tinggi"},
        {"Zona .id": ".desa.id", "Query (qr=0)": 22079, "Response (qr=1)": 22060, "NXDOMAIN (Vol)": 1807, "% NXDOMAIN": 8.19, "% Truncated (tc=1)": 16.38, "Profil Risiko": "Truncation Tinggi"},
        {"Zona .id": ".co.id", "Query (qr=0)": 1715520, "Response (qr=1)": 1706772, "NXDOMAIN (Vol)": 220465, "% NXDOMAIN": 12.92, "% Truncated (tc=1)": 12.42, "Profil Risiko": "Truncation Tinggi"},
        {"Zona .id": ".my.id", "Query (qr=0)": 380140, "Response (qr=1)": 380068, "NXDOMAIN (Vol)": 78070, "% NXDOMAIN": 20.54, "% Truncated (tc=1)": 0.07, "Profil Risiko": "Terkendali"},
        {"Zona .id": ".or.id", "Query (qr=0)": 60290, "Response (qr=1)": 60281, "NXDOMAIN (Vol)": 7552, "% NXDOMAIN": 12.53, "% Truncated (tc=1)": 0.06, "Profil Risiko": "Terkendali"},
        {"Zona .id": ".ac.id", "Query (qr=0)": 212167, "Response (qr=1)": 212152, "NXDOMAIN (Vol)": 24131, "% NXDOMAIN": 11.37, "% Truncated (tc=1)": 0.05, "Profil Risiko": "Terkendali"},
        {"Zona .id": ".id (Langsung)", "Query (qr=0)": 2462926, "Response (qr=1)": 2462832, "NXDOMAIN (Vol)": 154941, "% NXDOMAIN": 6.29, "% Truncated (tc=1)": 0.02, "Profil Risiko": "Terkendali"},
        {"Zona .id": ".net.id", "Query (qr=0)": 256841, "Response (qr=1)": 256819, "NXDOMAIN (Vol)": 24642, "% NXDOMAIN": 9.60, "% Truncated (tc=1)": 0.01, "Profil Risiko": "Terkendali"},
        {"Zona .id": ".go.id", "Query (qr=0)": 218168, "Response (qr=1)": 218151, "NXDOMAIN (Vol)": 9006, "% NXDOMAIN": 4.13, "% Truncated (tc=1)": 0.00, "Profil Risiko": "Terkendali"},
        {"Zona .id": ".mil.id", "Query (qr=0)": 3890, "Response (qr=1)": 3890, "NXDOMAIN (Vol)": 1025, "% NXDOMAIN": 26.35, "% Truncated (tc=1)": 0.00, "Profil Risiko": "NXDOMAIN Tinggi"},
        {"Zona .id": ".ponpes.id", "Query (qr=0)": 2989, "Response (qr=1)": 2989, "NXDOMAIN (Vol)": 1278, "% NXDOMAIN": 42.76, "% Truncated (tc=1)": 0.00, "Profil Risiko": "NXDOMAIN Tinggi"},
    ]
    
    df = pd.DataFrame(data)
    
    # Menampilkan dataframe dengan style dan format di Streamlit
    st.dataframe(
        df,
        column_config={
            "Query (qr=0)": st.column_config.NumberColumn(format="%d"),
            "Response (qr=1)": st.column_config.NumberColumn(format="%d"),
            "NXDOMAIN (Vol)": st.column_config.NumberColumn(format="%d"),
            "% NXDOMAIN": st.column_config.ProgressColumn(format="%.2f%%", min_value=0, max_value=50),
            "% Truncated (tc=1)": st.column_config.ProgressColumn(format="%.2f%%", min_value=0, max_value=25)
        },
        use_container_width=True,
        hide_index=True
    )
    st.caption("*Tips: Klik pada nama kolom (misalnya '% Truncated' atau '% NXDOMAIN') untuk mengurutkan data dari yang paling tinggi ke terendah.*")

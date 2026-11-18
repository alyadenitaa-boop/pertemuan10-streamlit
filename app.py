
import pandas as pd
import streamlit as st
import plotly.express as px
import yfinance as yf
from datetime import date, timedelta

# Judul aplikasi
st.title("Pertemuan 10: Interaksi Streamlit dan Yahoo Finance")

# Kamus kode perusahaan
kamus_ticker = {
    "GOOGL": "Google",
    "AAPL": "Apple Inc",
    "SBUX": "Starbucks",
    "MCD": "McDonald's Corp",
    "META": "Meta Platforms Inc",
    "TLKM.JK": "Telkom Indonesia (Persero) Tbk PT",
    "BBNI.JK": "Bank Negara Indonesia (Persero) Tbk PT",
    "BMRI.JK": "Bank Mandiri (Persero) Tbk PT",
    "BBRI.JK": "Bank Rakyat Indonesia (Persero) Tbk PT",
    "NESN": "Nestle SA"
}

# Memilih kode perusahaan
ticker_symbol = st.selectbox(
    "Silahkan pilih kode perusahaan:",
    sorted(kamus_ticker.keys())
)

# Menampilkan nama perusahaan
st.write(kamus_ticker[ticker_symbol])

# Mengambil data saham dari Yahoo Finance
ticker_data = yf.Ticker(ticker_symbol)

# Memilih tanggal mulai
tgl_mulai = st.date_input(
    "Mulai tanggal",
    value=date.today() - timedelta(days=30)
)

# Memilih tanggal akhir
tgl_akhir = st.date_input(
    "Sampai tanggal",
    value=date.today()
)

# Menampilkan tanggal
st.write(f"Tanggal mulai: {tgl_mulai}")
st.write(f"Tanggal akhir: {tgl_akhir}")

# Memeriksa rentang tanggal
if tgl_mulai > tgl_akhir:
    st.error("Tanggal mulai tidak boleh melebihi tanggal akhir.")
    st.stop()

# Mengambil histori data saham
df_ticker = ticker_data.history(
    start=str(tgl_mulai),
    end=str(tgl_akhir + timedelta(days=1))
)

# Widget untuk menampilkan tabel
pilihan_tampil_tabel = st.checkbox("Tampilkan tabel")

if pilihan_tampil_tabel:
    st.write("## Lima Data Awal")
    st.write(df_ticker.head())

# Judul visualisasi
st.write(
    f"## Visualisasi Pergerakan Saham "
    f"{kamus_ticker[ticker_symbol]}"
)

# Memilih atribut saham
pilihan_atribut = st.multiselect(
    "Silahkan pilih atribut yang akan ditampilkan:",
    ["Low", "High", "Open", "Close", "Volume"]
)

# Membuat grafik
if not df_ticker.empty and pilihan_atribut:

    grafik = px.line(
        df_ticker,
        y=pilihan_atribut,
        title=f"Harga Saham {kamus_ticker[ticker_symbol]}"
    )

    st.plotly_chart(
        grafik,
        use_container_width=True
    )

elif df_ticker.empty:
    st.warning("Data saham tidak tersedia pada periode tersebut.")

else:
    st.info("Silahkan pilih atribut yang ingin ditampilkan.")

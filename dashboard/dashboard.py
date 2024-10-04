import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Pengaturan awal halaman
sns.set(style='dark')
st.set_page_config(page_title="Analisis Data Set Bike Sharing")

# Memuat data
df = pd.read_csv('data/day.csv')

# Sidebar untuk identitas
st.sidebar.title("Info")
st.sidebar.markdown("---")
st.sidebar.write("**Nama:** Dzaky Muhammad Zidane")
st.sidebar.write("**E-mail:** acelolik09@gmail.com")
st.sidebar.write("**ID Dicoding:** Dzaky Muhammad Zidane")
st.sidebar.markdown("---")

# Main header
st.title("Dashboard Analisis Data Set Bike Sharing")
st.markdown("---")

# Selectbox untuk memilih pertanyaan
visualization = st.selectbox("Pilih Analisis yang Ingin Ditampilkan:", 
                             ("Bagaimana pengaruh musim terhadap jumlah transaksi bike sharing?", 
                              "Bagaimana cuaca mempengaruhi jumlah pengguna, baik casual dan registered?", 
                              "Seberapa besar pengaruh temperatur terhadap jumlah total transaksi bike sharing?"))
st.markdown("---")

# Bagian 1: Analisis Musim
if visualization == "Bagaimana pengaruh musim terhadap jumlah transaksi bike sharing?":
    st.subheader("Bagaimana pengaruh musim terhadap jumlah transaksi bike sharing?")

    # Analisis berdasarkan musim
    season_year_cnt = df.groupby(['season', 'yr'])['cnt'].sum().unstack()
    season_year_cnt.plot(kind='line', figsize=(10, 6))

    plt.title('Jumlah Total Transaksi Bike Sharing per Musim (Tahun 2011 & 2012)')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah Total Transaksi')
    plt.xticks([1, 2, 3, 4], ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
    plt.legend(['2011', '2012'])
    st.pyplot(plt)

    st.caption("Berdasarkan data selama dua tahun tersebut, musim memiliki dampak terhadap jumlah transaksi. Tren yang terlihat pada tahun 2011 sejalan dengan tren di tahun 2012, di mana jumlah transaksi peminjaman tertinggi terjadi pada musim gugur, diikuti oleh musim panas, musim dingin, dan terakhir musim semi.")

# Bagian 2: Pengaruh Cuaca
elif visualization == "Bagaimana cuaca mempengaruhi jumlah pengguna, baik casual dan registered?":
    st.subheader("Bagaimana cuaca mempengaruhi jumlah pengguna, baik casual dan registered?")

    weather_labels = {
        1: 'Cerah',
        2: 'Berkabut',
        3: 'Salju Ringan/Hujan Ringan'
    }
    df['weather_label'] = df['weathersit'].map(weather_labels)

    avg_rentals = df.groupby('weather_label').agg({'casual': 'mean', 'registered': 'mean'}).reset_index()

    plt.figure(figsize=(12, 6))
    avg_rentals.set_index('weather_label').plot(kind='bar', stacked=False, color=['#66c2a5', '#fc8d62'])
    plt.title('Rata-rata Peminjaman Sepeda berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Rata-rata Peminjaman')
    plt.xticks(rotation=45)
    plt.legend(['Pengguna Biasa (Casual)', 'Pengguna Terdaftar (Registered)'])
    st.pyplot(plt)

    st.caption("Pengguna casual dan registered cenderung melakukan peminjaman sepeda ketika cuaca cerah atau berkabut, dengan peminjaman paling sedikit pada kondisi salju ringan atau hujan ringan.")

# Bagian 3: Pengaruh Temperatur
elif visualization == "Seberapa besar pengaruh temperatur terhadap jumlah total transaksi bike sharing?":
    st.subheader("Seberapa besar pengaruh temperatur terhadap jumlah total transaksi bike sharing?")

    df['temp_bin'] = pd.cut(df['temp'], bins=[0, 0.3, 0.6, 1], labels=['Rendah', 'Sedang', 'Tinggi'])
    temp_analysis = df.groupby('temp_bin', observed=True)['cnt'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(x='temp_bin', y='cnt', data=temp_analysis, palette='coolwarm')
    plt.title('Rata-rata total peminjaman berdasarkan kategori temperatur')
    plt.xlabel('Kategori Temperatur')
    plt.ylabel('Rata-rata Total Peminjaman')
    plt.tight_layout()
    st.pyplot(plt)

    st.caption("Transaksi peminjaman sepeda lebih banyak ketika temperatur tinggi, diikuti temperatur sedang, dan paling sedikit saat temperatur rendah.")

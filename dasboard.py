import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set konfigurasi halaman
st.set_page_config(layout="wide")
st.title('🚲 Welcome to ZooBike, Bike Share Dashboard')


# Pengenalan Dashboard
st.markdown("""
    ## 🌟Let's start exploring! 🚀
""")

# Memuat dataset
df = pd.read_csv('hour.csv')

# Sidebar untuk navigasi dan filter
st.sidebar.header('🗺️ Navigation and Filters')
page = st.sidebar.selectbox("Select Page", ["Rental Analysis"])

if page == "Rental Analysis":
    st.header('📊 Bike Rental Analysis')

    # Visualisasi Data
    st.header('Number of Rentals Based on Working Days')
    cnt_by_workingday = df.groupby('workingday')['cnt'].sum()

    # Visualisasi menggunakan bar chart
    st.bar_chart(cnt_by_workingday)
    st.caption('0: Hari Libur, 1: Hari Kerja')

    st.markdown("---")  # Add a horizontal line for separation

    # Penyewaan Berdasarkan Bulan
    st.header('Number of Rentals by Month')
    df['dteday'] = pd.to_datetime(df['dteday'])  # Konversi kolom 'dteday' menjadi datetime
    df['month'] = df['dteday'].dt.month
    monthly_cnt = df.groupby('month')['cnt'].sum()

    # Visualisasi menggunakan line chart
    st.line_chart(monthly_cnt)
    st.caption('1-12 menandakan bulan')

    st.markdown("---")  # Add a horizontal line for separation

    # Penyewaan Berdasarkan Cuaca
    st.header('Number of Rentals Based on Weather')

    # Mengelompokkan data berdasarkan 'weathersit' dan menghitung total jumlah penyewaan
    cnt_by_weathersit = df.groupby('weathersit')['cnt'].sum().reset_index()

    # Mengonversi 'weathersit' menjadi label deskriptif
    weather_labels = {1: 'Cerah', 2: 'Kabut', 3: 'Curah Hujan Ringan', 4: 'Curah Hujan Lebat'}
    cnt_by_weathersit['weather_label'] = cnt_by_weathersit['weathersit'].map(weather_labels)

    # Buat pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(cnt_by_weathersit['cnt'], labels=cnt_by_weathersit['weather_label'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    ax.set_title('Total Penyewaan Berdasarkan Cuaca', fontsize=14)

    # Tampilkan plot di Streamlit
    st.pyplot(fig)

    # Tambahkan interaksi: filter berdasarkan bulan
    st.sidebar.subheader('🔍 Filter by Month')
    selected_month = st.sidebar.selectbox("Select Month", range(1, 13), format_func=lambda x: f"Bulan {x}")
    
    filtered_data = df[df['month'] == selected_month]
    st.write(f"📅 Data Penyewaan untuk Bulan {selected_month}:")
    st.dataframe(filtered_data[['dteday', 'cnt', 'workingday', 'weathersit']])

if __name__ == "__main__":
    pass

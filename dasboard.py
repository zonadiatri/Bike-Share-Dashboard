import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.set_page_config(layout="wide")
st.title('Proyek Akhir Analisis Data Dhafindra')
st.text('Selamat datang di Dashboard laporan Proyek Akhir Analisis Data Dhafindra.')

st.header('Dataset')
df = pd.read_csv('data\hour.csv')
st.dataframe(data=df, width=900, height=300)
st.caption('Bike Sharing Dataset')

st.header('Pertanyaan Bisnis')
st.markdown('''
    1. Apakah jumlah sepeda yang disewa lebih banyak di hari libur atau di hari kerja?
    2. Pada Bulan apa sepeda paling banyak di sewa?
    ''')

tab1, tab2, tab3= st.tabs(["Data Wrangling", "Exploratory Data Analysis", "Visualization & Explanatory Analysis"])

with tab1:
    st.header('Data Wrangling')
    tab11, tab12, tab13 = st.tabs(['Gathering Data', 'Asessing Data', 'Cleaning Data'])
    with tab11:
        st.subheader('Gathering Data')
        df1 = pd.read_csv('data\day.csv')
        code1 = '''
                df1 = pd.read_csv('day.csv')
                df1.describe()
                '''
        st.code(code1, language='python')
        st.dataframe(data=df1, width=900, height=300)

        df2 = df
        code2 = '''
                df2 = pd.read_csv('data\hour.csv')
                df2.describe()
                '''
        st.code(code2, language='python')
        st.dataframe(data=df2,width=900,height=300)

        st.text("Dataset hour.csv dipakai karena dataset tersebut lebih lengkap")
    with tab12:
        st.subheader('Assessing Data')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.code('df.info', language='python')
            buffer = io.StringIO()
            df.info(buf=buffer)
            info_output = buffer.getvalue()
            st.text(info_output)   

        with col2:
            st.code('df.isnull().sum()', language='python')
            st.dataframe(df.isnull().sum(),width=900,height=300)

        with col3:
            code3 = '''
            duplicates = {}

            for column in df.columns:
                duplicates[column] = df.duplicated(subset=[column]).sum()

            # Menampilkan jumlah data duplikat dari setiap kolom
            for column, n_duplicates in duplicates.items(): 
                print(f'{column} : {n_duplicates} data duplikat')
            '''
            st.code(code3, language='python')
            duplicates = {}

            for column in df.columns:
                duplicates[column] = df.duplicated(subset=[column]).sum()

            # Menampilkan jumlah data duplikat dari setiap kolom
            for column, n_duplicates in duplicates.items(): 
                st.markdown(f'{column} : {n_duplicates} data duplikat')

        with col4: 
            code4='''
                # Mencari outlier
                    # Mencari outlier
                    outliers = {}
                    for column in df.columns:
                        if df[column].dtype.kind in 'biufc':  # Cek apakah kolom numerik
                            Q1 = df[column].quantile(0.25)  # Q1
                            Q3 = df[column].quantile(0.75)  # Q3
                            IQR = Q3 - Q1  # IQR
                            # Mendefinisikan range untuk nilai-nilai non-pencilan
                            non_outlier_range = (df[column] >= Q1 - 1.5*IQR) & (df[column] <= Q3 + 1.5*IQR)
                            # Hitung jumlah pencilan dan tambahkan ke dictionary
                            outliers[column] = len(df[column]) - non_outlier_range.sum()

                    for column, n_outliers in outliers.items():
                        print(f'{column}: {n_outliers} data pencilan')
            '''

            st.code(code4,language='python')
            # Mencari outlier
            outliers = {}
            for column in df.columns:
                if df[column].dtype.kind in 'biufc':  # Cek apakah kolom numerik
                    Q1 = df[column].quantile(0.25)  # Q1
                    Q3 = df[column].quantile(0.75)  # Q3
                    IQR = Q3 - Q1  # IQR
                    # Mendefinisikan range untuk nilai-nilai non-pencilan
                    non_outlier_range = (df[column] >= Q1 - 1.5*IQR) & (df[column] <= Q3 + 1.5*IQR)
                    # Hitung jumlah pencilan dan tambahkan ke dictionary
                    outliers[column] = len(df[column]) - non_outlier_range.sum()

            for column, n_outliers in outliers.items():
                print(f'{column}: {n_outliers} data pencilan')

        # Memilih kolom yang numerik saja
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns

        # Hitung korelasi kolom-kolom tersebut
        corr = df[numeric_columns].corr()
        
        st.subheader('Korelasi data sebelum dibersihkan')
        # Buat Heatmap korelasi tersebut
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Heatmap')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    with tab13:
        st.subheader('Cleaning Data')
        col1, col2, col3 = st.columns(3)
        with col1:
            code5 = '''
                # Menghilangkan beberapa fitur yang tidak terpakai
                dropkolom = ['instant', 'atemp','hr','holiday','weekday']
                df = df.drop(dropkolom, axis=1)
                '''
            st.code(code5, language='python')
            st.markdown('ini dilakukan untuk menghilangkan beberapa kolom yang tidak digunakan untuk analisis')

        with col2:
            code5 = '''
                # Konversi dteday menjadi datetime
                # Ini dilakukan karena kita hanya akan melihat 
                # banyak sewaan berdasarkan bulan
                df['dteday'] = pd.to_datetime(df['dteday'])

                #Ambil bulan dari 'dteday'
                df['month'] = df['dteday'].dt.month
                '''
            st.code(code5, language='python')
            st.markdown('konversi ke bulan saja karena kita hanya melihat banyak sewaan berdasarkan bulan')

        with col3:
            code6 = '''
            # hilangkan outlier yang sebelumnya sudah ditemukan
            for column in df.columns:
                if df[column].dtype.kind in 'biufc':  # Cek apakah kolom yang diperiksa numerik
                    Q1 = df[column].quantile(0.25)  # Q1
                    Q3 = df[column].quantile(0.75)  # Q3
                    IQR = Q3 - Q1  # Interquartile range (IQR)
                    # Mendefinisikan range untuk nilai-nilai non-pencilan
                    non_outlier_range = (df[column] >= Q1 - 1.5*IQR) & (df[column] <= Q3 + 1.5*IQR)
                    # RHilangkan pencilan
                    df = df[non_outlier_range]
            '''
            st.code(code6, language='python')
            st.markdown('ini dilakukan untuk menghilangkan outlier dari dataset yang digunakan')


with tab2:
    st.header('Exploratory Data Analysis')
    tab21, tab22, tab23= st.tabs(["Korelasi Data", "Jumlah Penyewaan Berdasarkan Tipe Hari", "Jumlah Penyewaan Berdasarkan Bulan"])

    with tab21:
        st.subheader('Korelasi data setelah dibersihkan')
        # Menghilangkan beberapa fitur yang tidak terpakai
        dropkolom = ['instant', 'atemp','hr','holiday','weekday']
        df = df.drop(dropkolom, axis=1)

        # Konversi dteday menjadi datetime
        # Ini dilakukan karena kita hanya akan melihat banyak sewaan berdasarkan bulan
        df['dteday'] = pd.to_datetime(df['dteday'])

        # hilangkan outlier yang sebelumnya sudah ditemukan
        for column in df.columns:
            if df[column].dtype.kind in 'biufc':  # Cek apakah kolom yang diperiksa numerik
                Q1 = df[column].quantile(0.25)  # Q1
                Q3 = df[column].quantile(0.75)  # Q3
                IQR = Q3 - Q1  # Interquartile range (IQR)
                # Mendefinisikan range untuk nilai-nilai non-pencilan
                non_outlier_range = (df[column] >= Q1 - 1.5*IQR) & (df[column] <= Q3 + 1.5*IQR)
                # RHilangkan pencilan
                df = df[non_outlier_range]

        #Ambil bulan dari 'dteday'
        df['month'] = df['dteday'].dt.month
        # Memilih kolom yang numerik saja
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns

        # Hitung korelasi kolom-kolom tersebut
        corr = df[numeric_columns].corr()
        
        # Buat Heatmap korelasi tersebut
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Heatmap')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    with tab22:
        # Kelompokkan data berdasarkan 'workingday' dan hitung jumlah 'cnt' dari setiap kelompok
        cnt_by_workingday = df.groupby('workingday')['cnt'].sum()

        st.write(cnt_by_workingday)
        st.caption('''
                   0 : hari libur \n
                   1 : hari kerja
                   ''')

    with tab23:
        # Konversi dteday menjadi datetime
        # Ini dilakukan karena kita hanya akan melihat banyak sewaan berdasarkan bulan
        df['dteday'] = pd.to_datetime(df['dteday'])

        #Ambil bulan dari 'dteday'
        df['month'] = df['dteday'].dt.month

        # Melihat jumlah total sewaan di setiap bulan
        monthly_cnt = df.groupby('month')['cnt'].sum()
        st.write(monthly_cnt)
        st.caption('''
                   1-12 menandakan bulan
                   ''')




with tab3:
    st.header('Visualization & Explanatory Analysis')
    st.subheader('Pertanyaan 1')
    # Mengelompokkan data berdasarkan 'workingday' hitung total dari 'cnt'
    cnt_by_workingday = df.groupby('workingday')['cnt'].sum()

    st.text('Jumlah Penyewaan Berdasarkan Hari Kerja')
    st.bar_chart(cnt_by_workingday)
    st.caption('0 : hari libur \n 1 : hari kerja')

    st.subheader('Pertanyaan 2')
    # Konversi dteday menjadi datetime
    df['dteday'] = pd.to_datetime(df['dteday'])

    # Ambil bulan dari 'dteday'
    df['month'] = df['dteday'].dt.month

    monthly_cnt = df.groupby('month')['cnt'].sum()

    st.text('Jumlah Total Berdasarkan Bulan')
    st.line_chart(monthly_cnt)
    st.caption('1-12 menandakan bulan')


st.header('Conclusion')
st.markdown('''
            - Conclusion Pertanyaan 1:
                sepeda jauh lebih banyak disewa pada hari kerja dibandingkan hari libur.

            - Conclusion Pertanyaan 2:
                penyewaan sepeda paling banyak terjadi di bulan ke-7 atau bulan Juli.
            ''')
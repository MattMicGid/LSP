import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Membaca dataset
df = pd.read_csv('bestsellers_with_categories.csv')

# Judul aplikasi
st.title("Aplikasi Rekomendasi Buku")

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman:", ["Daftar Buku", "Rekomendasi Buku", "Visualisasi"])

# Halaman Daftar Buku
if page == "Daftar Buku":
    st.subheader("Daftar Buku")
    st.dataframe(df, hide_index=True)  # Menampilkan DataFrame tanpa kolom indeks

# Halaman Rekomendasi Buku
elif page == "Rekomendasi Buku":
    st.subheader("Rekomendasi Buku")
    
    # Pilihan untuk rekomendasi berdasarkan genre atau rating
    rekomendasi_tipe = st.selectbox("Pilih Tipe Rekomendasi:", ["Genre", "Rating"])

    # Jika pengguna memilih berdasarkan genre
    if rekomendasi_tipe == "Genre":
        genre_filter = st.selectbox("Pilih Genre:", df['Genre'].unique())
        filtered_books = df[df['Genre'] == genre_filter]
        
        if not filtered_books.empty:
            top_books_genre = filtered_books.nlargest(5, 'User Rating')
            st.subheader(f"Buku Terbaik dalam Genre: {genre_filter}")
            st.dataframe(top_books_genre, hide_index=True)  # Menampilkan rekomendasi tanpa kolom indeks

            # Menampilkan informasi detail tentang buku yang dipilih
            selected_book = st.selectbox("Pilih Buku untuk Detail:", top_books_genre['Name'])
            book_details = top_books_genre[top_books_genre['Name'] == selected_book]

            if not book_details.empty:
                st.subheader("Detail Buku")
                st.write("Pengarang:", book_details['Author'].values[0])
                st.write("Rating Pengguna:", book_details['User Rating'].values[0])
                st.write("Jumlah Penilaian:", book_details['Reviews'].values[0])
                st.write("Harga:", book_details['Price'].values[0])
                st.write("Tahun Publikasi:", book_details['Year'].values[0])
        else:
            st.write("Tidak ada buku dalam genre ini.")

    # Jika pengguna memilih berdasarkan rating
    elif rekomendasi_tipe == "Rating":
        top_books = df.nlargest(5, 'User Rating')
        st.subheader("Rekomendasi Buku Terbaik Berdasarkan Rating")
        st.dataframe(top_books, hide_index=True)  # Menampilkan rekomendasi tanpa kolom indeks

        # Menampilkan informasi detail tentang buku yang dipilih
        selected_book = st.selectbox("Pilih Buku untuk Detail:", top_books['Name'])
        book_details = top_books[top_books['Name'] == selected_book]

        if not book_details.empty:
            st.subheader("Detail Buku")
            st.write("Pengarang:", book_details['Author'].values[0])
            st.write("Rating Pengguna:", book_details['User Rating'].values[0])
            st.write("Jumlah Penilaian:", book_details['Reviews'].values[0])
            st.write("Harga:", book_details['Price'].values[0])
            st.write("Tahun Publikasi:", book_details['Year'].values[0])

# Halaman Visualisasi
elif page == "Visualisasi":
    st.subheader("Visualisasi Data Buku")

    # Subheader dan plot untuk rata-rata harga buku per tahun
    st.subheader("Rata-rata Harga Buku per Tahun")
    # Menghitung harga rata-rata per tahun
    avg_price_by_year = df.groupby('Year')['Price'].mean().reset_index()

    # Set the Seaborn style and color palette
    sns.set(style="whitegrid")

    # Create a figure for the average price plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='Year', y='Price', data=avg_price_by_year, marker='o', linewidth=2.5, ax=ax, color='royalblue')
    ax.set_title('Rata-rata Harga Buku per Tahun', fontsize=16, fontweight='bold')
    ax.set_xlabel('Tahun', fontsize=12)
    ax.set_ylabel('Harga Rata-rata ($)', fontsize=12)
    ax.set_ylim(1, 20)
    ax.set_xticks(avg_price_by_year['Year'])
    ax.tick_params(axis='x', rotation=45)
    ax.set_yticks(np.arange(0, 21, 1))
    ax.grid(True, which='both', linestyle='--', linewidth=0.7, alpha=0.7)

    # Show the plot in Streamlit
    st.pyplot(fig)  # Pass the figure to st.pyplot()

    # Subheader dan plot untuk perbandingan jumlah ulasan
    st.subheader("Perbandingan Jumlah Ulasan Berdasarkan Genre per Tahun")
    # Menghitung total ulasan per tahun dan genre
    genre_per_year = df.groupby(['Year', 'Genre'])['Reviews'].sum().reset_index()

    # Create a figure for the review comparison plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Year', y='Reviews', hue='Genre', data=genre_per_year, palette="muted", ax=ax)
    ax.set_title('Perbandingan Jumlah Ulasan Antara Genre per Tahun', fontsize=16, fontweight='bold')
    ax.set_xlabel('Tahun', fontsize=12)
    ax.set_ylabel('Total Ulasan', fontsize=12)
    ax.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')  # Adjust legend position

    # Show the plot in Streamlit
    st.pyplot(fig)  # Pass the figure to st.pyplot()
    
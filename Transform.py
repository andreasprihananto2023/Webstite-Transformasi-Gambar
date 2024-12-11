import streamlit as st
import cv2
import numpy as np
import math

st.title("Aplikasi Transformasi Gambar Interaktif")

# Unggah file gambar
unggah_file = st.file_uploader("Unggah gambar dalam format JPEG atau PNG", type=["jpg", "jpeg", "png"])

if unggah_file is not None:
    # Membaca gambar
    file_bytes = np.asarray(bytearray(unggah_file.read()), dtype=np.uint8)
    gambar = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    tinggi, lebar = gambar.shape[:2]

    # Menampilkan gambar asli
    st.image(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB), caption="Gambar Asli", use_container_width=True)

    # Slider untuk transformasi
    dx = st.slider("Translasi X (px)", -200, 200, 0)
    dy = st.slider("Translasi Y (px)", -200, 200, 0)
    sudut = st.slider("Sudut Rotasi (derajat)", -180, 180, 0)
    scale = st.slider("Faktor Skala", 0.5, 2.0, 1.0)
    skew_x = st.slider("Distorsi X", 0.0, 2.0, 0.0)
    skew_y = st.slider("Distorsi Y", 0.0, 2.0, 0.0)

    # Membuat matriks transformasi gabungan
    angle_rad = math.radians(sudut)
    matriks_translasi = np.array([[1, 0, dx],
                                  [0, 1, dy],
                                  [0, 0, 1]])
    matriks_rotasi = np.array([[math.cos(angle_rad), -math.sin(angle_rad), 0],
                               [math.sin(angle_rad), math.cos(angle_rad), 0],
                               [0, 0, 1]])
    matriks_skala = np.array([[scale, 0, 0],
                              [0, scale, 0],
                              [0, 0, 1]])
    matriks_distorsi = np.array([[1, skew_x, 0],
                                  [skew_y, 1, 0],
                                  [0, 0, 1]])

    # Kombinasi matriks
    matriks_transformasi = matriks_translasi @ matriks_rotasi @ matriks_skala @ matriks_distorsi

    # Transformasi gambar
    def transformasi_gambar(matriks, tinggi, lebar):
        hasil = np.zeros_like(gambar)
        for y in range(tinggi):
            for x in range(lebar):
                koordinat_asli = np.array([x, y, 1])
                koordinat_baru = matriks @ koordinat_asli
                x_baru, y_baru = int(koordinat_baru[0]), int(koordinat_baru[1])
                if 0 <= x_baru < lebar and 0 <= y_baru < tinggi:
                    hasil[y_baru, x_baru] = gambar[y, x]
        return hasil

    # Gambar setelah transformasi gabungan
    gambar_akhir = transformasi_gambar(matriks_transformasi, tinggi, lebar)

    # Menampilkan hasil transformasi
    st.image(cv2.cvtColor(gambar_akhir, cv2.COLOR_BGR2RGB), caption="Hasil Transformasi", use_container_width=True)

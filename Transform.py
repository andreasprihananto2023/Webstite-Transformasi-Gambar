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
    st.image(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB), caption="Gambar Asli", use_container_width=True)

    # Slider untuk translasi
    dx = st.slider("Translasi X (px)", -200, 200, 0)
    dy = st.slider("Translasi Y (px)", -200, 200, 0)
    matriks_translasi = np.array([[1, 0, dx],
                                  [0, 1, dy],
                                  [0, 0, 1]])

    # Slider untuk rotasi
    sudut = st.slider("Sudut Rotasi (derajat)", -180, 180, 0)
    angle_rad = math.radians(sudut)
    matriks_rotasi = np.array([[math.cos(angle_rad), -math.sin(angle_rad), 0],
                               [math.sin(angle_rad), math.cos(angle_rad), 0],
                               [0, 0, 1]])

    # Slider untuk skala
    scale = st.slider("Faktor Skala", 0.5, 2.0, 1.0)
    matriks_skala = np.array([[scale, 0, 0],
                              [0, scale, 0],
                              [0, 0, 1]])

    # Slider untuk distorsi
    skew_x = st.slider("Distorsi X", 0.0, 2.0, 0.0)
    skew_y = st.slider("Distorsi Y", 0.0, 2.0, 0.0)
    matriks_distorsi = np.array([[1, skew_x, 0],
                                  [skew_y, 1, 0],
                                  [0, 0, 1]])

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

    # Gambar setelah transformasi
    gambar_translasi = transformasi_gambar(matriks_translasi, tinggi, lebar)
    gambar_rotasi = transformasi_gambar(matriks_rotasi, tinggi, lebar)
    gambar_skala = transformasi_gambar(matriks_skala, int(tinggi * scale), int(lebar * scale))
    gambar_distorsi = transformasi_gambar(matriks_distorsi, tinggi, lebar)

    # Menampilkan hasil transformasi
    st.image(cv2.cvtColor(gambar_translasi, cv2.COLOR_BGR2RGB), caption="Gambar Translasi", use_container_width=True)
    st.image(cv2.cvtColor(gambar_rotasi, cv2.COLOR_BGR2RGB), caption="Gambar Rotasi", use_container_width=True)
    st.image(cv2.cvtColor(gambar_skala, cv2.COLOR_BGR2RGB), caption="Gambar Skala", use_container_width=True)
    st.image(cv2.cvtColor(gambar_distorsi, cv2.COLOR_BGR2RGB), caption="Gambar Distorsi", use_container_width=True)

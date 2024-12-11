import streamlit as st
import cv2
import numpy as np
import math

st.title("Aplikasi Transformasi Gambar")

# Unggah file
unggah_file = st.file_uploader("Unggah gambar dalam format JPEG atau PNG", type=["jpg", "jpeg", "png"])

if unggah_file is not None:
    # Membaca gambar
    file_bytes = np.asarray(bytearray(unggah_file.read()), dtype=np.uint8)
    gambar = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    tinggi, lebar = gambar.shape[:2]
    st.image(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB), caption="Gambar Asli", use_container_width=True)

    # 1. Translasi
    st.subheader("Translasi")
    dx = st.slider("Translasi Horizontal (dx)", -200, 200, 50)
    dy = st.slider("Translasi Vertikal (dy)", -200, 200, 30)

    matriks_translasi = np.array([[1, 0, dx],
                                  [0, 1, dy],
                                  [0, 0, 1]])
    gambar_translasi = np.zeros_like(gambar)
    for y in range(tinggi):
        for x in range(lebar):
            koordinat_asli = np.array([x, y, 1])
            koordinat_baru = matriks_translasi @ koordinat_asli
            x_baru, y_baru = int(koordinat_baru[0]), int(koordinat_baru[1])
            if 0 <= x_baru < lebar and 0 <= y_baru < tinggi:
                gambar_translasi[y_baru, x_baru] = gambar[y, x]
    st.image(cv2.cvtColor(gambar_translasi, cv2.COLOR_BGR2RGB), caption="Gambar Translasi", use_container_width=True)

    # 2. Rotasi
    st.subheader("Rotasi")
    sudut = st.slider("Sudut Rotasi (derajat)", -180, 180, 45)
    radian = math.radians(sudut)
    matriks_rotasi = np.array([[math.cos(radian), -math.sin(radian), 0],
                               [math.sin(radian), math.cos(radian), 0],
                               [0, 0, 1]])
    tengah_x, tengah_y = lebar // 2, tinggi // 2
    gambar_rotasi = np.zeros_like(gambar)
    for y in range(tinggi):
        for x in range(lebar):
            koordinat_relative = np.array([x - tengah_x, y - tengah_y, 1])
            koordinat_baru = matriks_rotasi @ koordinat_relative
            x_baru, y_baru = int(koordinat_baru[0] + tengah_x), int(koordinat_baru[1] + tengah_y)
            if 0 <= x_baru < lebar and 0 <= y_baru < tinggi:
                gambar_rotasi[y_baru, x_baru] = gambar[y, x]
    st.image(cv2.cvtColor(gambar_rotasi, cv2.COLOR_BGR2RGB), caption="Gambar Rotasi", use_container_width=True)

    # 3. Skala
    st.subheader("Skala")
    skala_x = st.slider("Skala Horizontal", 0.5, 3.0, 1.5)
    skala_y = st.slider("Skala Vertikal", 0.5, 3.0, 1.5)

    matriks_skala = np.array([[skala_x, 0, 0],
                              [0, skala_y, 0],
                              [0, 0, 1]])
    tinggi_skala, lebar_skala = int(tinggi * skala_y), int(lebar * skala_x)
    gambar_skala = np.zeros((tinggi_skala, lebar_skala, 3), dtype=gambar.dtype)
    for y in range(tinggi):
        for x in range(lebar):
            koordinat_asli = np.array([x, y, 1])
            koordinat_baru = matriks_skala @ koordinat_asli
            x_baru, y_baru = int(koordinat_baru[0]), int(koordinat_baru[1])
            if 0 <= x_baru < lebar_skala and 0 <= y_baru < tinggi_skala:
                gambar_skala[y_baru, x_baru] = gambar[y, x]
    st.image(cv2.cvtColor(gambar_skala, cv2.COLOR_BGR2RGB), caption="Gambar Skala", use_container_width=True)

    # 4. Distorsi (Skewing)
    st.subheader("Distorsi")
    skew_x = st.slider("Distorsi Horizontal", 0.0, 2.0, 1.5)
    skew_y = st.slider("Distorsi Vertikal", 0.0, 2.0, 0.5)

    matriks_distorsi = np.array([[1, skew_x, 0],
                                 [skew_y, 1, 0],
                                 [0, 0, 1]])
    tinggi_distorsi, lebar_distorsi = int(tinggi * 2), int(lebar * 2)
    gambar_distorsi = np.zeros((tinggi_distorsi, lebar_distorsi, 3), dtype=gambar.dtype)
    for y in range(tinggi):
        for x in range(lebar):
            koordinat_asli = np.array([x, y, 1])
            koordinat_baru = matriks_distorsi @ koordinat_asli
            x_baru, y_baru = int(koordinat_baru[0]), int(koordinat_baru[1])
            if 0 <= x_baru < lebar_distorsi and 0 <= y_baru < tinggi_distorsi:
                gambar_distorsi[y_baru, x_baru] = gambar[y, x]
    st.image(cv2.cvtColor(gambar_distorsi, cv2.COLOR_BGR2RGB), caption="Gambar Distorsi", use_container_width=True)

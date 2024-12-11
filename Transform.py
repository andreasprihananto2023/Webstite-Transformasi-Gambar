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

    # Gunakan fungsi warpAffine untuk translasi
    matriks_translasi = np.float32([[1, 0, dx], [0, 1, dy]])
    gambar_translasi = cv2.warpAffine(gambar, matriks_translasi, (lebar, tinggi))
    st.image(cv2.cvtColor(gambar_translasi, cv2.COLOR_BGR2RGB), caption="Gambar Translasi", use_container_width=True)

    # 2. Rotasi
    st.subheader("Rotasi")
    sudut = st.slider("Sudut Rotasi (derajat)", -180, 180, 45)
    
    # Gunakan getRotationMatrix2D untuk rotasi yang lebih presisi
    tengah = (lebar // 2, tinggi // 2)
    matriks_rotasi = cv2.getRotationMatrix2D(tengah, sudut, 1.0)
    gambar_rotasi = cv2.warpAffine(gambar, matriks_rotasi, (lebar, tinggi))
    st.image(cv2.cvtColor(gambar_rotasi, cv2.COLOR_BGR2RGB), caption="Gambar Rotasi", use_container_width=True)

    # 3. Skala
    st.subheader("Skala")
    skala_x = st.slider("Skala Horizontal", 0.5, 3.0, 1.5)
    skala_y = st.slider("Skala Vertikal", 0.5, 3.0, 1.5)

    # Gunakan resize untuk scaling dengan interpolasi
    gambar_skala = cv2.resize(gambar, None, fx=skala_x, fy=skala_y, interpolation=cv2.INTER_LINEAR)
    st.image(cv2.cvtColor(gambar_skala, cv2.COLOR_BGR2RGB), caption="Gambar Skala", use_container_width=True)

    # 4. Distorsi (Skewing)
    st.subheader("Distorsi")
    skew_x = st.slider("Distorsi Horizontal", 0.0, 2.0, 1.5)
    skew_y = st.slider("Distorsi Vertikal", 0.0, 2.0, 0.5)

    # Gunakan perspectiveTransform untuk skewing
    pts1 = np.float32([[0,0], [lebar-1,0], [0,tinggi-1], [lebar-1,tinggi-1]])
    pts2 = np.float32([[0,0], 
                       [lebar-1,0], 
                       [skew_x*lebar,tinggi-1], 
                       [(1+skew_y)*lebar-1,tinggi-1]])

    matriks_distorsi = cv2.getPerspectiveTransform(pts1, pts2)
    gambar_distorsi = cv2.warpPerspective(gambar, matriks_distorsi, (lebar, tinggi))
    st.image(cv2.cvtColor(gambar_distorsi, cv2.COLOR_BGR2RGB), caption="Gambar Distorsi", use_container_width=True)

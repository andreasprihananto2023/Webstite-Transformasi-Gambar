import streamlit as st
import cv2
import numpy as np
import math

# Fungsi untuk mengompres gambar
@st.cache_data
def compress_image(image, max_size=(800, 800)):
    """Mengompres gambar dengan menjaga rasio aspek"""
    h, w = image.shape[:2]
    ratio = min(max_size[0]/w, max_size[1]/h)
    new_size = (int(w*ratio), int(h*ratio))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)

# Fungsi transformasi dengan caching
@st.cache_data
def transform_image(image, transform_type, **kwargs):
    """Fungsi transformasi gambar dengan caching"""
    if transform_type == 'translasi':
        dx, dy = kwargs.get('dx', 0), kwargs.get('dy', 0)
        matriks_translasi = np.float32([[1, 0, dx], [0, 1, dy]])
        return cv2.warpAffine(image, matriks_translasi, (image.shape[1], image.shape[0]))
    
    elif transform_type == 'rotasi':
        sudut = kwargs.get('sudut', 0)
        tengah = (image.shape[1] // 2, image.shape[0] // 2)
        matriks_rotasi = cv2.getRotationMatrix2D(tengah, sudut, 1.0)
        return cv2.warpAffine(image, matriks_rotasi, (image.shape[1], image.shape[0]))
    
    elif transform_type == 'skala':
        skala_x, skala_y = kwargs.get('skala_x', 1.0), kwargs.get('skala_y', 1.0)
        return cv2.resize(image, None, fx=skala_x, fy=skala_y, interpolation=cv2.INTER_LINEAR)
    
    elif transform_type == 'distorsi':
        h, w = image.shape[:2]
        skew_x, skew_y = kwargs.get('skew_x', 0), kwargs.get('skew_y', 0)
        pts1 = np.float32([[0,0], [w-1,0], [0,h-1], [w-1,h-1]])
        pts2 = np.float32([[0,0], 
                           [w-1,0], 
                           [skew_x*w,h-1], 
                           [(1+skew_y)*w-1,h-1]])
        matriks_distorsi = cv2.getPerspectiveTransform(pts1, pts2)
        return cv2.warpPerspective(image, matriks_distorsi, (w, h))

def main():
    st.title("Aplikasi Transformasi Gambar Cepat")

    # Sidebar untuk pengaturan
    with st.sidebar:
        st.header("Pilih Jenis Transformasi")
        transform_type = st.radio(
            "Transformasi",
            ['Translasi', 'Rotasi', 'Skala', 'Distorsi']
        )

    # Unggah file
    unggah_file = st.file_uploader(
        "Unggah gambar dalam format JPEG atau PNG", 
        type=["jpg", "jpeg", "png"]
    )

    if unggah_file is not None:
        # Baca dan kompres gambar
        file_bytes = np.asarray(bytearray(unggah_file.read()), dtype=np.uint8)
        gambar_asli = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        gambar_asli = compress_image(gambar_asli)

        # Tampilkan gambar asli
        col1, col2 = st.columns(2)
        with col1:
            st.image(cv2.cvtColor(gambar_asli, cv2.COLOR_BGR2RGB), 
                     caption="Gambar Asli", 
                     use_container_width=True)

        # Transformasi dinamis berdasarkan pilihan
        with col2:
            if transform_type == 'Translasi':
                dx = st.slider("Translasi Horizontal (dx)", -200, 200, 50)
                dy = st.slider("Translasi Vertikal (dy)", -200, 200, 30)
                gambar_transformasi = transform_image(
                    gambar_asli, 
                    'translasi', 
                    dx=dx, 
                    dy=dy
                )

            elif transform_type == 'Rotasi':
                sudut = st.slider("Sudut Rotasi (derajat)", -180, 180, 45)
                gambar_transformasi = transform_image(
                    gambar_asli, 
                    'rotasi', 
                    sudut=sudut
                )

            elif transform_type == 'Skala':
                skala_x = st.slider("Skala Horizontal", 0.5, 3.0, 1.5)
                skala_y = st.slider("Skala Vertikal", 0.5, 3.0, 1.5)
                gambar_transformasi = transform_image(
                    gambar_asli, 
                    'skala', 
                    skala_x=skala_x, 
                    skala_y=skala_y
                )

            elif transform_type == 'Distorsi':
                skew_x = st.slider("Distorsi Horizontal", 0.0, 2.0, 1.5)
                skew_y = st.slider("Distorsi Vertikal", 0.0, 2.0, 0.5)
                gambar_transformasi = transform_image(
                    gambar_asli, 
                    'distorsi', 
                    skew_x=skew_x, 
                    skew_y=skew_y
                )

            # Tampilkan gambar hasil transformasi
            st.image(
                cv2.cvtColor(gambar_transformasi, cv2.COLOR_BGR2RGB), 
                caption=f"Gambar {transform_type}", 
                use_container_width=True
            )

if __name__ == "__main__":
    main()

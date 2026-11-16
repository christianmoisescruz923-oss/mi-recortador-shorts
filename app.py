import streamlit as st
import tempfile
import os
from moviepy.editor import VideoFileClip

st.set_page_config(page_title="Mi Recortador de Shorts", page_icon="✂️")
st.title("✂️ Mi Recortador de Shorts")
st.write("Sube tu video largo y te lo corto en shorts verticales")

video = st.file_uploader("Sube tu video", type=["mp4","mov","mkv"])
duracion_clip = st.slider("Duración de cada short (segundos)", 15, 60, 30)

if video:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(video.read())
    tfile.close()

    clip_original = VideoFileClip(tfile.name)
    duracion_total = int(clip_original.duration)
    st.video(tfile.name)
    st.write(f"Tu video dura {duracion_total} segundos")

    if st.button("¡Cortar en Shorts! 🔥"):
        num_clips = duracion_total // duracion_clip
        for i in range(min(num_clips, 5)):
            inicio = i * duracion_clip
            fin = inicio + duracion_clip
            clip = clip_original.subclip(inicio, fin)
            w, h = clip.size
            nuevo_w = int(h * 9 / 16)
            x1 = (w - nuevo_w) // 2
            clip_vertical = clip.crop(x1=x1, x2=x1+nuevo_w)
            salida = f"short_{i+1}.mp4"
            clip_vertical.write_videofile(salida, codec="libx264", audio_codec="aac", verbose=False, logger=None)
            st.video(salida)
            with open(salida, "rb") as f:
                st.download_button(f"Descargar Short {i+1}", f, file_name=salida)
        st.success("¡Listo! Ya tienes tus shorts")

import streamlit as st
import tempfile
import os
import yt_dlp
from moviepy import VideoFileClip

st.set_page_config(page_title="Recortador de Shorts", page_icon="✂️")
st.title("✂️ Mi Recortador de Shorts")
st.write("Pega el link de YouTube y te lo corto en shorts verticales")

url = st.text_input("Pega aquí el link de YouTube", placeholder="https://www.youtube.com/watch?v=...")

num_shorts = st.slider("¿Cuántos shorts quieres?", 1, 10, 5)
duracion = st.slider("Duración de cada short (segundos)", 15, 60, 30)

if st.button("Cortar en Shorts"):
    if not url:
        st.warning("Primero pega el link")
    else:
        with st.spinner("Descargando video de YouTube... espera un poco"):
            tmpdir = tempfile.mkdtemp()
            video_path = os.path.join(tmpdir, "video.mp4")
            ydl_opts = {
                'format': 'mp4',
                'outtmpl': video_path,
                'quiet': True,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                clip_original = VideoFileClip(video_path)
                duracion_total = clip_original.duration
                st.write(f"El video dura {int(duracion_total)} segundos")

                for i in range(num_shorts):
                    inicio = i * duracion
                    fin = inicio + duracion
                    if fin > duracion_total:
                        break
                    clip = clip_original.subclipped(inicio, fin)
                    w, h = clip.size
                    nuevo_h = int(w * 16 / 9)
                    if nuevo_h > h:
                        nuevo_h = h
                    clip_vertical = clip.cropped(x_center=w//2, y_center=h//2, width=w, height=nuevo_h)
                    clip_vertical = clip_vertical.resized(height=1280)

                    salida = os.path.join(tmpdir, f"short_{i+1}.mp4")
                    clip_vertical.write_videofile(salida, codec="libx264", audio_codec="aac", logger=None)
                    
                    with open(salida, 'rb') as f:
                        st.download_button(f"Descargar Short {i+1}", f, file_name=f"short_{i+1}.mp4")
                
                st.success("¡Listo! Ya tienes tus shorts")
            except Exception as e:
                st.error(f"Hubo un error: {e}")
                st.write("Prueba con otro video, algunos videos no dejan descargar.")

import streamlit as st
import tempfile as tmpfile
import os
import yt_dlp
from moviepy import VideoFileClip

st.set_page_config(page_title="NEXUS CLIPPER", page_icon="👾", layout="centered")

CSS = "<style>"
CSS += ".stApp{background:#050510;color:white;}"
CSS += "h1{text-align:center;font-size:42px !important;color:#00ffcc !important;text-shadow:0 0 10px #00ffcc,0 0 25px #00ffcc;}"
CSS += ".subtitle{text-align:center;color:#a5f3fc;font-size:14px;margin-bottom:22px;}"
CSS += ".neon-card{background:rgba(10,15,35,0.9);border:1px solid #00ffcc;border-radius:18px;padding:22px;box-shadow:0 0 20px rgba(0,255,204,0.25);margin-bottom:16px;}"
CSS += ".step-title{color:#00ffcc;font-weight:700;font-size:16px;margin:14px 0 8px 0;}"
CSS += ".stTextInput > div > div > input{background:#0a0a1a !important;color:#00ffcc !important;border:1.5px solid #00ffcc !important;border-radius:12px !important;padding:14px !important;}"
CSS += ".stButton > button{width:100%;background:#00ffcc !important;color:#000 !important;font-size:17px !important;font-weight:900 !important;border:none !important;border-radius:14px !important;padding:16px !important;box-shadow:0 0 25px #00ffcc;}"
CSS += ".stDownloadButton > button{width:100%;background:transparent !important;color:#00ffcc !important;border:1.5px solid #00ffcc !important;border-radius:12px !important;font-weight:700 !important;}"
CSS += ".badge{display:inline-block;border:1px solid #00ffcc;color:#00ffcc;font-size:10px;font-weight:800;padding:5px 10px;border-radius:20px;margin:2px;}"
CSS += ".badge-pink{border-color:#ff006e;color:#ff006e;}"
CSS += ".short-card{background:linear-gradient(135deg,rgba(0,255,204,0.12),rgba(255,0,110,0.12));border:1px solid rgba(255,255,255,0.2);border-radius:14px;padding:14px;margin:10px 0 4px 0;}"
CSS += "</style>"
st.markdown(CSS, unsafe_allow_html=True)

st.markdown("<h1>👾 NEXUS CLIPPER</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>SISTEMA V2.0 // YOUTUBE A SHORTS VIRALES // IA ACTIVADA</p>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center'><span class='badge'>● ONLINE</span> <span class='badge badge-pink'>⚡ VELOCIDAD ULTRA</span> <span class='badge'>★ SIN MARCA DE AGUA</span></div><br>", unsafe_allow_html=True)

st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
st.markdown("<div class='step-title'>// 01 - INSERTAR ENLACE</div>", unsafe_allow_html=True)
url = st.text_input("Link", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")
st.markdown("<div class='step-title'>// 02 - CONFIGURACION</div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    num_shorts = st.slider("N DE SHORTS", 1, 10, 5)
with c2:
    duracion = st.slider("DURACION SEG", 15, 60, 30)
st.markdown("<div class='step-title'>// 03 - EJECUTAR</div>", unsafe_allow_html=True)
boton = st.button("▶ GENERAR SHORTS")
st.markdown("</div>", unsafe_allow_html=True)

if boton:
    if not url:
        st.warning("Primero pega el link de YouTube")
    else:
        with st.spinner("PROCESANDO... Descargando y cortando con IA..."):
            tmpdir = tmpfile.mkdtemp()
            video_path = os.path.join(tmpdir, "video.mp4")
            ydl_opts = {
                'format': 'mp4[height<=720]/best[height<=720]',
                'outtmpl': video_path,
                'quiet': True,
                'noplaylist': True,
                'user_agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
                'http_headers': {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'},
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                clip_original = VideoFileClip(video_path)
                duracion_total = clip_original.duration
                st.success(f"VIDEO DETECTADO: {int(duracion_total)}s | GENERANDO {num_shorts} SHORTS...")
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
                    st.markdown(f"<div class='short-card'>🎬 <b>SHORT {i+1}</b> - {duracion}s - LISTO</div>", unsafe_allow_html=True)
                    with open(salida, 'rb') as f:
                        st.download_button(f"DESCARGAR SHORT {i+1}", f, file_name=f"short_{i+1}.mp4", key=f"dl{i}")
                st.balloons()
                st.success("MISION COMPLETADA - Todos tus Shorts estan listos")
            except Exception as e:
                st.error(f"Hubo un error: {e}")
                st.write("Prueba con otro video, algunos videos no dejan descargar.")

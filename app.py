import streamlit as st
import tempfile as tmpfile
import os
import yt_dlp
import numpy as np
from moviepy import VideoFileClip

st.set_page_config(page_title="NEXUS CLIPPER IA", page_icon="🧠", layout="centered")

CSS = "<style>"
CSS += ".stApp{background:#050510;color:white;}"
CSS += "h1{text-align:center;font-size:36px !important;color:#00ffcc !important;text-shadow:0 0 10px #00ffcc,0 0 25px #00ffcc;}"
CSS += ".subtitle{text-align:center;color:#a5f3fc;font-size:13px;margin-bottom:20px;}"
CSS += ".neon-card{background:rgba(10,15,35,0.9);border:1px solid #00ffcc;border-radius:18px;padding:22px;box-shadow:0 0 20px rgba(0,255,204,0.25);margin-bottom:16px;}"
CSS += ".step-title{color:#00ffcc;font-weight:700;font-size:15px;margin:14px 0 8px 0;}"
CSS += ".stTextInput > div > div > input{background:#0a0a1a !important;color:#00ffcc !important;border:1.5px solid #00ffcc !important;border-radius:12px !important;padding:14px !important;}"
CSS += ".stButton > button{width:100%;background:#00ffcc !important;color:#000 !important;font-size:16px !important;font-weight:900 !important;border:none !important;border-radius:14px !important;padding:14px !important;box-shadow:0 0 20px #00ffcc;}"
CSS += ".stDownloadButton > button{width:100%;background:#ff006e !important;color:white !important;font-size:17px !important;font-weight:900 !important;border:none !important;border-radius:14px !important;padding:15px !important;box-shadow:0 0 20px #ff006e;}"
CSS += ".badge{display:inline-block;border:1px solid #00ffcc;color:#00ffcc;font-size:10px;font-weight:800;padding:5px 10px;border-radius:20px;margin:2px;}"
CSS += ".momento{background:rgba(255,230,0,0.10);border:1px solid #ffe600;border-radius:12px;padding:12px;margin:8px 0;}"
CSS += ".momento-seleccionado{background:rgba(0,255,204,0.15);border:2px solid #00ffcc;border-radius:12px;padding:12px;margin:8px 0;}"
CSS += "</style>"
st.markdown(CSS, unsafe_allow_html=True)

if "shorts_list" not in st.session_state:
    st.session_state.shorts_list = []
if "seleccionado" not in st.session_state:
    st.session_state.seleccionado = 0
if "tmpdir_guardado" not in st.session_state:
    st.session_state.tmpdir_guardado = tmpfile.mkdtemp()

st.markdown("<h1>🧠 NEXUS CLIPPER IA</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>La IA analiza tu video y te muestra solo los momentos más épicos</p>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center'><span class='badge'>● IA ACTIVADA</span> <span class='badge'>🔥 DETECTA SUSPENSO</span> <span class='badge'>🎬 MENÚ DE SHORTS</span></div><br>", unsafe_allow_html=True)

def analizar_momentos(video_path, duracion_total, duracion_short, num_shorts):
    try:
        clip = VideoFileClip(video_path)
        audio = clip.audio
        if audio is None:
            return []
        fps_audio = 22050
        arr = audio.to_soundarray(fps=fps_audio)
        if len(arr.shape) > 1:
            arr = arr.mean(axis=1)
        energia = []
        for seg in range(int(duracion_total)):
            ini = seg * fps_audio
            fin = (seg + 1) * fps_audio
            if fin > len(arr):
                break
            trozo = arr[ini:fin]
            energia.append(float(np.sqrt(np.mean(trozo ** 2)) + 0.0001))
        clip.close()
        scores = []
        for i in range(len(energia) - duracion_short):
            ventana = energia[i:i+duracion_short]
            score = (sum(ventana)/len(ventana))*1.0 + max(ventana)*0.8 + (max(ventana)-min(ventana))*0.5
            scores.append((score, i))
        scores.sort(reverse=True)
        elegidos = []
        for score, inicio in scores:
            cerca = False
            for ya in elegidos:
                if abs(inicio - ya) < duracion_short + 5:
                    cerca = True
                    break
            if not cerca:
                elegidos.append(inicio)
            if len(elegidos) >= num_shorts:
                break
        elegidos.sort()
        return elegidos
    except Exception:
        return []

# ===== MENÚ DE SELECCIÓN - ESTO ES LO QUE PEDISTE =====
if len(st.session_state.shorts_list) > 0:
    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
    st.markdown("<div class='step-title'>✅ ¡Análisis terminado! Elige el Short que quieres ver</div>", unsafe_allow_html=True)
    st.write("La IA encontró estos momentos. Toca uno para verlo y si te gusta, descárgalo.")
    for i in range(len(st.session_state.shorts_list)):
        info = st.session_state.shorts_list[i]
        mm = int(info["inicio"] // 60)
        ss = int(info["inicio"] % 60)
        etiqueta = f"🔥 Short {i+1} - Minuto {mm}:{ss:02d} - {info['duracion']}s - Épico {info['score']}%"
        clase = "momento-seleccionado" if st.session_state.seleccionado == i else "momento"
        if st.session_state.seleccionado == i:
            st.markdown(f"<div

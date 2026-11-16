import streamlit as st
import tempfile as tmpfile
import os
import numpy as np
from moviepy import VideoFileClip

st.set_page_config(
    page_title="NEXUS CLIPPER IA",
    page_icon="🧠",
    layout="centered"
)

# ESTILO MODERNO FUTURISTA
st.markdown("<style>", unsafe_allow_html=True)
st.markdown(".stApp{", unsafe_allow_html=True)
st.markdown("background:#050510;", unsafe_allow_html=True)
st.markdown("color:white;", unsafe_allow_html=True)
st.markdown("}", unsafe_allow_html=True)
st.markdown("h1{", unsafe_allow_html=True)
st.markdown("color:#00ffcc !important;", unsafe_allow_html=True)
st.markdown("text-align:center;", unsafe_allow_html=True)
st.markdown("text-shadow:0 0 15px #00ffcc;", unsafe_allow_html=True)
st.markdown("}", unsafe_allow_html=True)
st.markdown(".neon{", unsafe_allow_html=True)
st.markdown("background:#0a0f2a;", unsafe_allow_html=True)
st.markdown("border:1px solid #00ffcc;", unsafe_allow_html=True)
st.markdown("border-radius:18px;", unsafe_allow_html=True)
st.markdown("padding:20px;", unsafe_allow_html=True)
st.markdown("box-shadow:0 0 20px #00ffcc44;", unsafe_allow_html=True)
st.markdown("}", unsafe_allow_html=True)
st.markdown(".stButton > button{", unsafe_allow_html=True)
st.markdown("background:#00ffcc !important;", unsafe_allow_html=True)
st.markdown("color:#000 !important;", unsafe_allow_html=True)
st.markdown("font-weight:900 !important;", unsafe_allow_html=True)
st.markdown("border-radius:14px !important;", unsafe_allow_html=True)
st.markdown("padding:14px !important;", unsafe_allow_html=True)
st.markdown("width:100%;", unsafe_allow_html=True)
st.markdown("}", unsafe_allow_html=True)
st.markdown(".stDownloadButton > button{", unsafe_allow_html=True)
st.markdown("background:#ff006e !important;", unsafe_allow_html=True)
st.markdown("color:white !important;", unsafe_allow_html=True)
st.markdown("font-weight:900 !important;", unsafe_allow_html=True)
st.markdown("border-radius:14px !important;", unsafe_allow_html=True)
st.markdown("padding:14px !important;", unsafe_allow_html=True)
st.markdown("width:100%;", unsafe_allow_html=True)
st.markdown("}", unsafe_allow_html=True)
st.markdown("</style>", unsafe_allow_html=True)

if "shorts_list" not in st.session_state:
    st.session_state.shorts_list = []
if "sel" not in st.session_state:
    st.session_state.sel = 0
if "tmpdir" not in st.session_state:
    st.session_state.tmpdir = tmpfile.mkdtemp()

st.markdown("# 🧠 NEXUS CLIPPER IA")
st.markdown("### Snaptube + IA = Tus mejores Shorts")
st.markdown("---")

def analizar(video_path, total, dur, num):
    try:
        clip = VideoFileClip(video_path)
        audio = clip.audio
        if audio is None:
            return []
        fps_a = 22050
        arr = audio.to_soundarray(fps=fps_a)
        if len(arr.shape) > 1:
            arr = arr.mean(axis=1)
        energia = []
        for seg in range(int(total)):
            ini = seg * fps_a
            fin = (seg + 1) * fps_a
            if fin > len(arr):
                break
            trozo = arr[ini:fin]
            v = float(np.sqrt(np.mean(trozo ** 2)))
            energia.append(v + 0.0001)
        clip.close()
        scores = []
        for i in range(len(energia) - dur):
            ventana = energia[i:i+dur]
            s = sum(ventana) / len(ventana)
            s = s + max(ventana) * 0.8
            scores.append((s, i))
        scores.sort(reverse=True)
        elegidos = []
        for s, inicio in scores:
            cerca = False
            for ya in elegidos:
                if abs(inicio - ya) < dur + 5:
                    cerca = True
            if not cerca:
                elegidos.append(inicio)
            if len(elegidos) >= num:
                break
        elegidos.sort()
        return elegidos
    except Exception:
        return []

def crear_shorts

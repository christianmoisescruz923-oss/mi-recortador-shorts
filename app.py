import streamlit as st
import tempfile
import os
import numpy as np
from moviepy import VideoFileClip

st.set_page_config(page_title="SHORTCUT AI", page_icon="⚡", layout="centered")

st.markdown("""
<style>
.stApp{background:#0f0c29;color:white;}
h1{text-align:center;color:#00f2ff;}
.card{background:#1a1a3a;border:1px solid #a855f7;border-radius:20px;padding:20px;margin-bottom:15px;}
.stButton > button{width:100%;background:#db2777 !important;color:white !important;font-weight:800 !important;border-radius:15px !important;padding:15px !important;}
.stDownloadButton > button{width:100%;border:1px solid #00f2ff !important;border-radius:12px !important;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚡ SHORTCUT AI</h1>", unsafe_allow_html=True)
st.write("Sube tu video y crea clips horizontales 16:9")

if "lista" not in st.session_state:
    st.session_state.lista = []
if "sel" not in st.session_state:
    st.session_state.sel = 0
if "tmpdir" not in st.session_state:
    st.session_state.tmpdir = tempfile.mkdtemp()

if len(st.session_state.lista) > 0:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("✅ Listo! Toca un clip para verlo")
    for i in range(len(st.session_state.lista)):
        info = st.session_state.lista[i]
        mm = int(info["inicio"] // 60)
        ss = int(info["inicio"] % 60)
        txt = "Clip " + str(i+1) + " - Min " + str(mm) + ":" + str(ss)
        st.write(txt)
        if st.button("Ver Clip " + str(i+1), key="ver" + str(i)):
            st.session_state.sel = i
            st.rerun()
    st.write("---")
    idx = st.session_state.sel
    info_sel = st.session_state.lista[idx]
    st.write("Vista previa Clip " + str(idx+1))
    if os.path.exists(info_sel["path"]):
        st.video(info_sel["path"])
        with open(info_sel["path"], "rb") as f:
            datos = f.read()
        st.download_button("Descargar Clip " + str(idx+1), datos, file_name="clip_" + str(idx+1) + ".mp4")
    if st.button("Analizar otro video"):
        st.session_state.lista = []
        st.session_state.sel = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.write("1. Sube tu video")
archivo = st.file_uploader("Sube tu video", type=["mp4", "mov", "mkv", "webm", "avi"], label_visibility="collapsed")
if archivo is not None:
    mb = archivo.size / 1024 / 1024
    st.success("Video subido! " + str(int(mb)) + " MB")
st.write("2. Configura")
col1, col2 = st.columns(2)
with col1:
    num_shorts = st.slider("Cuantos?", 1, 10, 5)
with col2:
    duracion = st.slider("Segundos", 15, 60, 30)
st.write("3. A crear!")
boton = st.button("CORTAR EN HORIZONTAL 16:9")
st

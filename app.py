import streamlit as st
import tempfile as tmpfile
import os
import numpy as np
from moviepy import VideoFileClip

st.set_page_config(page_title="NEXUS CLIPPER IA", page_icon="🧠", layout="centered")

# CSS TODO JUNTO EN UNA SOLA VARIABLE
CSS = "<style>"
CSS = CSS + ".stApp{background:#050510;color:white;}"
CSS = CSS + "h1{color:#00ffcc !important;text-align:center;}"
CSS = CSS + ".neon{background:#0a0f2a;}"
CSS = CSS + ".neon{border:1px solid #00ffcc;}"
CSS = CSS + ".neon{border-radius:18px;padding:20px;}"
CSS = CSS + ".stButton > button{background:#00ffcc !important;}"
CSS = CSS + ".stButton > button{color:#000 !important;}"
CSS = CSS + ".stButton > button{font-weight:900 !important;}"
CSS = CSS + ".stButton > button{border-radius:14px !important;}"
CSS = CSS + ".stButton > button{width:100%;}"
CSS = CSS + ".stDownloadButton > button{background:#ff006e !important;}"
CSS = CSS + ".stDownloadButton > button{color:white !important;}"
CSS = CSS + ".stDownloadButton > button{font-weight:900 !important;}"
CSS = CSS + ".stDownloadButton > button{border-radius:14px !important;}"
CSS = CSS + ".stDownloadButton > button{width:100%;}"
CSS = CSS + "</style>"
st.markdown(CSS, unsafe_allow_html=True)

if "shorts_list" not in st.session_state:
    st.session_state.shorts_list = []
if "sel" not in st.session_state:
    st.session_state.sel = 0
if "tmpdir" not in st.session_state:
    st.session_state.tmpdir = tmpfile.mkdtemp()

st.markdown("# 🧠 NEXUS CLIPPER IA")
st.markdown("### Sube tu video, la IA te da los Shorts")
st.markdown("---")

if len(st.session_state.shorts_list) > 0:
    st.markdown('<div class="neon">', unsafe_allow_html=True)
    st.markdown("## ✅ Analisis terminado!")
    st.write("Toca un Short para ver su vista previa con audio.")
    st.write("Si te gusta, descargalo.")
    for i in range(len(st.session_state.shorts_list)):
        info = st.session_state.shorts_list[i]
        mm = int(info["inicio"] // 60)
        ss = int(info["inicio"] % 60)
        txt = "🔥 Short "
        txt = txt + str(i+1)
        txt = txt + " - Minuto "
        txt = txt + str(mm)
        txt = txt + ":"
        txt = txt + str(ss)
        txt = txt + " - Epico "
        txt = txt + str(info["score"])
        txt = txt + "%"
        if st.session_state.sel == i:
            txt = "✅ " + txt
        st.write(txt)
        btn = "▶️ Ver vista previa Short "
        btn = btn + str(i+1)
        if st.button(btn, key="ver_" + str(i)):
            st.session_state.sel = i
            st.rerun()
    st.write("---")
    idx = st.session_state.sel
    info_sel = st.session_state.shorts_list[idx]
    mm2 = int(info_sel["inicio"] // 60)
    ss2 = int(info_sel["inicio"] % 60)
    t2 = "🎬 Vista previa Short "
    t2 = t2 + str(idx+1)
    t2 = t2 + " - Minuto "
    t2 = t2 + str(mm2)
    t2 = t2 + ":"
    t2 = t2 +

import streamlit as st
import tempfile
import os
import numpy as np
from moviepy import VideoFileClip

st.set_page_config(page_title="SHORTCUT AI - Subir Archivo", page_icon="⚡", layout="centered")

st.markdown("""
<style>
.stApp{background: radial-gradient(circle at top, #0f0c29 0%, #302b63 50%, #24243e 100%);color:white;}
h1{text-align:center;font-size:38px !important;background:linear-gradient(90deg,#00f2ff,#a855f7,#ff00cc);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:900;}
.subtitle{text-align:center;color:#cbd5e1;font-size:15px;margin-top:-15px;margin-bottom:25px;}
.card{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);border-radius:20px;padding:20px;margin-bottom:18px;box-shadow:0 8px 30px rgba(0,0,0,0.4);}
.stButton > button{width:100%;background:linear-gradient(90deg,#7c3aed,#db2777,#06b6d4) !important;color:white !important;font-size:18px !important;font-weight:800 !important;border:none !important;border-radius:15px !important;padding:15px !important;}
.stDownloadButton > button{width:100%;background:rgba(255,255,255,0.12) !important;color:white !important;border:1px solid #00f2ff !important;border-radius:12px !important;margin-top:8px;}
.badge{display:inline-block;background:#00f2ff;color:black;font-size:11px;font-weight:800;padding:4px 10px;border-radius:20px;margin:2px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚡ SHORTCUT AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Sube cualquier video y conviertelo en clips horizontales 16:9 automaticamente</p>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center'><span class='badge'>TODOS LOS FORMATOS</span> <span class='badge' style='background:#a855f7;color:white'>HORIZONTAL 16:9</span> <span class='badge' style='background:#ff00cc;color:white'>HASTA 10 CLIPS</span> <span class='badge'>CON AUDIO</span></div><br>", unsafe_allow_html=True)

if "shorts_list" not in st.session_state:
    st.session_state.shorts_list = []
if "sel" not in st.session_state:
    st.session_state.sel = 0
if "tmpdir" not in st.session_state:
    st.session_state.tmpdir = tempfile.mkdtemp()

if len(st.session_state.shorts_list) > 0:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ✅ Recorte horizontal 16:9 terminado!")
    st.write("Toca un clip para ver su vista previa en formato horizontal 16:9 con audio.")
    for i in range(len(st.session_state.shorts_list)):
        info = st.session_state.shorts_list[i]
        mm = int(info["inicio"] // 60)
        ss = int(info["inicio"] % 60)
        txt = "🔥 Clip " + str(i+1) + " (Horizontal 16:9) - Min " + str(mm) + ":" + str(ss) + " - " + str(info["score"]) + "% Viral"
        if st.session_state.sel == i:
            txt = "✅ " + txt
        st.write(txt)
        if st.button("▶️ Ver Clip " + str(i+1), key="ver_" + str(i)):
            st.session_state.sel = i
            st.rerun()
    st.write("---")
    idx = st.session_state.sel
    info_sel = st.session_state.shorts_list[idx]
    mm2 = int(info_sel["inicio"] // 60)
    ss2 = int(info_sel["inicio"] % 60)
    st.subheader("🎬 Vista previa Clip " + str(idx+1) + " - 16:9 - Min " + str(mm2) + ":" + str(ss2))
    if os.path.exists(info_sel["path"]):
        st.video(info_sel["path"])
        with open(info_sel["path"], "rb") as f:
            datos = f.read()
        st.download_button("⬇️ Descargar Clip " + str(idx+1) + " en 16:9", datos, file_name="clip_horizontal_16x9_" + str(idx+1) + ".mp4", mime="video/mp4")
    if st.button("⬅️ Analizar otro video"):
        st.session_state.shorts_list = []
        st.session_state.sel = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 📤 1. Sube tu video")
st.info("Formatos: MP4

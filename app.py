import streamlit as st
import tempfile
import os
import numpy as np
from moviepy import VideoFileClip

st.set_page_config(
    page_title="SHORTCUT AI",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
.stApp{
background: radial-gradient(
circle at top,
#0f0c29 0%,
#302b63 50%,
#24243e 100%
);
color:white;
}
h1{
text-align:center;
font-size:42px !important;
background:linear-gradient(
90deg,
#00f2ff,
#a855f7,
#ff00cc
);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
font-weight:900;
}
.subtitle{
text-align:center;
color:#cbd5e1;
font-size:15px;
margin-top:-15px;
margin-bottom:20px;
}
.card{
background:rgba(255,255,255,0.08);
backdrop-filter:blur(15px);
border:1px solid rgba(255,255,255,0.15);
border-radius:22px;
padding:22px;
margin-bottom:18px;
box-shadow:0 10px 35px rgba(0,0,0,0.45);
}
.badge{
display:inline-block;
background:#00f2ff;
color:black;
font-size:11px;
font-weight:800;
padding:5px 11px;
border-radius:20px;
margin:2px;
}
.stButton > button{
width:100%;
background:linear-gradient(
90deg,
#7c3aed,
#db2777,
#06b6d4
) !important;
color:white !important;
font-size:17px !important;
font-weight:800 !important;
border:none !important;
border-radius:16px !important;
padding:15px !important;
box-shadow:0 6px 22px rgba(219,39,119,0.5);
}
.stDownloadButton > button{
width:100%;
background:rgba(255,255,255,0.12) !important;
color:white !important;
border:1px solid #00f2ff !important;
border-radius:12px !important;
margin-top:8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚡ SHORTCUT AI</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Sube tu video y crea clips horizontales 16:9</p>",
    unsafe_allow_html=True
)
st.markdown(
    "<div style='text-align:center'>",
    unsafe_allow_html=True
)
st.markdown(
    "<span class='badge'>TODOS LOS FORMATOS</span>",
    unsafe_allow_html=True
)
st.markdown(
    "<span class='badge' style='background:#a855f7;color:white'>HORIZONTAL 16:9</span>",
    unsafe_allow_html=True
)
st.markdown(
    "<span class='badge' style='background:#ff00cc;color:white'>HASTA 10 CLIPS</span>",
    unsafe_allow_html=True
)
st.markdown(
    "<span class='badge'>CON AUDIO</span>",
    unsafe_allow_html=True
)
st.markdown("</div><br>", unsafe_allow_html=True)

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
        txt = "🔥 Clip "
        txt += str(i + 1)
        txt += " - 16:9 - Min "
        txt += str(mm)
        txt += ":"
        txt += str(ss)
        if st.session_state.sel == i:
            txt = "✅ " + txt
        st.write(txt)
        btn = "▶️ Ver Clip " + str(i + 1)
        key = "ver" + str(i)
        if st.button(btn, key=key):
            st.session_state.sel = i
            st.rerun()
    st.write("---")
    idx = st.session_state.sel
    info_sel = st.session_state.lista[idx]
    st.write("🎬 Vista previa Clip " + str(idx + 1))
    if os.path.exists(info_sel["path"]):
        st.video(info_sel["path"])
        with open(info_sel["path"], "rb") as f:
            datos = f.read()
        nombre = "clip_horizontal_16x9_" + str(idx + 1) + ".mp4"
        texto_dl = "⬇️ Descargar Clip " + str(idx + 1)
        st.download_button(texto_dl, datos, file_name=nombre)
    if st.button("⬅️ Analizar otro video"):
        st.session_state.lista = []
        st.session_state.sel = 0
        st.rerun()
    st

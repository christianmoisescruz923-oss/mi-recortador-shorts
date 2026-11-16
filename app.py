import streamlit as st
import tempfile
import os
import numpy as np
from moviepy import VideoFileClip

st.set_page_config(page_title="SHORTCUT AI - Subir Archivo", page_icon="⚡", layout="centered")

# ===== ESTILO FUTURISTA =====
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    h1 {
        text-align: center;
        font-size: 38px !important;
        background: linear-gradient(90deg, #00f2ff, #a855f7, #ff00cc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 15px;
        margin-top: -15px;
        margin-bottom: 25px;
    }
    .card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #7c3aed, #db2777, #06b6d4) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 15px !important;
        box-shadow: 0 5px 20px rgba(219,39,119,0.5);
    }
    .stDownloadButton > button {
        width: 100%;
        background: rgba(255,255,255,0.12) !important;
        color: white !important;
        border: 1px solid #00f2ff !important;
        border-radius: 12px !important;
        margin-top: 8px;
    }
    .badge {
        display: inline-block;
        background: #00f2ff;
        color: black;
        font-size: 11px;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 20px;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ===== TÍTULO =====
st.markdown("<h1>⚡ SHORTCUT AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Sube tu video y convierte los momentos épicos en Shorts virales</p>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center'>"
    "<span class='badge'>✦ IA AUTOMÁTICA</span> "
    "<span class='badge' style='background:#a855f7;color:white'>✦ SIN MARCA DE AGUA</span> "
    "<span class='badge' style='background:#ff00cc;color:white'>✦ CON AUDIO</span>"
    "</div><br>",
    unsafe_allow_html=True
)

if "shorts_list" not in st.session_state:
    st.session_state.shorts_list = []
if "sel" not in st.session_state:
    st.session_state.sel = 0
if "tmpdir" not in st.session_state:
    st.session_state.tmpdir = tempfile.mkdtemp()

# ===== SI YA HAY SHORTS, MOSTRAR MENÚ =====
if len(st.session_state.shorts_list) > 0:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ✅ ¡Análisis terminado!")
    st.write("Toca un Short para ver su vista previa con audio y descargarlo.")

    for i, info in enumerate(st.session_state.shorts_list):
        mm = int(info["inicio"] // 60)
        ss = int(info["inicio"] % 60)
        prefijo = "✅ " if st.session_state.sel == i else ""
        txt = f"{prefijo}🔥 Short {i+1} - Min {mm:02d}:{ss:02d} - {info['score']}% Viral"
        st.write(txt)
        if st.button(f"▶️ Ver Short {i+1}", key=f"ver_{i}"):
            st.session_state.sel = i
            st.rerun()

    st.write("---")
    idx = st.session_state.sel
    info_sel = st.session_state.shorts_list[idx]
    mm2 = int(info_sel["inicio"] // 60)
    ss2 = int(info_sel["inicio"] % 60)
    st.subheader(f"🎬 Vista previa Short {idx+1} - Min {mm2:02d}:{ss2:02d} - Con audio 🔊")

    if os.path.exists(info_sel["path"]):
        st.video(info_sel["path"])
        with open(info_sel["path"], "rb") as f:
            datos = f.read()
        st.download_button(
            f"⬇️ Descargar este Short {idx+1} con audio",
            datos,
            file_name=f"short_epico_{idx+1}.mp4",
            mime="video/mp4"
        )

    if st.button("⬅️ Analizar otro video"):
        for item in st.session_state.shorts_list:
            if os.path.exists(item["path"]):
                os.remove(item["path"])
        st.session_state.shorts_list = []
        st.session_state.sel = 0
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ===== TARJETA PRINCIPAL - SUBIR ARCHIVO =====
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 📤 1. Sube tu video")
st.write("Elige tu video largo desde tu dispositivo.")
archivo = st.file_uploader("Sube tu video aquí", type=["mp4", "mov", "mkv", "webm"], label_visibility="collapsed")

if archivo is not None:
    mb = archivo.size / (1024 * 1024)
    st.success(f"✅ ¡Video subido! Pesa {mb:.1f} MB")

st.markdown("### 🎬 2. Configura tus Shorts")
col1, col2 = st.columns(2)
with col1:
    num_shorts = st.slider("¿Cuántos shorts?", 1, 5, 3)
with col2:
    duracion = st.slider("Duración (seg)", 15, 60, 30)

st.markdown("### 🚀 3. ¡A crear!")
st.write("La IA buscará los momentos de mayor intensidad en el audio.")
boton = st.button("✨ CORTAR EN SHORTS AHORA")
st.markdown("</div>", unsafe_allow_html=True)
st.write("Para videos largos puede tomar unos momentos. No recargues la página.")

if boton:
    if archivo is None:
        st.warning("⚠️ Primero sube un video")
        st.stop()

    tmpdir = st.session_state.tmpdir
    ext = os.path.splitext(archivo.name)[1] or ".mp4"
    video_path = os.path.join(tmpdir, f"input_video{ext}")

    with open(video_path, "wb") as f:
        f.write(archivo.read())

    clip = VideoFileClip(video_path)
    total = clip.duration

    if total <= duracion:
        clip.close()
        st.error(f"⚠️ El video dura {int(total)}s, debe ser más largo que la duración elegida ({duracion}s

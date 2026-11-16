import streamlit as st
import tempfile
import os
import yt_dlp
from moviepy import VideoFileClip

st.set_page_config(page_title="SHORTCUT AI - Recortador", page_icon="⚡", layout="centered")

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
    .stTextInput > div > div > input {
        background: rgba(0,0,0,0.5) !important;
        color: white !important;
        border: 1px solid #a855f7 !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #00f2ff, #ff00cc) !important;
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

# ===== TITULO =====
st.markdown("<h1>⚡ SHORTCUT AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Convierte cualquier video de YouTube en Shorts virales en segundos</p>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center'><span class='badge'>✦ IA AUTOMÁTICA</span> <span class='badge' style='background:#a855f7;color:white'>✦ SIN MARCA DE AGUA</span> <span class='badge' style='background:#ff00cc;color:white'>✦ 100% GRATIS</span></div><br>", unsafe_allow_html=True)

# ===== TARJETA PRINCIPAL =====
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 🔗 1. Pega tu link")
url = st.text_input("Pega aquí el link de YouTube", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")

st.markdown("### 🎬 2. Configura tus Shorts")
col1, col2 = st.columns(2)
with col1:
    num_shorts = st.slider("¿Cuántos shorts?", 1, 10, 5)
with col2:
    duracion = st.slider("Duración (seg)", 15, 60, 30)

st.markdown("### 🚀 3. ¡A crear!")
boton = st.button("✨ CORTAR EN SHORTS AHORA")
st.markdown("</div>", unsafe_allow_html=True)

if boton:
    if not url:
        st.warning("⚠️ Primero pega el link de YouTube")
    else:
        with st.spinner("🤖 La IA está descargando y cortando tu video... espera un poco"):
            tmpdir = tempfile.mk

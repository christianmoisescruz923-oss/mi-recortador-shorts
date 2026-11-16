import streamlit as st
import tempfile as tmpfile
import os
import yt_dlp
from moviepy import VideoFileClip

st.set_page_config(page_title="NEXUS CLIPPER - Futuro", page_icon="👾", layout="centered")

# ===== ESTILO CYBERPUNK FUTURISTA V2 =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@400;600&display=swap');
    .stApp {
        background: #050510;
        background-image: 
            radial-gradient(circle at 20% 20%, rgba(0,255,204,0.15) 0%, transparent 40%),
            radial-gradient(circle at 80% 80%, rgba(255,0,110,0.15) 0%, transparent 40%),
            linear-gradient(rgba(0,255,204,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,255,204,0.05) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    h1 {
        text-align: center;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 42px !important;
        letter-spacing: 2px;
        color: #00ffcc !important;
        text-shadow: 0 0 10px #00ffcc, 0 0 25px #00ffcc, 0 0 45px #00ffcc;
        margin-bottom: 0px !important;
    }
    .subtitle {
        text-align: center;
        color: #a5f3fc;
        font-size: 14px;
        letter-spacing: 1px;
        margin-bottom: 22px;
    }
    .neon-card {
        background: rgba(10, 15, 35, 0.85);
        border: 1px solid #00ffcc;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 0 20px rgba(0,255,204,0.25), inset 0 0 20px rgba(0,255,204,0.05);
        margin-bottom: 16px;
    }
    .step-title {
        color: #00ffcc;
        font-weight: 700;
        font-size: 16px;
        margin: 14px 0 8px 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stTextInput > div > div > input {
        background: #0a0a1a !important;
        color: #00ffcc !important;
        border: 1.5px solid #00ffcc !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-size: 15px !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
    }
    .stSlider label { color: white !important; font-weight: 600; }
    .stButton > button {
        width: 100%;
        background: #00ffcc !important;
        color: #000 !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 17px !important;
        font-weight: 900 !important;
        letter-spacing: 1px;
        border: none !important;
        border-radius: 14px !important;
        padding: 16px !important;
        box-shadow: 0 0 25px #00ffcc, 0 0 50px rgba(0,255,204,0.4);
        transition: 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 35px #00ffcc;
    }
    .stDownloadButton > button {
        width: 100%;
        background: transparent !important;
        color: #00ffcc !important;
        border: 1.5px solid #00ffcc !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 12px !important;
    }
    .badge-row { text-align: center; margin-bottom: 18px; }
    .badge {
        display: inline-block

import streamlit as st
import tempfile
import os
import numpy as np
from moviepy import VideoFileClip

st.set_page_config(page_title="SHORTCUT AI", page_icon="⚡", layout="centered")
st.markdown("""
<style>
.stApp{background: radial-gradient(circle at top, #0f0c29 0%, #302b63 50%, #24243e 100%);color:white;}
h1{text-align:center;font-size:38px !important;background:linear-gradient(90deg,#00f2ff,#a855f7,#ff00cc);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:900;}
.subtitle{text-align:center;color:#cbd5e1;font-size:15px;margin-top:-15px;margin-bottom:25px;}
.card{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);border-radius:20px;padding:20px;margin-bottom:18px;}
.stButton > button{width:100%;background:linear-gradient(90deg,#7c3aed,#db2777,#06b6d4) !important;color:white !important;font-size:18px !important;font-weight:800 !important;border:none !important;border-radius:15px !important;padding:15px !important;}
.stDownloadButton > button{width:100%;background:rgba(255,255,255,0.12) !important;color:white !important;border:1px solid #00f2ff !important;border-radius:12px !important;margin-top:8px;}
.badge{display:inline-block;background:#00f2ff;color:black;font-size:11px;font-weight:800;padding:4px 10px;border-radius:20px;margin:2px;}
</style>
""", unsafe_allow_html=True)
st.markdown("<h1>⚡ SHORTCUT AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='

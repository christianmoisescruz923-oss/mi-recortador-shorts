import streamlit as st
import tempfile as tmpfile
import os
import yt_dlp
from moviepy import VideoFileClip

st.set_page_config(page_title="NEXUS CLIPPER", page_icon="👾", layout="centered")

CSS = "<style>"
CSS += ".stApp{background:#050510;color:white;}"
CSS += "h1{text-align:center;font-size:42px !important;color:#00ffcc !important;text-shadow:0 0 10px #00ffcc,0 0 25px #00ffcc;}"
CSS += ".subtitle{text-align:center;color:#a5f3fc;font-size:14px;margin-bottom:22px;}"
CSS += ".neon-card{background:rgba(10,15,35,0.9);border:1px solid #00ffcc;border-radius:18px;padding:22px;box-shadow:0 0 20px rgba(0,255,204,0.25);margin-bottom:16px;}"
CSS += ".step-title{color:#00ffcc;font-weight:700;font-size:16px;margin:14px 0 8px 0;}"
CSS += ".stTextInput > div > div > input{background:#0a0a1a !important;color:#00ffcc !important;border:1.5px solid #00ffcc !important;border-radius:12px !important;padding:14px !important;}"
CSS += ".stButton > button{width:100%;background:#00ffcc !important;color:#000 !important;font-size:17px !important;font-weight:900 !important;border:none !important;border-radius:14px !important;padding:16px !important;box-shadow:0 0 25px #00ffcc;}"
CSS += ".stDownloadButton > button{width:100%;background:#ff006e !important;color:white !important;font-size:16px !important;font-weight:900 !important;border:none !important;border-radius:14px !important;padding:14px !important;box-shadow:0 0 20px #ff006e;}"
CSS += ".badge{display:inline-block;border:1px solid #00ffcc;color:#00ffcc;font-size:10px;font-weight:800;padding:5px 10px;border-radius:20px;margin:2px;}"
CSS += ".short-card{background:linear-gradient(135deg,rgba(0,255,204,0.12),rgba(255,0,110,0.12));border:1px solid rgba(255,255,255,0.2);border-radius:14px;padding:14px;margin:10px 0 4px 0;}"
CSS += "</style>"
st.markdown(CSS, unsafe_allow_html=True)

if "shorts_list" not in st.session_state:
    st.session_state.shorts_list = []
if "shorts_bytes" not in st.session_state:
    st.session_state.shorts_bytes = {}

st.markdown("<h1>👾 NEXUS CLIPPER</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>GENERAR -> VER -> ELEGIR -> DESCARGAR SOLO EL QUE TE GUSTE</p>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center'><span class='badge'>● ONLINE</span> <span class='badge'>🎬 VISTA PREVIA</span></div><br>", unsafe_allow_html=True)

# Si ya hay shorts generados, mostrar el MENU DE VER
if len(st.session_state.shorts_list) > 0:
    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
    st.markdown("<div class='step-title'>🎬 TUS SHORTS LISTOS - ESCOGE UNO PARA VERLO</div>", unsafe_allow_html=True)
    st.write("Toca un Short para verlo, y si te gusta lo descargas abajo.")
    opciones = [f"🎬 Short {i+1} - {st.session_state.shorts_list[i]['duracion']}s" for i in range(len(st.session_state.shorts_list))]
    seleccion = st.selectbox("Elige un Short para ver:", opciones)
    idx = opciones.index(seleccion)
    info = st.session_state.shorts_list[idx]
    st.video(info["path"])
    st.markdown(f"<div class='short-card'>🎬 <b>{seleccion}</b> - Listo para TikTok / Shorts / Reels</div>", unsafe_allow_html=True)
    with open(info["path"], "rb") as f:
        st.download_button(f"⬇️ DESCARGAR ESTE SHORT - {seleccion}", f, file_name=f"short_{idx+1}.mp4", key=f"dl_unico_{idx}")
    colA, colB = st.columns(2)
    with colA:
        if st.button("⬅️ HACER OTROS SHORTS"):
            st.session_state.shorts_list = []
            st.session_state.shorts_bytes = {}
            st.rerun()
    with colB:
        if st.button("⬇️ DESCARGAR TODOS"):
            st.info("Para descargar todos, ve uno por uno y picale descargar, asi no se traba tu cel.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Si NO hay shorts, mostrar el generador
st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
modo = st.radio("Como quieres hacerlo?", ["📤 Subir video desde mi celular (SIEMPRE funciona)", "🔗 Pegar link de YouTube (a veces YouTube lo bloquea)"], index=0)
tmpdir = tmpfile.mkdtemp()
video_path_final = None
url = None
minuto_inicio = 0
if modo.startswith("🔗"):
    url = st.text_input("Link", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")
    minuto_inicio = st.slider("Empezar desde el minuto", 0, 110, 0)
else:
    st.write("1. Descarga el video en tu cel con Snaptube")
    st.write("2. Subelo aqui abajo")
    archivo = st.file_uploader("Sube tu video MP4 aqui", type=["mp4", "mov", "mkv", "webm"])
    if archivo is not None:
        video_path_final = os.path.join(tmpdir, "subido.mp4")
        with open(video_path_final, "wb") as f:
            f.write(archivo.read())
        st.success("Video subido! Ya puedes cortar")
    minuto_inicio = st.slider("Empezar desde el minuto (si es largo)", 0, 110, 0)
c1, c2 = st.columns(2)
with c1:
    num_shorts = st.slider("N DE SHORTS", 1, 10, 5)
with c2:
    duracion = st.slider("DURACION SEG", 15, 60, 30)
boton = st.button("▶ GENERAR SHORTS Y VERLOS")
st.markdown("</div>", unsafe_allow_html=True)

if boton:
    video_path = video_path_final
    if modo.startswith("🔗"):
        if not url:
            st.warning("Pega el link primero")
            st.stop()
        with st.spinner("Intentando descargar de YouTube..."):
            video_path = os.path.join(tmpdir, "video.mp4")
            inicio_seg = minuto_inicio * 60
            fin_seg = inicio_seg + (num_shorts * duracion) + 5
            intentos = [{'player_client': ['android']}, {'player_client': ['ios']}, {'player_client': ['web']}]
            descargado = False
            for intento in intentos:
                try:
                    ydl_opts = {'format': 'mp4[height<=720]/best[height<=720]', 'outtmpl': video_path, 'quiet': True, 'noplaylist

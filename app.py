import streamlit as st
import tempfile as tmpfile
import os
import yt_dlp
import numpy as np
from moviepy import VideoFileClip

st.set_page_config(page_title="NEXUS CLIPPER IA", page_icon="🧠", layout="centered")

CSS = "<style>"
CSS += ".stApp{background:#050510;color:white;}"
CSS += "h1{text-align:center;font-size:36px !important;color:#00ffcc !important;}"
CSS += ".subtitle{text-align:center;color:#a5f3fc;font-size:13px;margin-bottom:20px;}"
CSS += ".neon-card{background:rgba(10,15,35,0.9);border:1px solid #00ffcc;border-radius:18px;padding:22px;margin-bottom:16px;}"
CSS += ".step-title{color:#00ffcc;font-weight:700;font-size:15px;margin:14px 0 8px 0;}"
CSS += ".stTextInput > div > div > input{background:#0a0a1a !important;color:#00ffcc !important;border:1.5px solid #00ffcc !important;border-radius:12px !important;padding:14px !important;}"
CSS += ".stButton > button{width:100%;background:#00ffcc !important;color:#000 !important;font-size:16px !important;font-weight:900 !important;border:none !important;border-radius:14px !important;padding:14px !important;}"
CSS += ".stDownloadButton > button{width:100%;background:#ff006e !important;color:white !important;font-size:17px !important;font-weight:900 !important;border:none !important;border-radius:14px !important;padding:15px !important;}"
CSS += ".badge{display:inline-block;border:1px solid #00ffcc;color:#00ffcc;font-size:10px;font-weight:800;padding:5px 10px;border-radius:20px;margin:2px;}"
CSS += ".momento{background:rgba(255,230,0,0.10);border:1px solid #ffe600;border-radius:12px;padding:12px;margin:8px 0;}"
CSS += ".momento-sel{background:rgba(0,255,204,0.15);border:2px solid #00ffcc;border-radius:12px;padding:12px;margin:8px 0;}"
CSS += "</style>"
st.markdown(CSS, unsafe_allow_html=True)

if "shorts_list" not in st.session_state:
    st.session_state.shorts_list = []
if "seleccionado" not in st.session_state:
    st.session_state.seleccionado = 0
if "tmpdir_guardado" not in st.session_state:
    st.session_state.tmpdir_guardado = tmpfile.mkdtemp()

st.markdown("<h1>🧠 NEXUS CLIPPER IA</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>La IA analiza tu video y te muestra solo los momentos mas epicos</p>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center'><span class='badge'>IA ACTIVADA</span> <span class='badge'>DETECTA SUSPENSO</span> <span class='badge'>MENU DE SHORTS</span></div><br>", unsafe_allow_html=True)

def analizar_momentos(video_path, duracion_total, duracion_short, num_shorts):
    try:
        clip = VideoFileClip(video_path)
        audio = clip.audio
        if audio is None:
            return []
        fps_audio = 22050
        arr = audio.to_soundarray(fps=fps_audio)
        if len(arr.shape) > 1:
            arr = arr.mean(axis=1)
        energia = []
        total_seg = int(duracion_total)
        for seg in range(total_seg):
            ini = seg * fps_audio
            fin = (seg + 1) * fps_audio
            if fin > len(arr):
                break
            trozo = arr[ini:fin]
            energia.append(float(np.sqrt(np.mean(trozo ** 2)) + 0.0001))
        clip.close()
        scores = []
        for i in range(len(energia) - duracion_short):
            ventana = energia[i:i+duracion_short]
            score = (sum(ventana)/len(ventana))*1.0 + max(ventana)*0.8 + (max(ventana)-min(ventana))*0.5
            scores.append((score, i))
        scores.sort(reverse=True)
        elegidos = []
        for score, inicio in scores:
            cerca = False
            for ya in elegidos:
                if abs(inicio - ya) < duracion_short + 5:
                    cerca = True
                    break
            if not cerca:
                elegidos.append(inicio)
            if len(elegidos) >= num_shorts:
                break
        elegidos.sort()
        return elegidos
    except Exception:
        return []

if len(st.session_state.shorts_list) > 0:
    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
    st.markdown("<div class='step-title'>✅ Analisis terminado! Elige el Short que quieres ver</div>", unsafe_allow_html=True)
    st.write("La IA encontro estos momentos. Toca uno para verlo y si te gusta, descargalo.")
    for i in range(len(st.session_state.shorts_list)):
        info = st.session_state.shorts_list[i]
        mm = int(info["inicio"] // 60)
        ss = int(info["inicio"] % 60)
        ss_texto = str(ss)
        if ss < 10:
            ss_texto = "0" + str(ss)
        etiqueta = "Short " + str(i+1) + " - Minuto " + str(mm) + ":" + ss_texto + " - " + str(info["duracion"]) + "s - Epico " + str(info["score"]) + "%"
        if st.session_state.seleccionado == i:
            html_caja = "<div class='momento-sel'><b>" + etiqueta + "</b><br><span style='font-size:12px;'>Estas viendo este ahora</span></div>"
            st.markdown(html_caja, unsafe_allow_html=True)
        else:
            html_caja2 = "<div class='momento'><b>" + etiqueta + "</b></div>"
            st.markdown(html_caja2, unsafe_allow_html=True)
        boton_texto = "Ver Short " + str(i+1)
        if st.button(boton_texto, key="ver_" + str(i)):
            st.session_state.seleccionado = i
            st.rerun()
    st.markdown("<hr>", unsafe_allow_html=True)
    idx = st.session_state.seleccionado
    info_sel = st.session_state.shorts_list[idx]
    mm2 = int(info_sel["inicio"] // 60)
    ss2 = int(info_sel["inicio"] % 60)
    ss2_texto = str(ss2)
    if ss2 < 10:
        ss2_texto = "0" + str(ss2)
    titulo_ver = "<div class='step-title'>Estas viendo: Short " + str(idx+1) + " - Minuto " + str(mm2) + ":" + ss2_texto + "</div>"
    st.markdown(titulo_ver, unsafe_allow_html=True)
    if os.path.exists(info_sel["path"]):
        st.video(info_sel["path"])
        st.write("Te gusto este momento? Si si, descargalo abajo. Si no, elige otro de arriba.")
        with open(info_sel["path"], "rb") as f:
            datos = f.read()
        nombre_archivo = "short_epico_" + str(idx+1) + ".mp4"
        boton_dl = "Descargar Short " + str(idx+1) + " - Minuto " + str(mm2) + ":" + ss2_texto
        st.download_button(boton_dl, datos, file_name=nombre_archivo, mime="video/mp4", key="dl_" + str(idx))
    else:
        st.error("La aplicacion se reinicio. Vuelve a analizar el video.")
    if st.button("Analizar otro video"):
        st.session_state.shorts_list = []
        st.session_state.seleccionado = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
st.markdown("<div class='step-title'>1. Pega tu video</div>", unsafe_allow_html=True)
url = st.text_input("Link de YouTube", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")
st.markdown("<div class='step-title'>2. Cuantos momentos epicos quieres?</div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    num_shorts = st.slider("Cantidad de Shorts", 1, 5, 3)
with c2:
    duracion = st.slider("Duracion de cada Short (segundos)", 15, 60, 30)
st.markdown("<div class='step-title'>3. Como detecta la IA lo epico?</div>", unsafe_allow_html=True)
st.write("Volumen alto = gritos, sustos y risas")
st.write("Cambios bruscos = suspenso y revelaciones")
st.write("Musica intensa = momentos emotivos")
boton = st.button("ANALIZAR VIDEO Y MOSTRARME EL MENU")
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#94a3b8;font-size:12px;'>Para videos de 2 horas, el analisis tarda 1-2 minutos. No recargues

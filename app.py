import streamlit as st
import tempfile as tmpfile
import os
import numpy as np
from moviepy import VideoFileClip

st.set_page_config(page_title="NEXUS CLIPPER IA", page_icon="🧠", layout="centered")

st.markdown("<style>", unsafe_allow_html=True)
st.markdown(".stApp{background:#050510;color:white;}", unsafe_allow_html=True)
st.markdown("h1{color:#00ffcc !important;text-align:center;}", unsafe_allow_html=True)
st.markdown(".neon{background:#0a0f2a;border:1px solid #00ffcc;border-radius:18px;padding:20px;}", unsafe_allow_html=True)
st.markdown(".stButton > button{background:#00ffcc !important;color:#000 !important;font-weight:900 !important;border-radius:14px !important;width:100%;}", unsafe_allow_html=True)
st.markdown(".stDownloadButton > button{background:#ff006e !important;color:white !important;font-weight:900 !important;border-radius:14px !important;width:100%;}", unsafe_allow_html=True)
st.markdown("</style>", unsafe_allow_html=True)

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
    t2 = t2 + str(ss2)
    t2 = t2 + " - Con audio 🔊"
    st.subheader(t2)
    if os.path.exists(info_sel["path"]):
        st.video(info_sel["path"])
        st.write("Escuchalo con audio. Si te gusta, descargalo.")
        with open(info_sel["path"], "rb") as f:
            datos = f.read()
        nombre = "short_epico_"
        nombre = nombre + str(idx+1) + ".mp4"
        dl = "⬇️ Descargar este Short "
        dl = dl + str(idx+1)
        dl = dl + " con audio"
        st.download_button(dl, datos, file_name=nombre, mime="video/mp4")
        st.write("Si no te gusta, elige otro Short de arriba.")
    if st.button("⬅️ Analizar otro video"):
        st.session_state.shorts_list = []
        st.session_state.sel = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

st.markdown('<div class="neon">', unsafe_allow_html=True)
st.markdown("## 📱 1. Descarga con Snaptube")
st.write("1. Abre Snaptube")
st.write("2. Descarga tu video en 360p")
st.write("3. Subelo aqui abajo")
st.markdown("## 📤 2. Sube tu video aqui")
archivo = st.file_uploader("Sube tu video de Snaptube", type=["mp4", "mov", "mkv", "webm"])
if archivo is not None:
    mb = archivo.size / 1024 / 1024
    st.success("Video subido! Pesa " + str(int(mb)) + " MB")
    st.write("Ya puedes analizarlo abajo.")
st.markdown("## ⚙️ 3. Configura tus Shorts")
num_shorts = st.slider("Cuantos Shorts quieres", 1, 5, 3)
duracion = st.slider("Segundos de cada Short", 15, 60, 30)
st.write("La IA busca gritos, sustos,")
st.write("suspenso y musica intensa.")
boton = st.button("🧠 ANALIZAR MI VIDEO")
st.markdown("</div>", unsafe_allow_html=True)
st.write("Para videos de 2 horas tarda 1-2 min.")
st.write("No recargues la pagina.")

if boton:
    if archivo is None:
        st.warning("Primero sube un video")
        st.stop()
    tmpdir = st.session_state.tmpdir
    video_path = os.path.join(tmpdir, "snaptube.mp4")
    with open(video_path, "wb") as f:
        f.write(archivo.read())
    clip_temp = VideoFileClip(video_path)
    total = clip_temp.duration
    clip_temp.close()
    mins = int(total // 60)
    st.success("Video de " + str(mins) + " minutos")
    with st.spinner("La IA escucha todo el video..."):
        clip = VideoFileClip(video_path)
        audio = clip.audio
        fps_a = 22050
        arr = audio.to_soundarray(fps=fps_a)
        if len(arr.shape) > 1:
            arr = arr.mean(axis=1)
        energia = []
        for seg in range(int(total)):
            ini = seg * fps_a
            fin = (seg + 1) * fps_a
            if fin > len(arr):
                break
            trozo = arr[ini:fin]
            v = float(np.sqrt(np.mean(trozo ** 2)))
            energia.append(v + 0.0001)
        clip.close()
        scores = []
        for i in range(len(energia) - duracion):
            ventana = energia[i:i+duracion]
            s = sum(ventana) / len(ventana)
            s = s + max(ventana) * 0.8
            scores.append((s, i))
        scores.sort(reverse=True)
        inicios = []
        for s, inicio in scores:
            cerca = False
            for ya in inicios:
                if abs(inicio - ya) < duracion + 5:
                    cerca = True
            if not cerca:
                inicios.append(inicio)
            if len(inicios) >= num_shorts:
                break
        inicios.sort()
    st.success("Encontre momentos epicos.")
    with st.spinner("Cortando en vertical con audio..."):
        clip_o = VideoFileClip(video_path)
        nuevos = []
        prog = st.progress(0)
        for i, inicio in enumerate(inicios):
            fin = inicio + duracion
            if fin > total:
                fin = total
            clip2 = clip_o.subclipped(inicio, fin)
            w, h = clip2.size
            nh = int(w * 16 / 9)
            if nh > h:
                nh = h
            cv = clip2.cropped(x_center=w//2, y_center=h//2, width=w, height=nh)
            cv = cv.resized(height=720)
            salida = os.path.join(tmpdir, "s" + str(i+1) + ".mp4")
            cv.write_videofile(salida, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
            puntaje = 98 - (i * 4)
            if puntaje < 75:
                puntaje = 75
            nuevos.append({"path": salida, "duracion": duracion, "inicio": inicio, "score": puntaje})
            prog.progress((i+1)/len(inicios))
        clip_o.close()
        st.session_state.shorts_list = nuevos
        st.session_state.sel = 0
        st.balloons()
        st.rerun()

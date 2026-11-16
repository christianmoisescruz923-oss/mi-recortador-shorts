import streamlit as st
import tempfile as tmpfile
import os
import numpy as np
from moviepy import VideoFileClip

st.set_page_config(
    page_title="NEXUS CLIPPER IA",
    page_icon="🧠",
    layout="centered"
)

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
st.markdown("### Snaptube + IA = Tus mejores Shorts")
st.markdown("---")

def analizar_momentos(video_path, total, dur, num):
    clip = VideoFileClip(video_path)
    audio = clip.audio
    if audio is None:
        return []
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
    for i in range(len(energia) - dur):
        ventana = energia[i:i+dur]
        s = sum(ventana) / len(ventana)
        s = s + max(ventana) * 0.8
        scores.append((s, i))
    scores.sort(reverse=True)
    elegidos = []
    for s, inicio in scores:
        cerca = False
        for ya in elegidos:
            if abs(inicio - ya) < dur + 5:
                cerca = True
        if not cerca:
            elegidos.append(inicio)
        if len(elegidos) >= num:
            break
    elegidos.sort()
    return elegidos

def crear(video_path, total, inicios, duracion):
    clip_o = VideoFileClip(video_path)
    nuevos = []
    prog = st.progress(0)
    tmpdir = st.session_state.tmpdir
    for i, inicio in enumerate(inicios):
        fin = inicio + duracion
        if fin > total:
            fin = total
        clip = clip_o.subclipped(inicio, fin)
        w, h = clip.size
        nh = int(w * 16 / 9)
        if nh > h:
            nh = h
        cv = clip.cropped(
            x_center=w//2,
            y_center=h//2,
            width=w,
            height=nh
        )
        cv = cv.resized(height=720)
        salida = os.path.join(tmpdir, "s" + str(i+1) + ".mp4")
        cv.write_videofile(
            salida,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            logger=None
        )
        puntaje = 98 - (i * 4)
        if puntaje < 75:
            puntaje = 75
        nuevos.append(
            {
                "path": salida,
                "duracion": duracion,
                "inicio": inicio,
                "score": puntaje
            }
        )
        prog.progress((i+1)/len(inicios))
    clip_o.close()
    return nuevos

if len(st.session_state.shorts_list) > 0:
    st.markdown('<div class="neon">', unsafe_allow_html=True)
    st.markdown("## ✅ Analisis terminado!")
    st.write("Elige un Short para verlo.")
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
        btn = "▶️ Ver Short "
        btn = btn + str(i+1)
        if st.button(btn, key="ver_" + str(i)):
            st.session_state.sel = i
            st.rerun()
    st.write("---")
    idx = st.session_state.sel
    info_sel = st.session_state.shorts_list[idx]
    mm2 = int(info_sel["inicio"] // 60)
    ss2 = int(info_sel["inicio

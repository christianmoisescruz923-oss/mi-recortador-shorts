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
.stApp{background:#0f0c29;color:white;}
h1{text-align:center;color:#00f2ff;}
.card{
background:#1a1a3a;
border:1px solid #a855f7;
border-radius:20px;
padding:20px;
margin-bottom:15px;
}
.stButton > button{
width:100%;
background:#db2777 !important;
color:white !important;
font-weight:800 !important;
border-radius:15px !important;
padding:15px !important;
}
.stDownloadButton > button{
width:100%;
border:1px solid #00f2ff !important;
border-radius:12px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚡ SHORTCUT AI</h1>", unsafe_allow_html=True)
st.write("Sube tu video y crea clips horizontales 16:9")

if "lista" not in st.session_state:
    st.session_state.lista = []
if "sel" not in st.session_state:
    st.session_state.sel = 0
if "tmpdir" not in st.session_state:
    st.session_state.tmpdir = tempfile.mkdtemp()

if len(st.session_state.lista) > 0:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("Listo! Toca un clip para verlo")
    for i in range(len(st.session_state.lista)):
        info = st.session_state.lista[i]
        mm = int(info["inicio"] // 60)
        ss = int(info["inicio"] % 60)
        txt = "Clip "
        txt += str(i + 1)
        txt += " - Min "
        txt += str(mm)
        txt += ":"
        txt += str(ss)
        st.write(txt)
        btn = "Ver Clip " + str(i + 1)
        key = "ver" + str(i)
        if st.button(btn, key=key):
            st.session_state.sel = i
            st.rerun()
    st.write("---")
    idx = st.session_state.sel
    info_sel = st.session_state.lista[idx]
    st.write("Vista previa Clip " + str(idx + 1))
    if os.path.exists(info_sel["path"]):
        st.video(info_sel["path"])
        with open(info_sel["path"], "rb") as f:
            datos = f.read()
        nombre = "clip_" + str(idx + 1) + ".mp4"
        texto_dl = "Descargar Clip " + str(idx + 1)
        st.download_button(texto_dl, datos, file_name=nombre)
    if st.button("Analizar otro video"):
        st.session_state.lista = []
        st.session_state.sel = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.write("1. Sube tu video")
archivo = st.file_uploader(
    "Sube tu video",
    type=["mp4", "mov", "mkv", "webm", "avi"],
    label_visibility="collapsed"
)
if archivo is not None:
    mb = archivo.size / 1024 / 1024
    st.success("Video subido! " + str(int(mb)) + " MB")
st.write("2. Configura")
col1, col2 = st.columns(2)
with col1:
    num_shorts = st.slider("Cuantos?", 1, 10, 5)
with col2:
    duracion = st.slider("Segundos", 15, 60, 30)
st.write("3. A crear!")
boton = st.button("CORTAR EN HORIZONTAL 16:9")
st.markdown("</div>", unsafe_allow_html=True)

if boton:
    if archivo is None:
        st.warning("Primero sube un video")
        st.stop()
    tmpdir = st.session_state.tmpdir
    video_path = os.path.join(tmpdir, "video.mp4")
    with open(video_path, "wb") as f:
        f.write(archivo.read())
    try:
        clip_temp = VideoFileClip(video_path)
        total = clip_temp.duration
        clip_temp.close()
    except Exception as e:
        st.error("No se pudo leer: " + str(e))
        st.stop()
    if total < duracion:
        st.warning("Tu video es mas corto que la duracion elegida")
        st.stop()
    st.success("Video de " + str(int(total // 60)) + " min")
    with st.spinner("Analizando audio..."):
        try:
            clip = VideoFileClip(video_path)
            audio = clip.audio
            if audio is None:
                energia = [1.0 for _ in range(int(total))]
            else:
                fps_a = 11025
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
            limite = len(energia) - duracion
            for i in range(limite):
                ventana = energia[i:i + duracion]
                prom = sum(ventana) / len(ventana)
                s = prom + max(ventana) * 0.8
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
        except Exception as e:
            st.error("Error: " + str(e))
            st.stop()
    if len(inicios) == 0:
        st.warning("No se encontraron momentos")
        st.stop()
    st.success("Momentos encontrados!")
    with st.spinner("Cortando en 16:9..."):
        try:
            clip_o = VideoFileClip(video_path)
            nuevos = []
            prog = st.progress(0)
            for i, inicio in enumerate(inicios):
                fin = inicio + duracion
                if fin > total:
                    fin = total
                clip2 = clip_o.subclipped(inicio, fin)
                w, h = clip2.size
                th = int(w * (9 / 16))
                if th > h:
                    th = h
                    tw = int(h * (16 / 9))
                    cv = clip2.cropped(
                        x_center=w // 2,
                        y_center=h // 2,
                        width=tw,
                        height=th
                    )
                else:
                    cv = clip2.cropped(
                        x_center=w // 2,
                        y_center=h // 2,
                        width=w,
                        height=th
                    )
                cv = cv.resized(width=1280)
                salida = os.path.join(tmpdir, "s" + str(i + 1) + ".mp4")
                cv.write_videofile(
                    salida,
                    codec="libx264",
                    audio_codec="aac",
                    preset="ultrafast",
                    logger=None
                )
                puntaje = 98 - (i * 2)
                if puntaje < 75:
                    puntaje = 75
                nuevos.append(
                    {
                        "path": salida,
                        "inicio": inicio,
                        "score": puntaje
                    }
                )
                prog.progress((i + 1) / len(inicios))
            clip_o.close()
            st.session_state.lista = nuevos
            st.session_state.sel = 0
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error("Error al exportar: " + str(e))

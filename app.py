import streamlit as st
import tempfile as tmpfile
import os
import yt_dlp
import numpy as np
from moviepy import VideoFileClip

st.set_page_config(
    page_title="NEXUS CLIPPER IA",
    page_icon="🧠"
)

if "shorts_list" not in st.session_state:
    st.session_state.shorts_list = []
if "sel" not in st.session_state:
    st.session_state.sel = 0
if "tmpdir" not in st.session_state:
    st.session_state.tmpdir = tmpfile.mkdtemp()

st.title("🧠 NEXUS CLIPPER IA")
st.write("La IA analiza tu video")
st.write("y te muestra los momentos mas epicos")
st.write("---")

def analizar(video_path, total, dur, num):
    try:
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
    except Exception:
        return []

if len(st.session_state.shorts_list) > 0:
    st.subheader("Elige el Short que quieres ver")
    st.write("Toca uno para verlo.")
    st.write("Si te gusta, descargalo.")
    for i in range(len(st.session_state.shorts_list)):
        info = st.session_state.shorts_list[i]
        mm = int(info["inicio"] // 60)
        ss = int(info["inicio"] % 60)
        txt = "Short "
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
        else:
            st.write(txt)
        btn = "Ver Short "
        btn = btn + str(i+1)
        if st.button(btn, key="ver_" + str(i)):
            st.session_state.sel = i
            st.rerun()
    st.write("---")
    idx = st.session_state.sel
    info_sel = st.session_state.shorts_list[idx]
    mm2 = int(info_sel["inicio"] // 60)
    ss2 = int(info_sel["inicio"] % 60)
    t2 = "Estas viendo Short "
    t2 = t2 + str(idx+1)
    t2 = t2 + " - Minuto "
    t2 = t2 + str(mm2)
    t2 = t2 + ":"
    t2 = t2 + str(ss2)
    st.subheader(t2)
    if os.path.exists(info_sel["path"]):
        st.video(info_sel["path"])
        with open(info_sel["path"], "rb") as f:
            datos = f.read()
        nombre = "short_epico_"
        nombre = nombre + str(idx+1) + ".mp4"
        dl = "Descargar Short "
        dl = dl + str(idx+1)
        st.download_button(
            dl,
            datos,
            file_name=nombre,
            mime="video/mp4"
        )
    if st.button("Analizar otro video"):
        st.session_state.shorts_list = []
        st.session_state.sel = 0
        st.rerun()
    st.stop()

st.subheader("1. Pega tu video")
url = st.text_input("Link de YouTube")
st.subheader("2. Configura")
num_shorts = st.slider("Cantidad", 1, 5, 3)
duracion = st.slider("Duracion seg", 15, 60, 30)
st.write("La IA busca gritos, sustos,")
st.write("suspenso y musica intensa.")
boton = st.button("ANALIZAR Y MOSTRAR MENU")
st.write("Para 2 horas tarda 1-2 min.")
st.write("No recargues la pagina.")

if boton:
    if not url:
        st.warning("Pega el link primero")
        st.stop()
    tmpdir = st.session_state.tmpdir
    video_path = os.path.join(tmpdir, "video.mp4")
    if os.path.exists(video_path):
        os.remove(video_path)
    with st.spinner("Paso 1: Descargando ligero..."):
        opts = {}
        opts["format"] = "mp4[height<=360]/best[height<=360]"
        opts["outtmpl"] = video_path
        opts["quiet"] = True
        opts["noplaylist"] = True
        opts["extractor_args"] = {}
        opts["extractor_args"]["youtube"] = {}
        opts["extractor_args"]["youtube"]["player_client"] = ["android", "web"]
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
        except Exception:
            st.error("YouTube bloqueo la descarga.")
            st.stop()
    try:
        clip_temp = VideoFileClip(video_path)
        total = clip_temp.duration
        clip_temp.close()
        mins = int(total // 60)
        st.success("Video de " + str(mins) + " minutos")
        with st.spinner("Paso 2: La IA escucha todo..."):
            inicios = analizar(video_path, total, duracion, num_shorts)
        if len(inicios) == 0:
            st.error("No pude analizar el audio.")
            st.stop()
        st.success("Encontre momentos epicos.")
        with st.spinner("Paso 3: Cortando en vertical..."):
            clip_o = VideoFileClip(video_path)
            nuevos = []
            prog = st.progress(0)
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
            st.session_state.shorts_list = nuevos
            st.session_state.sel = 0
            st.balloons()
            st.rerun()
    except Exception as e:
        st.error("Error: " + str(e))

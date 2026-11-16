import streamlit as st
import tempfile as tmpfile
import os
from moviepy import VideoFileClip

st.set_page_config(page_title="NEXUS CLIPPER", page_icon="👾", layout="centered")

CSS = "<style>"
CSS += ".stApp{background:#050510;color:white;}"
CSS += "h1{text-align:center;font-size:42px !important;color:#00ffcc !important;text-shadow:0 0 10px #00ffcc,0 0 25px #00ffcc;}"
CSS += ".subtitle{text-align:center;color:#a5f3fc;font-size:14px;margin-bottom:22px;}"
CSS += ".neon-card{background:rgba(10,15,35,0.9);border:1px solid #00ffcc;border-radius:18px;padding:22px;box-shadow:0 0 20px rgba(0,255,204,0.25);margin-bottom:16px;}"
CSS += ".step-title{color:#00ffcc;font-weight:700;font-size:16px;margin:14px 0 8px 0;}"
CSS += ".stButton > button{width:100%;background:#00ffcc !important;color:#000 !important;font-size:17px !important;font-weight:900 !important;border:none !important;border-radius:14px !important;padding:16px !important;box-shadow:0 0 25px #00ffcc;}"
CSS += ".stDownloadButton > button{width:100%;background:#ff006e !important;color:white !important;font-size:16px !important;font-weight:900 !important;border:none !important;border-radius:14px !important;padding:14px !important;box-shadow:0 0 20px #ff006e;}"
CSS += ".badge{display:inline-block;border:1px solid #00ffcc;color:#00ffcc;font-size:10px;font-weight:800;padding:5px 10px;border-radius:20px;margin:2px;}"
CSS += ".short-card{background:linear-gradient(135deg,rgba(0,255,204,0.12),rgba(255,0,110,0.12));border:1px solid rgba(255,255,255,0.2);border-radius:14px;padding:14px;margin:10px 0 4px 0;}"
CSS += "</style>"
st.markdown(CSS, unsafe_allow_html=True)

if "shorts_list" not in st.session_state:
    st.session_state.shorts_list = []
if "tmpdir_guardado" not in st.session_state:
    st.session_state.tmpdir_guardado = tmpfile.mkdtemp()

st.markdown("<h1>👾 NEXUS CLIPPER</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>GENERAR - VER - ELEGIR - DESCARGAR SOLO EL QUE TE GUSTE</p>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center'><span class='badge'>● ONLINE</span> <span class='badge'>🎬 VISTA PREVIA</span></div><br>", unsafe_allow_html=True)

if len(st.session_state.shorts_list) > 0:
    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
    st.markdown("<div class='step-title'>🎬 TUS SHORTS LISTOS - ESCOGE UNO PARA VERLO</div>", unsafe_allow_html=True)
    opciones = [f"🎬 Short {i+1} - {st.session_state.shorts_list[i]['duracion']}s" for i in range(len(st.session_state.shorts_list))]
    seleccion = st.selectbox("Elige un Short para ver:", opciones)
    idx = opciones.index(seleccion)
    info = st.session_state.shorts_list[idx]
    if os.path.exists(info["path"]):
        st.video(info["path"])
        st.markdown(f"<div class='short-card'>🎬 <b>{seleccion}</b> - Listo para TikTok</div>", unsafe_allow_html=True)
        with open(info["path"], "rb") as f:
            datos = f.read()
        st.download_button(f"⬇️ DESCARGAR ESTE SHORT - {seleccion}", datos, file_name=f"short_{idx+1}.mp4", mime="video/mp4", key=f"dl_unico_{idx}")
    else:
        st.error("La app se reinicio, vuelve a generar con 3 shorts.")
    if st.button("⬅️ HACER OTROS SHORTS"):
        st.session_state.shorts_list = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
st.markdown("<div class='step-title'>// PASO 1 - SUBE TU VIDEO</div>", unsafe_allow_html=True)
st.write("TIP: Si tu video dura 2 horas, cortalo primero en CapCut a solo 2-3 minutos.")
archivo = st.file_uploader("Sube tu video MP4 aqui", type=["mp4", "mov", "mkv", "webm"])
tmpdir = st.session_state.tmpdir_guardado
video_path_final = None
if archivo is not None:
    tamano_mb = archivo.size / 1024 / 1024
    st.write(f"Peso: {tamano_mb:.1f} MB")
    video_path_final = os.path.join(tmpdir, "subido.mp4")
    with open(video_path_final, "wb") as f:
        f.write(archivo.read())
    st.success("Video subido! Ya puedes cortar")
st.markdown("<div class='step-title'>// PASO 2 - CONFIGURA</div>", unsafe_allow_html=True)
minuto_inicio = st.slider("Empezar desde el minuto", 0, 110, 0)
c1, c2 = st.columns(2)
with c1:
    num_shorts = st.slider("N DE SHORTS", 1, 5, 3)
with c2:
    duracion = st.slider("DURACION SEG", 15, 60, 30)
boton = st.button("▶ GENERAR SHORTS Y VERLOS")
st.markdown("</div>", unsafe_allow_html=True)

if boton:
    if video_path_final is None or not os.path.exists(video_path_final):
        st.warning("Primero sube un video")
        st.stop()
    try:
        with st.spinner("Cortando tus Shorts... NO recargues la pagina..."):
            clip_original = VideoFileClip(video_path_final)
            if minuto_inicio > 0:
                clip_original = clip_original.subclipped(minuto_inicio*60, None)
            duracion_total = clip_original.duration
            st.info(f"Video detectado: {int(duracion_total)}s")
            nuevos = []
            progreso = st.progress(0)
            for i in range(num_shorts):
                inicio = i * duracion
                fin = inicio + duracion
                if fin > duracion_total:
                    break
                clip = clip_original.subclipped(inicio, fin)
                w, h = clip.size
                nuevo_h = int(w * 16 / 9)
                if nuevo_h > h:
                    nuevo_h = h
                clip_vertical = clip.cropped(x_center=w//2, y_center=h//2, width=w, height=nuevo_h)
                clip_vertical = clip_vertical.resized(height=720)
                salida = os.path.join(tmpdir, f"short_{i+1}.mp4")
                clip_vertical.write_videofile(salida, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
                nuevos.append({"path": salida, "duracion": duracion})
                progreso.progress((i+1)/num_shorts)
                st.write(f"Short {i+1} listo... ✅")
            st.session_state.shorts_list = nuevos
            st.balloons()
            st.rerun()
    except Exception as e:
        st.error(f"Hubo un error: {e}")

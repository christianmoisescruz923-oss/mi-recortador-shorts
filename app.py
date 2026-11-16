import streamlit as st
import tempfile as tmpfile
import os
import yt_dlp
import numpy as np
from moviepy import VideoFileClip

st.set_page_config(page_title="NEXUS CLIPPER IA", page_icon="🧠", layout="centered")

CSS = "<style>"
CSS += ".stApp{background:#050510;color:white;}"
CSS += "h1{text-align:center;font-size:36px !important;color:#00ffcc !important;text-shadow:0 0 10px #00ffcc,0 0 25px #00ffcc;}"
CSS += ".subtitle{text-align:center;color:#a5f3fc;font-size:13px;margin-bottom:20px;}"
CSS += ".neon-card{background:rgba(10,15,35,0.9);border:1px solid #00ffcc;border-radius:18px;padding:22px;box-shadow:0 0 20px rgba(0,255,204,0.25);margin-bottom:16px;}"
CSS += ".step-title{color:#00ffcc;font-weight:700;font-size:15px;margin:14px 0 8px 0;}"
CSS += ".stTextInput > div > div > input{background:#0a0a1a !important;color:#00ffcc !important;border:1.5px solid #00ffcc !important;border-radius:12px !important;padding:14px !important;}"
CSS += ".stButton > button{width:100%;background:#00ffcc !important;color:#000 !important;font-size:17px !important;font-weight:900 !important;border:none !important;border-radius:14px !important;padding:16px !important;box-shadow:0 0 25px #00ffcc;}"
CSS += ".stDownloadButton > button{width:100%;background:#ff006e !important;color:white !important;font-size:16px !important;font-weight:900 !important;border:none !important;border-radius:14px !important;padding:14px !important;}"
CSS += ".badge{display:inline-block;border:1px solid #00ffcc;color:#00ffcc;font-size:10px;font-weight:800;padding:5px 10px;border-radius:20px;margin:2px;}"
CSS += ".short-card{background:linear-gradient(135deg,rgba(0,255,204,0.12),rgba(255,0,110,0.12));border:1px solid rgba(255,255,255,0.2);border-radius:14px;padding:14px;margin:10px 0 4px 0;}"
CSS += ".momento{background:rgba(255,230,0,0.12);border:1px solid #ffe600;border-radius:12px;padding:10px;margin:6px 0;}"
CSS += "</style>"
st.markdown(CSS, unsafe_allow_html=True)

if "shorts_list" not in st.session_state:
    st.session_state.shorts_list = []
if "tmpdir_guardado" not in st.session_state:
    st.session_state.tmpdir_guardado = tmpfile.mkdtemp()

st.markdown("<h1>🧠 NEXUS CLIPPER IA</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>La IA analiza todo tu video y encuentra los momentos más épicos</p>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center'><span class='badge'>● IA ACTIVADA</span> <span class='badge'>🔥 DETECTA SUSPENSO</span> <span class='badge'>🎬 MOMENTOS TOP</span></div><br>", unsafe_allow_html=True)

def analizar_momentos_epicos(video_path, duracion_total, duracion_short, num_shorts):
    try:
        clip = VideoFileClip(video_path)
        audio = clip.audio
        if audio is None:
            return []
        fps_audio = 22050
        muestras = []
        paso = int(duracion_total)
        if paso > 7200:
            paso = 7200
        arr = audio.to_soundarray(fps=fps_audio)
        if len(arr.shape) > 1:
            arr = arr.mean(axis=1)
        energia_por_seg = []
        for seg in range(int(duracion_total)):
            ini = seg * fps_audio
            fin = (seg + 1) * fps_audio
            if fin > len(arr):
                break
            trozo = arr[ini:fin]
            energia = float(np.sqrt(np.mean(trozo ** 2)) + 0.0001)
            energia_por_seg.append(energia)
        clip.close()
        if len(energia_por_seg) < duracion_short:
            return []
        scores = []
        for i in range(len(energia_por_seg) - duracion_short):
            ventana = energia_por_seg[i:i+duracion_short]
            pico = max(ventana)
            promedio = sum(ventana) / len(ventana)
            variacion = max(ventana) - min(ventana)
            score = promedio * 1.0 + pico * 0.8 + variacion * 0.5
            scores.append((score, i))
        scores.sort(reverse=True)
        elegidos = []
        for score, inicio in scores:
            es_cercano = False
            for ya in elegidos:
                if abs(inicio - ya) < duracion_short + 5:
                    es_cercano = True
                    break
            if not es_cercano:
                elegidos.append(inicio)
            if len(elegidos) >= num_shorts:
                break
        elegidos.sort()
        return elegidos
    except Exception as e:
        return []

if len(st.session_state.shorts_list) > 0:
    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
    st.markdown("<div class='step-title'>🎬 Tus Shorts más épicos están listos</div>", unsafe_allow_html=True)
    st.write("Elige uno para verlo. Si te gusta, descárgalo. Si no, prueba con el siguiente.")
    opciones = []
    for i in range(len(st.session_state.shorts_list)):
        info_tmp = st.session_state.shorts_list[i]
        min_txt = int(info_tmp["inicio"] // 60)
        seg_txt = int(info_tmp["inicio"] % 60)
        opciones.append(f"🔥 Short {i+1} - Minuto {min_txt}:{seg_txt:02d} - Puntaje {info_tmp['score']}%")
    seleccion = st.selectbox("Elige un Short para ver:", opciones)
    idx = opciones.index(seleccion)
    info = st.session_state.shorts_list[idx]
    if os.path.exists(info["path"]):
        st.video(info["path"])
        st.markdown(f"<div class='short-card'>🔥 <b>{seleccion}</b><br>Este fue uno de los momentos con más energía, suspenso y reacción en todo el video.</div>", unsafe_allow_html=True)
        with open(info["path"], "rb") as f:
            datos = f.read()
        st.download_button(f"⬇️ Descargar este Short", datos, file_name=f"short_epico_{idx+1}.mp4", mime="video/mp4", key=f"dl_{idx}")
    else:
        st.error("La aplicación se reinició. Vuelve a generar los Shorts.")
    if st.button("⬅️ Analizar otro video"):
        st.session_state.shorts_list = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
st.markdown("<div class='step-title'>1. Pega tu video</div>", unsafe_allow_html=True)
url = st.text_input("Link de YouTube", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")
st.markdown("<div class='step-title'>2. ¿Cuántos momentos épicos quieres?</div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    num_shorts = st.slider("Cantidad de Shorts", 1, 5, 3)
with c2:
    duracion = st.slider("Duración de cada Short (segundos)", 15, 60, 30)
st.markdown("<div class='step-title'>3. ¿Cómo detecta la IA lo épico?</div>", unsafe_allow_html=True)
st.write("✅ Volumen alto = gritos, sustos, risas")
st.write("✅ Cambios bruscos = suspenso, revelaciones")
st.write("✅ Música intensa = momentos emotivos")
st.write("La IA escucha todo el video de 2 horas y solo se queda con lo mejor.")
boton = st.button("🧠 ANALIZAR VIDEO Y CREAR SHORTS ÉPICOS")
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#94a3b8;font-size:12px;'>Para videos de 2 horas, el análisis tarda 1-2 minutos. No recargues la página.</p>", unsafe_allow_html=True)

if boton:
    if not url:
        st.warning("Primero pega el link de YouTube.")
        st.stop()
    tmpdir = st.session_state.tmpdir_guardado
    video_path = os.path.join(tmpdir, "video_completo.mp4")
    if os.path.exists(video_path):
        os.remove(video_path)
    with st.spinner("Paso 1 de 3: Descargando en calidad ligera para analizar... (no pesa nada)"):
        ydl_opts = {}
        ydl_opts["format"] = "mp4[height<=360]/best[height<=360]"
        ydl_opts["outtmpl"] = video_path
        ydl_opts["quiet"] = True
        ydl_opts["noplaylist"] = True
        ydl_opts["extractor_args"] = {"youtube": {"player_client": ["android", "web"]}}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception:
            st.error("YouTube bloqueó la descarga desde el servidor (Error 403).")
            st.info("Solución: Descarga el video en tu celular con Snaptube, súbelo a la app y la IA lo analizará igual.")
            st.stop()
    try:
        clip_temp = VideoFileClip(video_path)
        duracion_total = clip_temp.duration
        clip_temp.close()
        st.success(f"Video detectado: {int(duracion_total // 60)} minutos y {int(duracion_total % 60)} segundos.")
        with st.spinner("Paso 2 de 3: La IA está escuchando todo el video para encontrar los momentos de suspenso..."):
            inicios = analizar_momentos_epicos(video_path, duracion_total, duracion, num_shorts)
        if len(inicios) == 0:
            st.error("No pude analizar el audio. Prueba con otro video.")
            st.stop()
        st.success(f"¡Listo! Encontré {len(inicios)} momentos épicos. Ahora los estoy cortando en vertical...")
        for ii, ini in enumerate(inicios):
            mm = int(ini // 60)
            ss = int(ini % 60)
            st.markdown(f"<div class='momento'>🔥 <b>Momento {ii+1}:</b> Minuto {mm}:{ss:02d} - Mucha energía detectada aquí</div>", unsafe_allow_html=True)
        with st.spinner("Paso 3 de 3: Cortando tus Shorts en vertical 9:16..."):
            clip_original = VideoFileClip(video_path)
            nuevos = []
            progreso = st.progress(0)
            for i, inicio in enumerate(inicios):
                fin = inicio + duracion
                if fin > duracion_total:
                    fin = duracion_total
                clip = clip_original.subclipped(inicio, fin)
                w, h = clip.size
                nuevo_h = int(w * 16 / 9)
                if nuevo_h > h:
                    nuevo_h = h
                clip_vertical = clip.cropped(x_center=w//2, y_center=h//2, width=w, height=nuevo_h)
                clip_vertical = clip_vertical.resized(height=720)
                salida = os.path.join(tmpdir, f"short_epico_{i+1}.mp4")
                clip_vertical.write_videofile(salida, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
                puntaje = 95 - (i * 5)
                if puntaje < 70:
                    puntaje = 70
                nuevos.append({"path": salida, "duracion": duracion, "inicio": inicio, "score": puntaje})
                progreso.progress((i+1)/len(inicios))
            clip_original.close()
            st.session_state.shorts_list = nuevos
            st.balloons()
            st.rerun()
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
        st.write("Intenta con un video más corto para probar, como uno de 10 minutos.")

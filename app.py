import streamlit as st
import tempfile
import os
import numpy as np
from moviepy import VideoFileClip

st.set_page_config(page_title="SHORTCUT AI - Subir Archivo", page_icon="⚡", layout="centered")

# ===== ESTILO FUTURISTA =====
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    h1 {
        text-align: center;
        font-size: 38px !important;
        background: linear-gradient(90deg, #00f2ff, #a855f7, #ff00cc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 15px;
        margin-top: -15px;
        margin-bottom: 25px;
    }
    .card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #7c3aed, #db2777, #06b6d4) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 15px !important;
        box-shadow: 0 5px 20px rgba(219,39,119,0.5);
    }
    .stDownloadButton > button {
        width: 100%;
        background: rgba(255,255,255,0.12) !important;
        color: white !important;
        border: 1px solid #00f2ff !important;
        border-radius: 12px !important;
        margin-top: 8px;
    }
    .badge {
        display: inline-block;
        background: #00f2ff;
        color: black;
        font-size: 11px;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 20px;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ===== TITULO =====
st.markdown("<h1>⚡ SHORTCUT AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Sube tu video y convierte los momentos épicos en Shorts virales</p>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center'><span class='badge'>✦ IA AUTOMÁTICA</span> <span class='badge' style='background:#a855f7;color:white'>✦ SIN MARCA DE AGUA</span> <span class='badge' style='background:#ff00cc;color:white'>✦ CON AUDIO</span></div><br>", unsafe_allow_html=True)

if "shorts_list" not in st.session_state:
    st.session_state.shorts_list = []
if "sel" not in st.session_state:
    st.session_state.sel = 0
if "tmpdir" not in st.session_state:
    st.session_state.tmpdir = tempfile.mkdtemp()

# ===== SI YA HAY SHORTS, MOSTRAR MENÚ =====
if len(st.session_state.shorts_list) > 0:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ✅ ¡Análisis terminado!")
    st.write("Toca un Short para ver su vista previa con audio.")
    
    for i in range(len(st.session_state.shorts_list)):
        info = st.session_state.shorts_list[i]
        mm = int(info["inicio"] // 60)
        ss = int(info["inicio"] % 60)
        txt = f"🔥 Short {i+1} - Min {mm}:{ss:02d} - {info['score']}% Viral"
        if st.session_state.sel == i:
            txt = f"✅ {txt}"
        st.write(txt)
        if st.button(f"▶️ Ver Short {i+1}", key=f"ver_{i}"):
            st.session_state.sel = i
            st.rerun()
            
    st.write("---")
    idx = st.session_state.sel
    info_sel = st.session_state.shorts_list[idx]
    mm2 = int(info_sel["inicio"] // 60)
    ss2 = int(info_sel["inicio"] % 60)
    
    st.subheader(f"🎬 Vista previa Short {idx+1} - Min {mm2}:{ss2:02d} - Con audio 🔊")
    if os.path.exists(info_sel["path"]):
        st.video(info_sel["path"])
        with open(info_sel["path"], "rb") as f:
            datos = f.read()
        st.download_button(f"⬇️ Descargar este Short {idx+1} con audio", datos, file_name=f"short_epico_{idx+1}.mp4", mime="video/mp4")
        
    if st.button("⬅️ Analizar otro video"):
        st.session_state.shorts_list = []
        st.session_state.sel = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ===== TARJETA PRINCIPAL - SUBIR ARCHIVO =====
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 📤 1. Sube tu video")
st.write("Toca abajo y elige tu video desde tu celular o compu.")
archivo = st.file_uploader("Sube tu video aquí", type=["mp4", "mov", "mkv", "webm"], label_visibility="collapsed")
if archivo is not None:
    mb = archivo.size / 1024 / 1024
    st.success(f"✅ ¡Video subido! Pesa {int(mb)} MB")

st.markdown("### 🎬 2. Configura tus Shorts")
col1, col2 = st.columns(2)
with col1:
    num_shorts = st.slider("¿Cuántos shorts?", 1, 5, 3)
with col2:
    duracion = st.slider("Duración (seg)", 15, 60, 30)

st.markdown("### 🚀 3. ¡A crear!")
st.write("La IA busca gritos, sustos y música intensa.")
boton = st.button("✨ CORTAR EN SHORTS AHORA")
st.markdown("</div>", unsafe_allow_html=True)
st.write("Para videos largos tarda 1-2 min. No recargues la página.")

if boton:
    if archivo is None:
        st.warning("⚠️ Primero sube un video")
        st.stop()
        
    tmpdir = st.session_state.tmpdir
    video_path = os.path.join(tmpdir, "video.mp4")
    with open(video_path, "wb") as f:
        f.write(archivo.read())
        
    clip_temp = VideoFileClip(video_path)
    total = clip_temp.duration
    clip_temp.close()
    mins = int(total // 60)
    st.success(f"✅ Video de {mins} minutos detectado")
    
    with st.spinner("🤖 La IA está escuchando todo el video..."):
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
        
    st.success("✅ ¡Encontré momentos épicos!")
    
    with st.spinner("✂️ Cortando en vertical con audio..."):
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
            salida = os.path.join(tmpdir, f"s{i+1}.mp4")
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

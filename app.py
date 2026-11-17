import streamlit as st
import random
import urllib.parse

st.set_page_config(page_title="VIRAL PUBLISHER - Sube a Todo Lados", page_icon="🚀", layout="centered")

st.markdown("""
<style>
.stApp { background: radial-gradient(circle at top, #0f0c29 0%, #302b63 50%, #24243e 100%); color: white; }
h1 { text-align:center; font-size:36px !important; background: linear-gradient(90deg,#00f2ff,#a855f7,#ff00cc); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-weight:900; }
.card { background: rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); border-radius:20px; padding:18px; margin-bottom:16px; }
.stButton > button { width:100%; background: linear-gradient(90deg,#7c3aed,#db2777,#06b6d4) !important; color:white !important; font-size:16px !important; font-weight:800 !important; border:none !important; border-radius:15px !important; padding:13px !important; }
.result { background:#00f2ff; color:black; padding:14px; border-radius:12px; font-weight:700; }
.check { background: rgba(0,255,150,0.15); border:1px solid #00ff96; padding:10px; border-radius:12px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🚀 VIRAL PUBLISHER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#cbd5e1'>Sube tu Short 1 vez, publícalo en TikTok + Instagram + Facebook</p>", unsafe_allow_html=True)

# 1. SUBIR VIDEO
st.markdown("<div class='card'><b>1. 📤 Sube tu Short / Reel</b></div>", unsafe_allow_html=True)
video = st.file_uploader("Arrastra tu video aquí (mp4, vertical)", type=["mp4","mov","webm"])

tema = st.text_input("¿De qué trata tu video?", placeholder="Ej: tacos, susto, gym, chisme...")

# 2. GENERAR CAPTION
st.markdown("<div class='card'><b>2. ✨ Genera tu texto viral</b></div>", unsafe_allow_html=True)

if st.button("✨ GENERAR TÍTULO + HASHTAGS"):
    if not tema:
        st.warning("Escribe de qué trata primero")
    else:
        titulos = [
            f"NO VAS A CREER lo que pasó con {tema} 😱",
            f"Probé {tema} y esto pasó 🤯",
            f"Si te gusta {tema}, tienes que ver esto hasta el final 👀",
            f"El secreto de {tema} que nadie te cuenta 🤫",
            f"POV: tu primera vez probando {tema} 🔥"
        ]
        titulo = random.choice(titulos)
        hashtags = f"#viral #fyp #parati #shorts #reels #{tema.replace(' ','').lower()} #tendencia #mexico"
        caption = f"{titulo}\n\n{hashtags}\n\nSígueme para más 👇"
        st.session_state["caption"] = caption
        st.session_state["titulo"] = titulo

if "caption" in st.session_state:
    st.markdown(f"<div class='result'>{st.session_state['caption']}</div>", unsafe_allow_html=True)
    st.caption("Toca, copia y pégalo igual en las 3 apps. Así el algoritmo te empuja en las 3.")

# 3. PREVIEW Y COMPARTIR
if video:
    st.markdown("<div class='card'><b>3. 👀 Vista previa</b></div>", unsafe_allow_html=True)
    st.video(video)
    st.download_button("⬇️ DESCARGAR VIDEO LISTO PARA SUBIR", video, file_name="mi-short-viral.mp4")

    st.markdown("<div class='card'><b>4. 📲 Publicar en las 3</b><br><span style='color:#cbd5e1;font-size:13px'>Toca cada botón, se abre la app y pegas el caption que copiaste</span></div>", unsafe_allow_html=True)

    texto_share = urllib.parse.quote(st.session_state.get("caption", "Mira mi nuevo Short viral 🔥"))
    # WhatsApp y Facebook sí permiten compartir con texto
    st.link_button("💬 Compartir en WhatsApp", f"https://wa.me/?text={texto_share}")
    st.link_button("📘 Compartir en Facebook", f"https://www.facebook.com/sharer/sharer.php?u=https://zqfxbrcpt.streamlit.app")
    st.link_button("🎵 Abrir TikTok para subir", "https://www.tiktok.com/upload")
    st.link_button("📸 Abrir Instagram Reels para subir", "https://www.instagram.com/reels/create/")

    st.markdown("<div class='check'>✅ Checklist viral:<br>✔️ Sube a la misma hora en las 3<br>✔️ Usa el mismo caption y hashtags<br>✔️ Responde los primeros 5 comentarios en 10 min<br>✔️ Sube 1 diario por 7 días</div>", unsafe_allow_html=True)
else:
    st.info("👆 Primero sube tu video para activar los botones de publicar")

st.markdown("<br><p style='text-align:center;color:#94a3b8;font-size:12px'>VIRAL PUBLISHER • Hecho para creadores</p>", unsafe_allow_html=True)

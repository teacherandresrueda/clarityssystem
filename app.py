import streamlit as st
import random
from collections import Counter
from auth import *

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="RetroCore AI 💀", layout="wide")

# 🎨 estilo premium
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #020617);
}
h1, h2, h3 {
    color: #00ffcc;
}
</style>
""", unsafe_allow_html=True)

# ======================
# DB USERS
# ======================
crear_tabla()

# ======================
# SESSION
# ======================
if "login" not in st.session_state:
    st.session_state["login"] = False

# ======================
# LOGIN / REGISTRO
# ======================
if not st.session_state["login"]:

    st.title("🔥 RetroCore AI")

    menu = st.sidebar.selectbox("Acceso", ["Login", "Registro"])

    if menu == "Registro":
        user = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Crear cuenta"):
            registrar(user, password)
            st.success("Cuenta creada")

    elif menu == "Login":
        user = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Entrar"):
            if login(user, password):
                st.session_state["login"] = True
                st.rerun()
            else:
                st.error("Datos incorrectos")

# ======================
# SISTEMA PRINCIPAL
# ======================
else:

    st.sidebar.success("🟢 Sesión activa")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state["login"] = False
        st.rerun()

    st.title("🔥 RetroCore AI Premium")
    st.markdown("## 🧠 Sistema de análisis y generación estratégica")

    # ======================
    # DATA (puedes mejorar después)
    # ======================
    if "resultados" not in st.session_state:
        st.session_state.resultados = [
            {"fecha": "2026-04-04", "numeros": [7,12,22,31,37,38]},
            {"fecha": "2026-04-01", "numeros": [4,11,17,22,26,39]},
            {"fecha": "2026-03-28", "numeros": [13,14,24,29,31,35]},
        ]

    if "jugadas" not in st.session_state:
        st.session_state.jugadas = [
            {"fecha": "2026-04-04", "numeros": [7,12,22,31,37,47]},
            {"fecha": "2026-04-01", "numeros": [4,7,12,17,22,31]},
        ]

    # ======================
    # MENU PRO
    # ======================
    menu = st.sidebar.radio("🧠 Sistema", [
        "📊 Dashboard",
        "🧠 Generador",
        "💀 Top Jugada",
        "📈 Evidencia"
    ])

    # ======================
    # DASHBOARD
    # ======================
    if menu == "📊 Dashboard":

        st.subheader("📊 Rendimiento del sistema")

        total_aciertos = 0
        total = 0

        for o in st.session_state.resultados:
            for j in st.session_state.jugadas:
                if o["fecha"] == j["fecha"]:

                    aciertos = set(o["numeros"]) & set(j["numeros"])
                    total_aciertos += len(aciertos)
                    total += 1

                    st.markdown(f"### 📅 {o['fecha']}")

                    cols = st.columns(6)
                    for i, n in enumerate(o["numeros"]):
                        color = "green" if n in aciertos else "gray"
                        cols[i].markdown(f":{color}[{n}]")

        if total > 0:
            st.metric("Promedio de aciertos", round(total_aciertos/total,2))

    # ======================
    # GENERADOR
    # ======================
    elif menu == "🧠 Generador":

        st.subheader("🧠 Generador basado en tu patrón")

        base = [7,22,31]

        for i in range(3):
            j = set(base)

            while len(j) < 6:
                j.add(random.randint(1,39))

            cols = st.columns(6)
            for idx, num in enumerate(sorted(j)):
                cols[idx].markdown(f"🔥 **{num}**")

    # ======================
    # TOP JUGADA
    # ======================
    elif menu == "💀 Top Jugada":

        resultados = st.session_state.resultados

        freq = Counter([n for r in resultados for n in r["numeros"]])
        mejor = sorted([n for n,_ in freq.most_common(6)])

        st.markdown("## 💀 Jugada Estratégica")

        cols = st.columns(6)
        for i, num in enumerate(mejor):
            cols[i].markdown(f":green[**{num}**]")

    # ======================
    # EVIDENCIA
    # ======================
    elif menu == "📈 Evidencia":

        st.subheader("📈 Evidencia del sistema")

        historial = []

        for o in st.session_state.resultados:
            for j in st.session_state.jugadas:
                if o["fecha"] == j["fecha"]:
                    aciertos = len(set(o["numeros"]) & set(j["numeros"]))
                    historial.append(aciertos)

        if historial:
            st.line_chart(historial)

            st.metric("Mejor resultado", max(historial))
            st.metric("Promedio", round(sum(historial)/len(historial),2))

            st.markdown("### 📊 Interpretación")

            if sum(historial)/len(historial) >= 3:
                st.success("Sistema consistente 🔥")
            else:
                st.warning("Sistema en ajuste ⚠️")

        else:
            st.warning("Sin datos suficientes")

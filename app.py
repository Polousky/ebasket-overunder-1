import streamlit as st
import pandas as pd

st.set_page_config(page_title="Over/Under eBasket - Descanso", layout="centered")
st.title("🏀 Bot Over/Under eBasket (Descanso)")

# === 1. CONTEXTO DEL PARTIDO ===
st.header("📌 Contexto del partido")

favorito_pre = st.selectbox("¿Quién era el favorito prepartido?", ["Equipo 1", "Equipo 2", "Parejo"])
favorito_descanso = st.selectbox("¿Quién va ganando al descanso?", ["Equipo 1", "Equipo 2", "Empate"])

# === 2. PUNTOS POR EQUIPO Y CUARTO ===
st.header("📊 Puntos por equipo (1er y 2º cuarto)")

eq1_q1 = st.number_input("Equipo 1 - Q1", min_value=0)
eq1_q2 = st.number_input("Equipo 1 - Q2", min_value=0)
eq2_q1 = st.number_input("Equipo 2 - Q1", min_value=0)
eq2_q2 = st.number_input("Equipo 2 - Q2", min_value=0)

# === 3. LÍNEAS DE APUESTA ===
st.header("📉 Líneas de apuesta")

linea_inicial = st.number_input("Línea Over/Under inicial (prepartido)", min_value=0.0, step=0.5)
linea_actual = st.number_input("Línea Over/Under actual (en vivo)", min_value=0.0, step=0.5)

# === 4. ANÁLISIS ===
if st.button("🔍 Analizar partido"):
    eq1_total = eq1_q1 + eq1_q2
    eq2_total = eq2_q1 + eq2_q2
    total_puntos = eq1_total + eq2_total

    prom_q_eq1 = eq1_total / 2
    prom_q_eq2 = eq2_total / 2
    ritmo_proyectado = (prom_q_eq1 + prom_q_eq2) * 4

    st.markdown("---")
    st.subheader("📈 Análisis automático")

    st.metric("Total puntos al descanso", total_puntos)
    st.metric("Ritmo proyectado", f"{ritmo_proyectado:.1f}")
    st.metric("Prom. por cuarto Equipo 1", f"{prom_q_eq1:.1f}")
    st.metric("Prom. por cuarto Equipo 2", f"{prom_q_eq2:.1f}")
    st.metric("Línea inicial", f"{linea_inicial}")
    st.metric("Línea actual", f"{linea_actual}")

    margen = abs(eq1_total - eq2_total)

    if ritmo_proyectado > linea_actual and linea_actual < linea_inicial - 5:
        if favorito_pre != favorito_descanso:
            st.success("🔥 OVER con valor: ritmo alto + posible remontada")
        else:
            st.info("📈 OVER posible: ritmo fuerte y línea bajada")
    elif ritmo_proyectado < linea_actual and linea_actual > linea_inicial + 5:
        if favorito_pre == favorito_descanso and margen > 10:
            st.warning("❄️ UNDER con valor: favorito dominante + ritmo bajo")
        else:
            st.info("📉 UNDER moderado: ritmo bajo y línea alta")
    else:
        st.info("🤔 No hay señal clara según ritmo y contexto actual.")

# === 5. HISTORIAL DE APUESTAS ===
st.markdown("---")
st.header("📋 Registro de apuestas")

if "historial" not in st.session_state:
    st.session_state.historial = []

with st.form("registro"):
    prediccion = st.selectbox("Predicción realizada", ["Over", "Under"])
    cuota = st.number_input("Cuota apostada", value=1.80, step=0.01)
    resultado = st.selectbox("¿Fue correcta?", ["Sí", "No"])
    guardar = st.form_submit_button("💾 Guardar resultado")

    if guardar:
        st.session_state.historial.append({
            "Predicción": prediccion,
            "Cuota": cuota,
            "Correcta": resultado == "Sí"
        })
        st.success("✅ Resultado guardado")

# Mostrar historial
if st.session_state.historial:
    df = pd.DataFrame(st.session_state.historial)
    st.dataframe(df)

    total = len(df)
    aciertos = df["Correcta"].sum()
    winrate = aciertos / total * 100
    beneficio = sum(
        (row["Cuota"] - 1 if row["Correcta"] else -1)
        for _, row in df.iterrows()
    )
    roi = beneficio / total * 100

    st.subheader("📊 Estadísticas del bot")
    st.write(f"🔢 Apuestas totales: {total}")
    st.write(f"✅ Aciertos: {aciertos} ({winrate:.1f}%)")
    st.write(f"💰 Beneficio total: {beneficio:.2f} unidades")
    st.write(f"📈 ROI: {roi:.1f}%")

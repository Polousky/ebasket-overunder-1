import streamlit as st
import pandas as pd

st.set_page_config(page_title="Over/Under eBasket - Q3+", layout="centered")
st.title("🏀 Bot Over/Under eBasket (Desde 3er Cuarto)")

# === 1. CONTEXTO DEL PARTIDO ===
st.header("📌 Contexto del partido")

favorito_pre = st.selectbox("¿Quién era el favorito prepartido?", ["Equipo 1", "Equipo 2", "Parejo"])
favorito_descanso = st.selectbox("¿Quién va ganando al descanso?", ["Equipo 1", "Equipo 2", "Empate"])

# === 2. PUNTOS POR CUARTO ===
st.header("📊 Puntos por cuarto")

q1 = st.number_input("Puntos en Q1", min_value=0)
q2 = st.number_input("Puntos en Q2", min_value=0)
q3 = st.number_input("Puntos en Q3", min_value=0)
q4 = st.number_input("Puntos en Q4", min_value=0)

# === 3. LÍNEAS DE APUESTA ===
st.header("📉 Líneas de apuesta")

linea_inicial = st.number_input("Línea Over/Under inicial (prepartido)", min_value=0.0, step=0.5)
linea_actual = st.number_input("Línea Over/Under actual (en vivo)", min_value=0.0, step=0.5)

# === 4. MARCADOR ACTUAL ===
st.header("🏁 Marcador actual")

eq1 = st.number_input("Puntos equipo 1", min_value=0)
eq2 = st.number_input("Puntos equipo 2", min_value=0)

# === 5. ANÁLISIS ===
if st.button("🔍 Analizar partido"):
    puntos_totales = q1 + q2 + q3 + q4
    cuartos_jugados = 2 + int(q3 > 0) + int(q4 > 0)
    ritmo_proyectado = (puntos_totales / cuartos_jugados) * 4 if cuartos_jugados > 0 else 0
    marcador_igualado = abs(eq1 - eq2) <= 5
    st.markdown("---")
    st.subheader("📈 Análisis automático")

    st.metric("Puntos totales", f"{puntos_totales}")
    st.metric("Cuartos jugados", f"{cuartos_jugados}/4")
    st.metric("Ritmo proyectado", f"{ritmo_proyectado:.1f}")
    st.metric("Línea inicial", f"{linea_inicial}")
    st.metric("Línea actual", f"{linea_actual}")

    # Reglas de decisión
    if ritmo_proyectado > linea_actual and linea_actual < linea_inicial - 5:
        if favorito_pre != favorito_descanso:
            st.success("🔥 OVER con valor: posible remontada o ritmo alto inesperado")
        else:
            st.info("📈 OVER posible: ritmo fuerte, partido dentro de guión")
    elif ritmo_proyectado < linea_actual and linea_actual > linea_inicial + 5:
        if favorito_pre == favorito_descanso and not marcador_igualado:
            st.warning("❄️ UNDER con valor: favorito dominante, ritmo bajo")
        else:
            st.info("📉 UNDER moderado: ritmo lento y línea alta")
    else:
        st.info("🤔 No hay señal clara según ritmo y contexto actual.")

# === 6. HISTORIAL DE APUESTAS ===
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

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Over/Under eBasket Pro", layout="centered")
st.title("🏀 Bot Over/Under eBasket Avanzado")

# Inputs del partido
st.header("📊 Datos del partido en vivo")

cuarto = st.radio("Cuarto actual", [1, 2, 3, 4], horizontal=True)
minuto = st.slider("Minuto del cuarto", 0.0, 5.0, 2.5, 0.1)

# Puntos por cuarto
q1 = st.number_input("Puntos en Q1", min_value=0)
q2 = st.number_input("Puntos en Q2", min_value=0)
q3 = st.number_input("Puntos en Q3", min_value=0) if cuarto >= 3 else 0
q4 = st.number_input("Puntos en Q4", min_value=0) if cuarto == 4 else 0

# Líneas
linea_inicial = st.number_input("📉 Línea Over/Under inicial", min_value=0.0, step=0.5)
linea_actual = st.number_input("📈 Línea actual en vivo", min_value=0.0, step=0.5)

# Marcador
eq1 = st.number_input("Puntos equipo 1", min_value=0)
eq2 = st.number_input("Puntos equipo 2", min_value=0)

# Botón de análisis
if st.button("🔍 Analizar partido"):
    total = eq1 + eq2
    jugados = (cuarto - 1) * 5 + minuto
    ritmo_proyectado = (total / jugados) * 20 if jugados > 0 else 0
    marcador_igualado = abs(eq1 - eq2) <= 5

    st.markdown("---")
    st.subheader("📈 Análisis automático")
    st.metric("Minutos jugados", f"{jugados:.1f}/20")
    st.metric("Total actual", f"{total} puntos")
    st.metric("Ritmo proyectado", f"{ritmo_proyectado:.1f}")
    st.metric("Línea inicial", f"{linea_inicial}")
    st.metric("Línea actual", f"{linea_actual}")

    # Evaluación
    if ritmo_proyectado > linea_actual and linea_actual < linea_inicial - 5 and marcador_igualado:
        st.success("🔥 OVER con valor detectado")
    elif ritmo_proyectado < linea_actual and linea_actual > linea_inicial + 5 and not marcador_igualado:
        st.warning("❄️ UNDER con valor detectado")
    else:
        st.info("🤔 Partido dentro de ritmo esperado. No hay valor claro.")

# REGISTRO HISTÓRICO
st.markdown("---")
st.header("📋 Registro de apuestas")

# Inicializa historial
if "historial" not in st.session_state:
    st.session_state.historial = []

# Formulario
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

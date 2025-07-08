import streamlit as st

st.set_page_config(page_title="Over/Under eBasket Pro", layout="centered")

st.title("🏀 Bot Avanzado Over/Under eBasket")

# Entradas principales
cuarto = st.radio("Cuarto actual", [1, 2, 3, 4], horizontal=True)
minuto = st.slider("Minuto del cuarto", 0.0, 5.0, 2.5, 0.1)
eq1 = st.number_input("Puntos equipo 1", min_value=0)
eq2 = st.number_input("Puntos equipo 2", min_value=0)
linea = st.number_input("Línea Over/Under actual", min_value=0.0, step=0.5)
puntos_2min = st.number_input("Puntos totales hace 2 minutos", min_value=0)

# Datos adicionales para afinar
prom_eq1 = st.number_input("Promedio puntos equipo 1 por partido", min_value=0)
prom_eq2 = st.number_input("Promedio puntos equipo 2 por partido", min_value=0)
racha = st.selectbox("¿Hay una racha reciente?", ["Ninguna", "5-0", "8-2", "10-3", "Otro"])

if st.button("📊 Analizar partido"):
    jugados = (cuarto - 1) * 5 + minuto
    total = eq1 + eq2
    ritmo_proyectado = (total / jugados) * 20 if jugados > 0 else 0
    ritmo_2min = (total - puntos_2min) / 2
    promedio_total = (prom_eq1 + prom_eq2) / 2 if (prom_eq1 + prom_eq2) > 0 else 0
    diff = ritmo_proyectado - linea
    marcador_igualado = abs(eq1 - eq2) <= 5

    st.markdown("---")
    st.metric("Minutos jugados", f"{jugados:.1f}/20")
    st.metric("Total actual", f"{total} puntos")
    st.metric("Ritmo proyectado", f"{ritmo_proyectado:.1f}")
    st.metric("Ritmo últimos 2min", f"{ritmo_2min:.1f}")
    st.metric("Promedio esperado", f"{promedio_total:.1f}")

    # Evaluación final
    if diff > 8 and ritmo_2min >= 1.5 and marcador_igualado:
        reco = "🔥 Apuesta sugerida: OVER fuerte"
    elif diff < -8 and ritmo_2min <= 1 and not marcador_igualado:
        reco = "❄️ Apuesta sugerida: UNDER fuerte"
    else:
        reco = "🤔 No hay valor claro. Espera o busca mejor spot."

    st.success(reco)
    if racha != "Ninguna":
        st.info(f"📈 Racha detectada: {racha}")

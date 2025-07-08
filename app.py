import streamlit as st

st.set_page_config(page_title="Bot Over/Under eBasket", layout="centered")

st.title("🏀 Bot Over/Under eBasket")
st.markdown("Introduce los datos del partido en directo:")

cuarto = st.radio("Cuarto actual", [1, 2, 3, 4], horizontal=True)
minuto = st.slider("Minuto del cuarto", 0.0, 5.0, 2.5, 0.1)
eq1 = st.number_input("Puntos equipo 1", min_value=0, step=1)
eq2 = st.number_input("Puntos equipo 2", min_value=0, step=1)
puntos_2min = st.number_input("Puntos totales hace 2 minutos", min_value=0, step=1)
linea = st.number_input("Línea Over/Under actual", min_value=0.0, step=0.5)

if st.button("📊 Analizar partido"):
    jugados = (cuarto - 1) * 5 + minuto
    total = eq1 + eq2
    ritmo = (total / jugados) * 20 if jugados > 0 else 0
    ritmo_2min = (total - puntos_2min) / 2
    dif = abs(eq1 - eq2)
    igualado = dif <= 5
    tendencia = "↑" if ritmo_2min >= 1.5 else "↓" if ritmo_2min <= 1 else "→"
    diff = ritmo - linea

    if diff > 10 and ritmo_2min >= 1.5 and igualado:
        reco = f"🔥 OVER fuerte (+{diff:.1f}, tendencia {tendencia})"
    elif diff > 5:
        reco = f"👍 OVER posible (+{diff:.1f}, tendencia {tendencia})"
    elif diff < -10 and ritmo_2min <= 1:
        reco = f"❄️ UNDER fuerte ({diff:.1f}, tendencia {tendencia})"
    elif diff < -5:
        reco = f"👎 UNDER posible ({diff:.1f}, tendencia {tendencia})"
    else:
        reco = f"🤔 No hay valor claro ({diff:.1f}, tendencia {tendencia})"

    st.markdown("---")
    st.markdown(f"**Minutos jugados:** `{jugados:.1f} / 20`")
    st.markdown(f"**Total puntos:** `{total} ({eq1}-{eq2})`")
    st.markdown(f"**Ritmo proyectado:** `{ritmo:.1f}`")
    st.markdown(f"**Ritmo últimos 2min:** `{ritmo_2min:.1f}`")
    st.markdown(f"**Partido igualado:** {'✅ Sí' if igualado else '❌ No'} (dif: {dif})")
    st.success(f"👉 Recomendación: **{reco}**")

import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="SmartBalance AI", layout="centered")

st.title("💰 SmartBalance AI - Motor Financiero Avanzado")
st.write("Analiza tu situación, optimiza tu dinero y detecta fugas financieras")

# -----------------------
# INPUT
# -----------------------
st.header("📊 Ingresos y gastos")

ingresos = st.number_input("Ingresos mensuales (€)", value=2000)

st.subheader("🏠 Vivienda")
vivienda = st.number_input("Vivienda (alquiler/hipoteca)", value=800)

st.subheader("💸 Gastos generales")
deuda = st.number_input("Deuda", value=200)
alimentacion = st.number_input("Alimentación", value=300)
gasolina = st.number_input("Gasolina", value=120)
otros = st.number_input("Otros", value=200)

st.subheader("🧾 Facturas")
luz = st.number_input("Electricidad", value=60)
agua = st.number_input("Agua", value=25)
gas = st.number_input("Gas", value=30)
internet = st.number_input("Internet", value=35)
movil = st.number_input("Móvil", value=20)

st.subheader("🛡️ Seguros")
seguros = st.number_input("Seguros", value=80)

analizar = st.button("Analizar situación")

# -----------------------
# MOTOR FINANCIERO
# -----------------------
def motor_financiero():

    # ---------------- ACTUAL ----------------
    necesidades_actuales = (
        vivienda + deuda + alimentacion +
        luz + agua + gas + internet + movil + seguros
    )

    ocio_actual = gasolina + otros
    ahorro_actual = max(0, ingresos - (necesidades_actuales + ocio_actual))

    total_gastos = necesidades_actuales + ocio_actual

    ratio = total_gastos / ingresos if ingresos > 0 else 0
    ratio_deuda = deuda / ingresos if ingresos > 0 else 0

    # ---------------- BENCHMARK (IDEAL) ----------------
    necesidades_ideal = ingresos * 0.5
    ocio_ideal = ingresos * 0.3
    ahorro_ideal = ingresos * 0.2

    # ---------------- OPTIMIZACIÓN FACTURAS ----------------
    ahorro_facturas = 0

    if luz > 40:
        ahorro_facturas += (luz - 25) * 12

    if internet > 40:
        ahorro_facturas += (internet - 25) * 12

    if gas > 40:
        ahorro_facturas += (gas - 25) * 12

    if movil > 25:
        ahorro_facturas += (movil - 15) * 12

    # ---------------- OPTIMIZACIÓN DEUDA ----------------
    ahorro_deuda = 0
    if ratio_deuda > 0.3:
        ahorro_deuda = deuda * 0.2 * 12

    # ---------------- ESTADO OPTIMIZADO ----------------
    ahorro_total_posible = ahorro_facturas + ahorro_deuda

    ingresos_optimizados = ingresos + (ahorro_total_posible / 12)

    necesidades_opt = max(0, necesidades_actuales - (ahorro_facturas / 12))
    ahorro_opt = ingresos * 0.2 + (ahorro_total_posible / 12)

    ocio_opt = ingresos_optimizados - necesidades_opt - ahorro_opt

    # ---------------- GAPS ----------------
    gap_ahorro = ahorro_ideal - ahorro_actual
    gap_necesidades = necesidades_actuales - necesidades_ideal

    return {
        "actual": (necesidades_actuales, ocio_actual, ahorro_actual),
        "ideal": (necesidades_ideal, ocio_ideal, ahorro_ideal),
        "opt": (necesidades_opt, ocio_opt, ahorro_opt),
        "gaps": (gap_ahorro, gap_necesidades),
        "ahorro_potencial": ahorro_total_posible,
        "ratio": ratio,
        "ratio_deuda": ratio_deuda
    }


# -----------------------
# EXPLICACIÓN IA
# -----------------------
def explicar_estado(data):

    ratio = data["ratio"]
    ahorro_gap, necesidades_gap = data["gaps"]

    if ratio > 0.6:
        return f"""
🚨 SITUACIÓN FINANCIERA AJUSTADA

Estás gastando un {round(ratio*100,1)}% de tus ingresos.

📉 Esto reduce tu capacidad de ahorro y te deja sin margen.

💸 Estás perdiendo aproximadamente {int(ahorro_gap)}€ de capacidad de ahorro mensual.

👉 Problema principal: estructura de gasto.
"""

    return f"""
✅ SITUACIÓN FINANCIERA ESTABLE

Tienes margen de maniobra financiero.

💡 Aun así, podrías optimizar hasta {int(data['ahorro_potencial']/12)}€ mensuales.

👉 Oportunidad: reducir fugas en facturas y deuda.
"""


# -----------------------
# RESULTADO
# -----------------------
if analizar:

    data = motor_financiero()

    actual = data["actual"]
    ideal = data["ideal"]
    opt = data["opt"]

    st.header("📊 Estado financiero")

    st.subheader("🔴 Estado actual")
    st.write(f"Necesidades: {int(actual[0])}€")
    st.write(f"Ocio: {int(actual[1])}€")
    st.write(f"Ahorro: {int(actual[2])}€")

    st.subheader("🟡 Estado ideal (benchmark)")
    st.write(f"Necesidades: {int(ideal[0])}€")
    st.write(f"Ocio: {int(ideal[1])}€")
    st.write(f"Ahorro: {int(ideal[2])}€")

    st.subheader("🟢 Estado optimizado (IA)")
    st.write(f"Necesidades: {int(opt[0])}€")
    st.write(f"Ocio: {int(opt[1])}€")
    st.write(f"Ahorro: {int(opt[2])}€")

    # -----------------------
    # GRÁFICO
    # -----------------------
    fig = go.Figure()

    fig.add_trace(go.Bar(name="Actual", x=["Necesidades","Ocio","Ahorro"], y=actual))
    fig.add_trace(go.Bar(name="Ideal", x=["Necesidades","Ocio","Ahorro"], y=ideal))
    fig.add_trace(go.Bar(name="Optimizado", x=["Necesidades","Ocio","Ahorro"], y=opt))

    st.plotly_chart(fig)

    # -----------------------
    # IA EXPLICATIVA
    # -----------------------
    st.subheader("🧠 Diagnóstico IA")
    st.info(explicar_estado(data))

    # -----------------------
    # ACCIONES
    # -----------------------
    st.header("💡 Acciones recomendadas")

    st.write(f"💰 Ahorro potencial total: {int(data['ahorro_potencial'])}€ / año")

    if luz > 40:
        st.link_button("🔌 Optimizar luz", "https://google.com")

    if internet > 40:
        st.link_button("🌐 Optimizar internet", "https://google.com")

    if gas > 40:
        st.link_button("🔥 Optimizar gas", "https://google.com")

    if movil > 25:
        st.link_button("📱 Optimizar móvil", "https://google.com")

    if data["ratio_deuda"] > 0.3:
        st.link_button("💳 Reducir deuda", "https://google.com")

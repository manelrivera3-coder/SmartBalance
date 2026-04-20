import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="SmartBalance AI", layout="centered")

st.title("💰 SmartBalance AI")
st.write("Analiza tu dinero, detecta problemas y optimiza tus gastos")

# -----------------------
# INPUT
# -----------------------
st.header("📊 Datos financieros")

ingresos = st.number_input("Ingresos mensuales (€)", min_value=0, value=2000)

st.subheader("🏠 Vivienda")
vivienda_tipo = st.selectbox("Tipo", ["Alquiler", "Hipoteca"])
vivienda = st.number_input("Pago vivienda", value=800)

st.subheader("💸 Gastos")
deuda = st.number_input("Deuda mensual", value=200)
alimentacion = st.number_input("Alimentación", value=300)
gasolina = st.number_input("Gasolina", value=120)
otros = st.number_input("Otros", value=200)

st.subheader("🧾 Facturas")
luz = st.number_input("Luz", value=60)
agua = st.number_input("Agua", value=25)
gas = st.number_input("Gas", value=30)
internet = st.number_input("Internet", value=35)

st.subheader("🛡️ Seguros")
seguros = st.number_input("Seguros totales (€)", value=80)

calcular = st.button("Analizar")

# -----------------------
# MOTOR IA
# -----------------------
def motor(ingresos, gastos):
    total = sum(gastos.values())
    libre = ingresos - total

    ratio = total / ingresos if ingresos > 0 else 0
    ratio_deuda = gastos["deuda"] / ingresos if ingresos > 0 else 0

    problemas = []

    if ratio > 0.6:
        problemas.append(("estructura", (ratio - 0.5) * ingresos, "Gastos demasiado altos"))

    if ratio_deuda > 0.3:
        problemas.append(("deuda", gastos["deuda"] * 0.2, "Deuda elevada"))

    if gastos["luz"] > 40:
        problemas.append(("luz", gastos["luz"] * 0.3, "Electricidad cara"))

    if gastos["internet"] > 40:
        problemas.append(("internet", gastos["internet"] * 0.4, "Internet caro"))

    if gastos["gas"] > 40:
        problemas.append(("gas", gastos["gas"] * 0.3, "Gas elevado"))

    if gastos["agua"] > 30:
        problemas.append(("agua", gastos["agua"] * 0.2, "Agua alta"))

    problemas = sorted(problemas, key=lambda x: x[1], reverse=True)

    return total, libre, ratio, ratio_deuda, problemas


# -----------------------
# EXPLICACIÓN IA
# -----------------------
def explicar(tipo, ratio, ratio_deuda):
    if tipo == "deuda":
        return f"Estás usando un {round(ratio_deuda*100,1)}% de ingresos en deuda. Nivel alto de riesgo financiero."
    if tipo == "estructura":
        return f"Estás gastando un {round(ratio*100,1)}% de tus ingresos. Muy ajustado."
    if tipo == "luz":
        return "Tu gasto en luz es superior a lo habitual. Probable sobrecoste en tarifa."


# -----------------------
# RESULTADO
# -----------------------
if calcular and ingresos > 0:

    gastos = {
        "vivienda": vivienda,
        "deuda": deuda,
        "alimentacion": alimentacion,
        "gasolina": gasolina,
        "luz": luz,
        "agua": agua,
        "gas": gas,
        "internet": internet,
        "seguros": seguros,
        "otros": otros
    }

    total, libre, ratio, ratio_deuda, problemas = motor(ingresos, gastos)

    st.header("📊 Resultado")

    st.write(f"💸 Gastos: {total}€")
    st.write(f"💰 Libre: {libre}€")
    st.write(f"📉 Ratio: {round(ratio*100,1)}%")

    # -----------------------
    # GRÁFICO
    # -----------------------
    st.subheader("📊 Distribución")

    fig = go.Figure(data=[go.Pie(labels=list(gastos.keys()), values=list(gastos.values()), hole=.4)])
    st.plotly_chart(fig)

    # -----------------------
    # 50/30/20
    # -----------------------
    st.subheader("📊 Regla 50/30/20")

    necesarios = vivienda + deuda + luz + agua + gas + internet + alimentacion + seguros
    ocio = gasolina + otros
    ahorro = ingresos - total

    st.write(f"Necesidades: {round(necesarios/ingresos*100)}%")
    st.write(f"Ocio: {round(ocio/ingresos*100)}%")
    st.write(f"Ahorro: {round(ahorro/ingresos*100)}%")

    # -----------------------
    # ANÁLISIS GLOBAL (FIX ERROR)
    # -----------------------
    def analisis_global():
        if libre < 0:
            return "🚨 Gastas más de lo que ingresas. Situación crítica."
        elif ratio > 0.6:
            return "⚠️ Gastos demasiado altos. Poco margen financiero."
        else:
            return "✅ Situación estable con margen de mejora."

    st.subheader("🧠 Análisis global")
    st.info(analisis_global())

    # -----------------------
    # FACTURAS (OPTIMIZACIÓN)
    # -----------------------
    st.subheader("💡 Optimización facturas")

    ahorro_facturas = 0

    if luz > 40:
        ahorro_facturas += (luz - 25) * 12
        st.write("💡 Luz: posible ahorro")

    if internet > 40:
        ahorro_facturas += (internet - 25) * 12
        st.write("🌐 Internet: posible ahorro")

    if gas > 40:
        ahorro_facturas += (gas - 25) * 12
        st.write("🔥 Gas: posible ahorro")

    if ahorro_facturas > 0:
        st.success(f"Ahorro estimado: {int(ahorro_facturas)}€/año")

    # -----------------------
    # SEGUROS
    # -----------------------
    st.subheader("🛡️ Seguros")

    if seguros > 60:
        st.warning("Seguros por encima de la media")
        st.write(f"💰 Posible ahorro: {int(seguros * 0.25 * 12)}€/año")
        st.link_button("Comparar seguros", "https://google.com")
    else:
        st.success("Seguros dentro de rango")

    # -----------------------
    # PROBLEMA PRINCIPAL
    # -----------------------
    if problemas:
        st.subheader("🚨 Problema principal")
        st.error(problemas[0][2])

        st.write(explicar(problemas[0][0], ratio, ratio_deuda))

    # -----------------------
    # PLAN ACCIÓN
    # -----------------------
    st.header("💡 Plan de acción")

    for p in problemas:
        if p[0] == "deuda":
            st.link_button("Mejorar deuda", "https://google.com")

        if p[0] == "luz":
            st.link_button("Reducir luz", "https://google.com")

        if p[0] == "internet":
            st.link_button("Mejorar internet", "https://google.com")

        if p[0] == "gas":
            st.link_button("Reducir gas", "https://google.com")

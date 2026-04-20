import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="SmartBalance AI", layout="centered")

st.title("💰 SmartBalance AI")
st.write("Detecta fugas de dinero y optimiza tus gastos con IA")

# -----------------------
# INPUT
# -----------------------
st.header("📊 Datos financieros")

ingresos = st.number_input("Ingresos mensuales (€)", min_value=0, value=2000)

st.subheader("🏠 Vivienda")
vivienda = st.number_input("Vivienda (alquiler/hipoteca)", value=800)

st.subheader("💸 Gastos")
deuda = st.number_input("Deuda mensual", value=200)
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

    # Facturas
    if luz > 40:
        problemas.append(("luz", luz * 0.3, "Electricidad cara"))

    if internet > 40:
        problemas.append(("internet", internet * 0.4, "Internet caro"))

    if gas > 40:
        problemas.append(("gas", gas * 0.3, "Gas elevado"))

    if movil > 25:
        problemas.append(("movil", movil * 0.4, "Móvil caro"))

    if agua > 30:
        problemas.append(("agua", agua * 0.2, "Agua alta"))

    return total, libre, ratio, ratio_deuda, sorted(problemas, key=lambda x: x[1], reverse=True)


# -----------------------
# IA EXPLICATIVA AVANZADA
# -----------------------
def explicar(tipo, ratio, ratio_deuda):
    if tipo == "deuda":
        return f"""
💳 DEUDA

Estás usando un {round(ratio_deuda*100,1)}% de tus ingresos en deuda.

📉 Por encima del 30–35% entras en riesgo financiero.

👉 Esto reduce tu capacidad de ahorro y te hace vulnerable.
"""

    if tipo == "luz":
        return """
💡 ELECTRICIDAD

Estás pagando por encima de la media.

🔍 Posibles causas:
- tarifa antigua
- potencia mal ajustada

💸 Ahorro potencial: 100–200€/año
"""

    if tipo == "internet":
        return """
🌐 INTERNET

Coste superior al mercado.

🔍 Causas habituales:
- permanencia antigua
- falta de revisión de tarifa

💸 Gasto innecesario mensual
"""

    if tipo == "gas":
        return """
🔥 GAS

Consumo por encima de lo esperado.

🔍 Posibles mejoras:
- revisión de tarifa
- cambio de comercializadora

💸 Ahorro anual posible significativo
"""

    if tipo == "movil":
        return """
📱 MÓVIL

Estás pagando más de lo necesario.

🔍 Normalmente ocurre por:
- tarifa antigua
- exceso de datos no usados

💸 Fácil ahorro mensual sin cambios de hábitos
"""

    if tipo == "agua":
        return """
🚰 AGUA

Consumo ligeramente elevado.

🔍 Posibles causas:
- hábitos domésticos
- tarifas no optimizadas
"""

    if tipo == "estructura":
        return f"""
🏠 ESTRUCTURA FINANCIERA

Estás gastando el {round(ratio*100,1)}% de tus ingresos.

📊 Lo recomendado es < 50%.

👉 Necesitas reducir gastos fijos o aumentar ingresos.
"""


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
        "movil": movil,
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

    necesarios = vivienda + deuda + luz + agua + gas + internet + movil + alimentacion + seguros
    ocio = gasolina + otros
    ahorro = ingresos - total

    st.write(f"Necesidades: {round(necesarios/ingresos*100)}%")
    st.write(f"Ocio: {round(ocio/ingresos*100)}%")
    st.write(f"Ahorro: {round(ahorro/ingresos*100)}%")

    # -----------------------
    # ANÁLISIS GLOBAL
    # -----------------------
    def analisis_global():
        if libre < 0:
            return "🚨 Gastas más de lo que ingresas"
        elif ratio > 0.6:
            return "⚠️ Situación ajustada"
        else:
            return "✅ Situación estable"

    st.subheader("🧠 Análisis global")
    st.info(analisis_global())

    # -----------------------
    # PROBLEMA PRINCIPAL
    # -----------------------
    if problemas:
        tipo = problemas[0][0]

        st.subheader("🚨 Problema principal")
        st.error(problemas[0][2])

        st.write(explicar(tipo, ratio, ratio_deuda))

    # -----------------------
    # PLAN DE ACCIÓN + MONETIZACIÓN
    # -----------------------
    st.header("💡 Optimización automática")

    for p in problemas:

        if p[0] == "luz":
            st.write("💡 Luz: posible ahorro")
            st.link_button("Comparar luz", "https://google.com")

        if p[0] == "internet":
            st.write("🌐 Internet: posible ahorro")
            st.link_button("Comparar internet", "https://google.com")

        if p[0] == "gas":
            st.write("🔥 Gas: posible ahorro")
            st.link_button("Comparar gas", "https://google.com")

        if p[0] == "movil":
            st.write("📱 Móvil: posible ahorro")
            st.link_button("Comparar móvil", "https://google.com")

        if p[0] == "agua":
            st.write("🚰 Agua: optimización posible")

        if p[0] == "deuda":
            st.write("💳 Refinanciar deuda")
            st.link_button("Mejorar deuda", "https://google.com")

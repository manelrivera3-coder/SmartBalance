import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="SmartBalance AI", layout="centered")

st.title("💰 SmartBalance AI")
st.write("Entiende por qué no llegas a fin de mes y cómo solucionarlo")

# -----------------------
# INPUT
# -----------------------
st.header("📊 Tus datos")

ingresos = st.number_input("Ingresos mensuales (€)", min_value=0, value=2000)

st.subheader("🏠 Vivienda")
vivienda_tipo = st.selectbox("Tipo de vivienda", ["Alquiler", "Hipoteca"])
vivienda = st.number_input("Pago mensual vivienda", value=800)

st.subheader("💸 Gastos mensuales")
deuda = st.number_input("Cuotas de deuda", value=200)
alimentacion = st.number_input("Alimentación", value=300)
gasolina = st.number_input("Gasolina", value=120)
otros = st.number_input("Otros gastos", value=200)

st.subheader("🧾 Facturas")
luz = st.number_input("Electricidad", value=60)
agua = st.number_input("Agua", value=25)
gas = st.number_input("Gas", value=30)
internet = st.number_input("Internet", value=35)

calcular = st.button("Analizar con IA")

# -----------------------
# MOTOR IA
# -----------------------
def motor_ia(ingresos, gastos):
    total = sum(gastos.values())
    libre = ingresos - total

    ratio_gasto = total / ingresos if ingresos > 0 else 0
    ratio_deuda = gastos["deuda"] / ingresos if ingresos > 0 else 0

    problemas = []

    # Problemas estructurales
    if ratio_gasto > 0.6:
        problemas.append({
            "tipo": "estructura",
            "impacto": (ratio_gasto - 0.5) * ingresos,
            "msg": "Tus gastos fijos son demasiado altos"
        })

    if ratio_deuda > 0.3:
        problemas.append({
            "tipo": "deuda",
            "impacto": gastos["deuda"] * 0.2,
            "msg": "Tu nivel de deuda es elevado"
        })

    # Facturas
    if luz > ingresos * 0.05:
        problemas.append({"tipo": "luz", "impacto": luz * 0.3, "msg": "Electricidad cara"})

    if internet > 40:
        problemas.append({"tipo": "internet", "impacto": internet * 0.4, "msg": "Internet caro"})

    if gas > 40:
        problemas.append({"tipo": "gas", "impacto": gas * 0.3, "msg": "Gas elevado"})

    if agua > 30:
        problemas.append({"tipo": "agua", "impacto": agua * 0.2, "msg": "Agua alta"})

    problemas = sorted(problemas, key=lambda x: x["impacto"], reverse=True)

    return total, libre, ratio_gasto, ratio_deuda, problemas


# -----------------------
# EXPLICACIONES IA (EDUCACIÓN FINANCIERA)
# -----------------------
def explicar(tipo, ratio_gasto, ratio_deuda):
    if tipo == "deuda":
        return f"""
💳 **Análisis de deuda**

Estás destinando un **{round(ratio_deuda*100,1)}%** de tus ingresos a deuda.

📉 A partir del 35% se considera riesgo financiero.

Esto significa:
- menos capacidad de ahorro
- mayor vulnerabilidad ante imprevistos

👉 Reducir esto es una prioridad.
"""

    if tipo == "estructura":
        return f"""
🏠 **Análisis de gastos**

Tus gastos fijos representan un **{round(ratio_gasto*100,1)}%** de tus ingresos.

📊 Lo recomendable es < 50%.

Esto indica:
- tu nivel de vida está ajustado a ingresos
- tienes poco margen de maniobra

👉 Necesitas optimizar gastos estructurales.
"""

    if tipo == "luz":
        return """
💡 **Electricidad**

Estás pagando por encima de lo habitual.

Muchas veces ocurre por:
- tarifas antiguas
- potencia mal ajustada

👉 Cambiar de compañía puede reducir coste sin esfuerzo.
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
        "otros": otros
    }

    total, libre, ratio, ratio_deuda, problemas = motor_ia(ingresos, gastos)

    st.header("📊 Resumen financiero")

    st.write(f"💸 Gastos totales: **{total}€**")
    st.write(f"💰 Dinero libre: **{libre}€**")
    st.write(f"📉 Ratio gasto: **{round(ratio*100,1)}%**")

    # -----------------------
    # GRÁFICO
    # -----------------------
    st.subheader("📊 Distribución de gastos")

    fig = go.Figure(data=[go.Pie(labels=list(gastos.keys()), values=list(gastos.values()), hole=.4)])
    st.plotly_chart(fig)

    # -----------------------
    # 50/30/20
    # -----------------------
    st.subheader("📊 Regla 50/30/20")

    necesarios = vivienda + deuda + luz + agua + gas + internet + alimentacion
    ocio = gasolina + otros
    ahorro = ingresos - total

    st.write(f"Necesidades: {round(necesarios/ingresos*100)}%")
    st.write(f"Ocio: {round(ocio/ingresos*100)}%")
    st.write(f"Ahorro: {round(ahorro/ingresos*100)}%")

    if necesarios > ingresos * 0.5:
        st.error("⚠️ Estás por encima del 50% en gastos necesarios")
    else:
        st.success("✅ Buen equilibrio")

    # -----------------------
    # PREDICCIÓN
    # -----------------------
    st.subheader("🔮 Predicción")

    if libre < 0:
        st.error("❌ No llegas a fin de mes con este nivel de gasto")
    else:
        st.success("✅ Llegas a fin de mes")

    # -----------------------
    # PROBLEMA PRINCIPAL
    # -----------------------
    if problemas:
        principal = problemas[0]

        st.subheader("🚨 Problema principal")
        st.error(principal["msg"])

        st.write(explicar(principal["tipo"], ratio, ratio_deuda))

    # -----------------------
    # PLAN DE ACCIÓN + MONETIZACIÓN
    # -----------------------
    st.header("💡 Plan de acción")

    for p in problemas:

        if p["tipo"] == "deuda":
            st.write("👉 Refinanciar deuda para reducir cuota")
            st.write("💰 Ahorro estimado: hasta 20% anual")
            st.link_button("Ver opciones de deuda", "https://google.com")

        elif p["tipo"] == "luz":
            st.write("👉 Cambiar tarifa eléctrica")
            st.write("💰 Ahorro estimado: 100–200€/año")
            st.link_button("Ver tarifas de luz", "https://google.com")

        elif p["tipo"] == "internet":
            st.write("👉 Cambiar proveedor de internet")
            st.link_button("Ver ofertas internet", "https://google.com")

        elif p["tipo"] == "gas":
            st.write("👉 Optimizar tarifa de gas")
            st.link_button("Ver tarifas gas", "https://google.com")

        elif p["tipo"] == "agua":
            st.write("👉 Revisar consumo de agua")

        elif p["tipo"] == "estructura":
            st.write("👉 Reducir gastos estructurales (vivienda o estilo de vida)")

    st.divider()
    st.success("👉 Empieza por el problema con mayor impacto económico")

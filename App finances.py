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
# PLAN DE ACCIÓN INTELIGENTE
# -----------------------
st.header("💡 Plan de acción inteligente")

def analisis_global(total, ingresos, libre, ratio):
    if libre < 0:
        return f"""
🚨 Situación crítica

Estás gastando más de lo que ingresas.

💸 Estás en déficit mensual.

👉 Prioridad absoluta:
- reducir gastos fijos
- eliminar deuda cara
"""
    elif ratio > 0.6:
        return f"""
⚠️ Situación ajustada

Estás gastando el {round(ratio*100,1)}% de tus ingresos.

📉 Tienes poco margen de seguridad.

👉 Problema estructural en tu nivel de gasto.
"""
    else:
        return f"""
✅ Situación estable

Tienes margen financiero positivo.

💡 Oportunidad de optimización de gastos.

👉 Aquí el objetivo es ahorrar más, no sobrevivir.
"""

st.subheader("🧠 Resumen global")
st.info(analisis_global(total, ingresos, libre, ratio))


# -----------------------
# OPTIMIZACIÓN FACTURAS
# -----------------------
st.subheader("📡 Optimización de facturas")

ahorro_facturas = 0

if luz > 40:
    ahorro = int((luz - 25) * 12)
    ahorro_facturas += ahorro
    st.write(f"💡 Luz: podrías ahorrar hasta **{ahorro}€/año**")
    st.link_button("Ver tarifas luz", "https://google.com")

if gas > 35:
    ahorro = int((gas - 25) * 12)
    ahorro_facturas += ahorro
    st.write(f"🔥 Gas: posible ahorro de **{ahorro}€/año**")
    st.link_button("Ver tarifas gas", "https://google.com")

if internet > 40:
    ahorro = int((internet - 25) * 12)
    ahorro_facturas += ahorro
    st.write(f"🌐 Internet: posible ahorro de **{ahorro}€/año**")
    st.link_button("Ver ofertas internet", "https://google.com")

if agua > 30:
    ahorro = int((agua - 20) * 12)
    ahorro_facturas += ahorro
    st.write(f"🚰 Agua: posible ahorro de **{ahorro}€/año**")

if ahorro_facturas > 0:
    st.success(f"💰 Ahorro total estimado en facturas: **{ahorro_facturas}€/año**")


# -----------------------
# SEGUROS (NUEVO MÓDULO)
# -----------------------
st.subheader("🛡️ Optimización de seguros")

tipo_seguro = st.selectbox(
    "Tipo de seguro principal",
    ["Coche", "Hogar", "Salud", "Varios"]
)

seguro_coste = st.number_input("Pago mensual seguros (€)", value=80)

if seguro_coste > 0:

    ahorro_seguro = int(seguro_coste * 0.25 * 12)

    st.write("📊 Análisis de seguros")

    if seguro_coste > 60:
        st.warning("⚠️ Tus seguros parecen por encima de la media del mercado")

        st.write(f"💰 Podrías ahorrar hasta **{ahorro_seguro}€/año**")

        st.link_button("Comparar seguros", "https://google.com")

    else:
        st.success("✅ Tus seguros están dentro de rango razonable")

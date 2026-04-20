import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="SmartBalance AI", layout="centered")

st.title("💰 SmartBalance AI")
st.write("Descubre por qué no llegas a fin de mes y cómo solucionarlo")

# -----------------------
# INPUT
# -----------------------
st.header("📊 Tus datos")

ingresos = st.number_input("Ingresos mensuales (€)", min_value=0, value=2000)

st.subheader("🏠 Vivienda")
vivienda_tipo = st.selectbox("Tipo", ["Alquiler", "Hipoteca"])
vivienda = st.number_input("Pago mensual vivienda", value=800)

st.subheader("💸 Gastos mensuales")
deuda = st.number_input("Cuotas de deuda", value=200)
alimentacion = st.number_input("Alimentación", value=300)
gasolina = st.number_input("Gasolina", value=120)

st.subheader("🧾 Facturas")
luz = st.number_input("Electricidad", value=60)
agua = st.number_input("Agua", value=25)
gas = st.number_input("Gas", value=30)
internet = st.number_input("Internet", value=35)

otros = st.number_input("Otros gastos", value=200)

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

    # Problema estructural
    if ratio_gasto > 0.6:
        impacto = (ratio_gasto - 0.5) * ingresos
        problemas.append({"tipo": "estructura", "impacto": impacto, "msg": "Gastos estructurales demasiado altos"})

    # Deuda
    if ratio_deuda > 0.3:
        ahorro = gastos["deuda"] * 0.2
        problemas.append({"tipo": "deuda", "impacto": ahorro, "msg": "Nivel de deuda elevado"})

    # Facturas
    if gastos["luz"] > ingresos * 0.05:
        problemas.append({"tipo": "luz", "impacto": gastos["luz"] * 0.3, "msg": "Gasto alto en electricidad"})

    if gastos["internet"] > 40:
        problemas.append({"tipo": "internet", "impacto": gastos["internet"] * 0.4, "msg": "Internet caro"})

    if gastos["gas"] > 40:
        problemas.append({"tipo": "gas", "impacto": gastos["gas"] * 0.3, "msg": "Gas elevado"})

    if gastos["agua"] > 30:
        problemas.append({"tipo": "agua", "impacto": gastos["agua"] * 0.2, "msg": "Agua por encima de lo normal"})

    problemas = sorted(problemas, key=lambda x: x["impacto"], reverse=True)

    # Predicción
    dias = int((ingresos / total) * 30) if total > ingresos else 30

    return total, libre, ratio_gasto, problemas, dias

# -----------------------
# RESULTADOS
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

    total, libre, ratio, problemas, dias = motor_ia(ingresos, gastos)

    st.header("📈 Resumen financiero")

    st.write(f"💸 Gastos totales: **{total}€**")
    st.write(f"💰 Dinero libre: **{libre}€**")
    st.write(f"📊 Ratio gasto: **{round(ratio*100,1)}%**")

    # -----------------------
    # GRÁFICO
    # -----------------------
    labels = list(gastos.keys())
    values = list(gastos.values())

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
    st.plotly_chart(fig)

    # -----------------------
    # 50/30/20
    # -----------------------
    st.subheader("📊 Regla 50/30/20")

    necesarios = vivienda + deuda + luz + agua + gas + internet + alimentacion
    ocio = gasolina + otros
    ahorro = ingresos - total

    st.write(f"Necesidades: {int(necesarios/ingresos*100)}%")
    st.write(f"Ocio: {int(ocio/ingresos*100)}%")
    st.write(f"Ahorro: {int(ahorro/ingresos*100)}%")

    if necesarios > ingresos * 0.5:
        st.error("⚠️ Gastos necesarios demasiado altos (>50%)")
    else:
        st.success("✅ Buen equilibrio en gastos necesarios")

    # -----------------------
    # PREDICCIÓN
    # -----------------------
    st.subheader("🔮 Predicción")

    if libre < 0:
        st.error(f"Te quedarás sin dinero en **{dias} días**")
    else:
        st.success("Llegas a fin de mes")

    # -----------------------
    # DIAGNÓSTICO
    # -----------------------
    if problemas:
        st.subheader("🚨 Problema principal")
        st.error(problemas[0]["msg"])

    # -----------------------
    # ACCIONES (MONETIZACIÓN)
    # -----------------------
    st.header("💡 Cómo mejorar")

    for p in problemas:
        if p["tipo"] == "deuda":
            st.write("👉 Refinanciar deuda")
            st.link_button("Ver opciones deuda", "https://google.com")

        elif p["tipo"] == "luz":
            st.write("👉 Cambiar tarifa de luz")
            st.link_button("Ver tarifas luz", "https://google.com")

        elif p["tipo"] == "internet":
            st.write("👉 Cambiar proveedor de internet")
            st.link_button("Ver ofertas internet", "https://google.com")

        elif p["tipo"] == "gas":
            st.write("👉 Optimizar tarifa de gas")
            st.link_button("Ver tarifas gas", "https://google.com")

        elif p["tipo"] == "agua":
            st.write("👉 Revisar consumo de agua")

        elif p["tipo"] == "estructura":
            st.write("👉 Reducir gastos estructurales")

    st.divider()
    st.success("Empieza por el problema con mayor impacto económico")

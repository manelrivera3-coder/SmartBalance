import streamlit as st

st.set_page_config(page_title="SmartBalance AI", layout="centered")

st.title("💰 SmartBalance AI")
st.write("Tu asistente financiero inteligente")

# -----------------------
# INPUT
# -----------------------
st.header("📊 Tus datos")

ingresos = st.number_input("Ingresos mensuales (€)", min_value=0, value=2000)

st.subheader("Gastos mensuales")
vivienda = st.number_input("Vivienda", value=800)
deuda = st.number_input("Cuotas de deuda", value=200)
alimentacion = st.number_input("Alimentación", value=300)
transporte = st.number_input("Transporte", value=120)
luz = st.number_input("Electricidad", value=60)
otros = st.number_input("Otros", value=200)

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

    # 1. Problema estructural
    if ratio_gasto > 0.6:
        impacto = (ratio_gasto - 0.5) * ingresos
        problemas.append({
            "tipo": "estructura",
            "impacto": impacto,
            "mensaje": "Tu estructura de gastos es insostenible"
        })

    # 2. Deuda
    if ratio_deuda > 0.3:
        ahorro = gastos["deuda"] * 0.2
        problemas.append({
            "tipo": "deuda",
            "impacto": ahorro,
            "mensaje": "Tu deuda es demasiado alta"
        })

    # 3. Luz
    if gastos["luz"] > ingresos * 0.05:
        ahorro = gastos["luz"] - (ingresos * 0.03)
        problemas.append({
            "tipo": "luz",
            "impacto": ahorro,
            "mensaje": "Estás pagando demasiado en luz"
        })

    # Ordenar por impacto (€ real)
    problemas = sorted(problemas, key=lambda x: x["impacto"], reverse=True)

    # Predicción (IA simple)
    if libre < 0:
        dias = int((ingresos / total) * 30) if total > 0 else 30
    else:
        dias = 30

    return {
        "total": total,
        "libre": libre,
        "ratio": ratio_gasto,
        "problemas": problemas,
        "dias": dias
    }

# -----------------------
# RESULTADOS
# -----------------------
if calcular and ingresos > 0:

    gastos = {
        "vivienda": vivienda,
        "deuda": deuda,
        "alimentacion": alimentacion,
        "transporte": transporte,
        "luz": luz,
        "otros": otros
    }

    resultado = motor_ia(ingresos, gastos)

    st.header("🧠 Diagnóstico inteligente")

    st.write(f"💸 Gastas: **{resultado['total']}€**")
    st.write(f"💰 Dinero libre: **{resultado['libre']}€**")
    st.write(f"📉 Ratio gasto: **{round(resultado['ratio']*100,1)}%**")

    # Predicción
    st.subheader("🔮 Predicción")
    if resultado["libre"] < 0:
        st.error(f"❌ A este ritmo, te quedarás sin dinero en **{resultado['dias']} días**")
    else:
        st.success("✅ Llegas a fin de mes, pero puedes optimizar")

    # Problema principal
    if resultado["problemas"]:
        principal = resultado["problemas"][0]

        st.subheader("🚨 Problema principal")
        st.error(principal["mensaje"])
        st.write(f"💥 Impacto estimado: **{int(principal['impacto']*12)}€ / año**")

    # Plan de acción
    st.subheader("📌 Plan de acción automático")

    for p in resultado["problemas"]:
        if p["tipo"] == "deuda":
            st.write("👉 Refinanciar deuda para bajar cuota")
            st.link_button("Ver opciones de deuda", "https://google.com")

        elif p["tipo"] == "luz":
            st.write("👉 Cambiar tarifa eléctrica")
            st.link_button("Ver tarifas de luz", "https://google.com")

        elif p["tipo"] == "estructura":
            st.write("👉 Reducir gastos estructurales (vivienda u otros)")

    st.divider()
    st.success("👉 Empieza por el problema con mayor impacto económico")

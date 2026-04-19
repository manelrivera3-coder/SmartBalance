import streamlit as st
import plotly.graph_objects as go

# 1. CONFIGURACIÓ I ESTILS
st.set_page_config(page_title="SmartBalance", layout="wide", page_icon="💰")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .company-box { 
        background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; 
        text-align: center; margin-bottom: 10px; min-height: 160px;
    }
    .save-label { color: #28a745; font-weight: bold; font-size: 0.9rem; }
    .total-save-banner { 
        background-color: #155724; color: white; padding: 20px; border-radius: 12px; 
        text-align: center; margin-bottom: 25px; font-size: 1.5rem; font-weight: bold;
    }
    .investment-card { padding: 15px; border-radius: 10px; border: 2px solid #e0e0e0; margin-bottom: 10px; min-height: 180px; }
    .recommended { border: 2px solid #28a745 !important; background-color: #f0fff4; }
    .debt-alert { padding: 10px; border-radius: 8px; font-size: 0.85rem; font-weight: bold; }
    .bad-debt { background-color: #f8d7da; color: #721c24; border-left: 5px solid #dc3545; }
    .good-debt { background-color: #d4edda; color: #155724; border-left: 5px solid #28a745; }
    </style>
    """, unsafe_allow_html=True)

# 2. INITIALIZE SESSION STATE
if 'deutes_lista' not in st.session_state:
    st.session_state.deutes_lista = []

# 3. SIDEBAR - GASTOS PRINCIPALES
with st.sidebar:
    st.header("📊 Tus Ingresos y Gastos")
    ing_val = st.number_input("Ingresos mensuales netos (€)", min_value=0, value=2000)
    st.subheader("Gastos Fijos / Necesidades")
    lloguer_val = st.number_input("Alquiler / Hipoteca (Cuota)", value=800)
    alim_val = st.number_input("Alimentación (Mensual)", value=350)
    gaso_val = st.number_input("Gasolina / Transporte", value=120)
    llum_val = st.number_input("Luz (Electricidad)", value=60)
    gas_val = st.number_input("Gas", value=30)
    aigua_val = st.number_input("Agua", value=20)
    int_val = st.number_input("Internet", value=35)
    mob_val = st.number_input("Móvil", value=15)
    seg_val = st.number_input("Seguro Coche (Mensual)", value=40)

# Càlculs totals
total_cuotas_deuda = sum(d['cuota'] for d in st.session_state.deutes_lista)
total_fijos = lloguer_val + alim_val + gaso_val + llum_val + gas_val + aigua_val + int_val + mob_val + seg_val + total_cuotas_deuda
ratio_fijos = (total_fijos / ing_val * 100) if ing_val > 0 else 0
oci_ideal = ing_val * 0.3
ahorro_ideal = ing_val * 0.2
sobrante_real = max(0, ing_val - total_fijos)

# 4. PESTAÑAS
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Radiografía", "✂️ Plan Ahorro", "📉 Deuda", "📈 Inversión", "🎓 Educación"])

with tab1:
    st.title("Estado de Salud Financiera")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Gastos Fijos", f"{total_fijos} €")
    c2.metric("% Sobre Ingresos", f"{ratio_fijos:.1f}%", delta="Máx 50%", delta_color="inverse")
    c3.metric("Ahorro Ideal", f"{int(ahorro_ideal)} €")
    c4.metric("Sobrante Real", f"{int(sobrante_real)} €")
    st.divider()
    col_l, col_r = st.columns([1, 1])
    with col_l:
        fig = go.Figure(data=[go.Pie(labels=["Fijos/Necesidad", "Ocio (30%)", "Ahorro (20%)"], 
                                     values=[total_fijos, oci_ideal, ahorro_ideal], hole=.4)])
        fig.update_layout(height=400, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    with col_r:
        st.subheader("Diagnóstico 50/30/20")
        if ratio_fijos <= 50: st.success("✅ ¡Posición sólida!")
        else: st.error("⚠️ Gastos fijos demasiado altos.")

with tab2:
    est_total = (int_val - 20)*12 + (0.18 - 0.11)*3000 + (mob_val - 7)*12 + (seg_val - 18)*12
    st.markdown(f"<div class='total-save-banner'>🚀 Ahorro anual potencial: {round(est_total, 2)} € 💰</div>", unsafe_allow_html=True)
    def draw_offer(cia, p_nou, p_act, url, unitat="€", is_kwh=False):
        est = (p_act - p_nou) * 3000 if is_kwh else (p_act - p_nou) * 12
        st.markdown(f"<div class='company-box'><b>{cia}</b><br><b>{p_nou}{unitat}</b><br><span class='save-label'>Ahorro: {max(0, round(est,2))}€/año</span></div>", unsafe_allow_html=True)
        st.link_button("Contratar", url, use_container_width=True)
    with st.expander("🚗 Seguro de Coche", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1: draw_offer("Qualitas", 18, seg_val, "https://google.com")
        with c2: draw_offer("Axa", 22, seg_val, "https://google.com")
        with c3: draw_offer("Mapfre", 28, seg_val, "https://google.com")

with tab3:
    st.header("Análisis de Créditos y Préstamos")
    with st.expander("➕ Añadir Deuda (Máximo 5)"):
        cl1, cl2, cl3, cl4 = st.columns([2, 1, 1, 1])
        d_n = cl1.text_input("Nombre Préstamo")
        d_t = cl2.selectbox("Tipo", ["Hipoteca", "Préstamo Personal", "Coche", "Tarjeta/Revolving"])
        d_c = cl3.number_input("Cuota Mensual (€)", min_value=0.0)
        d_i = cl4.number_input("Interés TIN (%)", min_value=0.0)
        if st.button("Guardar Deuda"):
            if len(st.session_state.deutes_lista) < 5:
                st.session_state.deutes_lista.append({"nom": d_n, "tipus": d_t, "cuota": d_c, "interes": d_i})
                st.rerun()
    for i, d in enumerate(st.session_state.deutes_lista):
        es_car = (d['tipus'] == "Hipoteca" and d['interes'] > 4) or (d['tipus'] != "Hipoteca" and d['interes'] > 9)
        status = "bad-debt" if es_car else "good-debt"
        cols = st.columns([2, 3, 1])
        cols[0].write(f"**{d['nom']}** ({d['tipus']})")
        cols[1].markdown(f"<div class='debt-alert {status}'>{d['interes']}%: {'Malo' if es_car else 'Bueno'}</div>", unsafe_allow_html=True)
        if cols[2].button("X", key=f"del_{i}"):
            st.session_state.deutes_lista.pop(i); st.rerun()
            # --- TAB 4: INVERSIÓN (TEST + RECOMENDACIONES) ---
with tab4:
    st.header("Tu Plan de Inversión")
    
    with st.expander("📝 Test de Perfil de Riesgo (10 Preguntas)", expanded=True):
        sc = 0
        q1 = st.selectbox("1. Edad", ["18-30", "31-45", "46-60", "60+"])
        q2 = st.selectbox("2. Plazo de inversión (¿Cuándo necesitarás el dinero?)", ["< 2 años", "2-5 años", "5-10 años", "> 10 años"])
        q3 = st.radio("3. ¿Qué harías si tu inversión baja un 20% en un mes?", ["Vender todo por miedo", "Mantener y esperar", "Comprar más barato"])
        q4 = st.radio("4. ¿Tienes un fondo de emergencia (3-6 meses de gastos)?", ["No", "Sí, pero pequeño", "Sí, completo"])
        q5 = st.selectbox("5. Nivel de conocimientos financieros", ["Principiante", "Intermedio", "Avanzado"])
        q6 = st.radio("6. Estabilidad de tus ingresos mensuales", ["Inestables", "Normales", "Muy estables / Funcionario"])
        q7 = st.radio("7. Prioridad en la inversión", ["No perder nada de dinero", "Equilibrio riesgo/beneficio", "Maximizar rentabilidad"])
        q8 = st.radio("8. ¿Qué porcentaje de tu ahorro mensual vas a invertir?", ["<10%", "10-30%", ">30%"])
        q9 = st.selectbox("9. Objetivo principal", ["Proteger capital", "Complemento jubilación", "Comprar casa / Crecimiento"])
        q10 = st.radio("10. ¿Cómo te afecta ver cambios diarios en tu cuenta?", ["Me estresa mucho", "Lo miro poco", "No me importa"])

        # Lògica de puntuació per definir perfil
        if q3 == "Comprar más barato": sc += 3
        if q7 == "Maximizar rentabilidad": sc += 3
        if q1 == "18-30": sc += 2
        if q2 == "> 10 años": sc += 2
        if q10 == "No me importa": sc += 2
        
        perfil = "Conservador" if sc < 4 else ("Moderado" if sc < 8 else "Arriesgado")
        st.subheader(f"Tu perfil de inversor es: **{perfil}**")

    st.divider()
    
    def draw_inv(nom, risc, rent, desc, rec=False):
        cl = "investment-card recommended" if rec else "investment-card"
        rec_tag = "<b style='color:#28a745;'>⭐ RECOMENDADO PARA TI</b><br>" if rec else ""
        st.markdown(f"""
            <div class='{cl}'>
                <h4>{nom}</h4>
                {rec_tag}
                <b>Riesgo:</b> {risc} | <b>Rentabilidad:</b> {rent}<br>
                <p style='font-size:0.9rem; margin-top:10px;'>{desc}</p>
            </div>
        """, unsafe_allow_html=True)
        st.link_button(f"Abrir cuenta en {nom}", "https://google.com")

    st.subheader("Opciones de Inversión según riesgo")
    c_i1, c_i2, c_i3 = st.columns(3)
    
    with c_i1:
        st.write("### 🛡️ Bajo Riesgo")
        draw_inv("Cuentas Remuneradas", "Mínimo", "2-3.5%", "Tu dinero siempre disponible y seguro (FGD).", rec=(perfil=="Conservador"))
        draw_inv("Depósitos a Plazo", "Bajo", "3-4%", "Dinero bloqueado a cambio de un interés fijo.")

    with c_i2:
        st.write("### ⚖️ Moderado")
        draw_inv("Fondos Indexados", "Medio", "7-9%", "Carteras diversificadas globalmente (MSCI World).", rec=(perfil=="Moderado"))
        draw_inv("Robo-Advisors", "Medio", "6-8%", "Gestión automática basada en algoritmos.")

    with c_i3:
        st.write("### 🚀 Alto Riesgo")
        draw_inv("Acciones y ETFs", "Alto", "Variable", "Inversión directa en empresas. Alta volatilidad.", rec=(perfil=="Arriesgado"))
        draw_inv("Criptomonedas / Otros", "Muy Alto", "Variable", "Solo para una pequeña parte de tu capital.")

# --- TAB 5: EDUCACIÓN ---
with tab5:
    st.header("Academia SmartBalance")
    st.write("### Los 3 Pilares del Éxito Financiero")
    st.info("1. **Optimización**: No gastes en facturas lo que puedes invertir.")
    st.info("2. **Deuda Inteligente**: Elimina deudas de más del 8% de interés lo antes posible.")
    st.info("3. **Interés Compuesto**: Empieza a invertir hoy, aunque sea poco. El tiempo es tu mayor aliado.")
    
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Vídeo d'exemple

import streamlit as st
import plotly.graph_objects as go

# 1. CONFIGURACIÓ DE LA PÀGINA
st.set_page_config(page_title="SmartBalance", layout="wide", page_icon="💰")

# Estils CSS Personalitzats
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .company-box { 
        background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; 
        text-align: center; margin-bottom: 5px; min-height: 160px;
    }
    .price-text { font-size: 1.3rem; font-weight: bold; color: #1E1E1E; }
    .save-label { color: #28a745; font-weight: bold; font-size: 0.9rem; margin-top: 5px; }
    .total-save-banner { 
        background-color: #155724; color: white; padding: 20px; border-radius: 12px; 
        text-align: center; margin-bottom: 25px; font-size: 1.5rem; font-weight: bold;
    }
    .debt-card {
        background-color: #fff3cd; border-left: 5px solid #ffc107; padding: 15px; border-radius: 5px; margin-bottom: 10px;
    }
    .st-expander { border: none !important; box-shadow: none !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. DICCIONARI DE TEXTOS
texts = {
    "Español": {
        "titol": "SmartBalance 💰",
        "tab1": "📊 Mi Radiografía",
        "tab2": "✂️ Plan de Ahorro",
        "tab3": "📉 Análisis de Deuda",
        "ingresos_label": "Ingresos mensuales netos (€)",
        "gastos_f": "Gastos Fijos Mensuales",
        "seguro_coche": "Seguro Coche (Mensual)",
        "ratio_label": "% Gastos Fijos",
        "total_ahorro_msg": "🚀 Si optimizas hoy, puedes ahorrar al año: ",
        "btn_save": "Contratar Oferta",
        "ahorro_anual": "Ahorro anual: ",
        "analisis_prof": "Análisis Profesional de Deuda",
        "btn_mejora": "Solicitar mejora de condiciones",
        "deuda_buena": "✅ Deuda bajo control (Interés bajo)",
        "deuda_mala": "⚠️ Deuda Peligrosa (Interés alto)",
        "f_marca": "Marca del coche",
        "f_combustible": "Combustible",
        "f_uso": "Uso del vehículo",
        "f_edad": "Edad conductor",
        "f_carnet": "Años de carnet",
        "preu_kwh_actual": "¿A cuánto pagas el kWh? (€)",
        "filtro_fibra": "Velocidad Fibra",
        "filtro_mobil": "Datos Móvil",
    },
    "English": {
        "titol": "SmartBalance 💰",
        "tab1": "📊 My Radiography",
        "tab2": "✂️ Saving Plan",
        "tab3": "📉 Debt Analysis",
        "ingresos_label": "Net Income (€)",
        "gastos_f": "Fixed Expenses",
        "seguro_coche": "Car Insurance (Monthly)",
        "ratio_label": "% Fixed Expenses",
        "total_ahorro_msg": "🚀 If you optimize today, you can save yearly: ",
        "btn_save": "Get Offer",
        "ahorro_anual": "Annual savings: ",
        "analisis_prof": "Professional Debt Analysis",
        "btn_mejora": "Request better conditions",
        "deuda_buena": "✅ Safe Debt (Low interest)",
        "deuda_mala": "⚠️ Dangerous Debt (High interest)",
        "f_marca": "Car Brand",
        "f_combustible": "Fuel type",
        "f_uso": "Vehicle use",
        "f_edad": "Driver age",
        "f_carnet": "License years",
        "preu_kwh_actual": "Price per kWh (€)",
        "filtro_fibra": "Fiber Speed",
        "filtro_mobil": "Mobile Data",
    }
}

# 3. SIDEBAR - ENTRADA DE DADES
with st.sidebar:
    idioma = st.selectbox("Language / Idioma", ["Español", "English"])
    t = texts[idioma]
    st.header(t["gastos_f"])
    ing_val = st.number_input(t["ingresos_label"], min_value=1, value=2000)
    lloguer_val = st.number_input("Alquiler / Hipoteca", value=800)
    llum_val = st.number_input("Luz (Electricidad)", value=60)
    gas_val = st.number_input("Gas", value=30)
    aigua_val = st.number_input("Agua", value=20)
    int_val = st.number_input("Internet (Fibra)", value=35)
    mob_val = st.number_input("Móvil", value=15)
    seg_val = st.number_input(t["seguro_coche"], value=40)
    deute_val = st.number_input("Cuota mensual Deudas (€)", value=150)

# Càlculs Radiografia 50/30/20
total_fijos = lloguer_val + llum_val + gas_val + aigua_val + int_val + mob_val + seg_val + deute_val
ratio_fijos = (total_fijos / ing_val) * 100
oci_ideal = ing_val * 0.3
ahorro_ideal = ing_val * 0.2
is_ready = ing_val > 0 and total_fijos > 0

# 4. ESTRUCTURA DE PESTANYES
tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], "🎓 Educación"])

# --- TAB 1: RADIOGRAFIA I DIAGNÒSTIC ---
with tab1:
    st.title(t["titol"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Gastos Fijos", f"{total_fijos} €")
    c2.metric(t["ratio_label"], f"{ratio_fijos:.1f}%", delta="Max 50%")
    c3.metric("Ocio (30%)", f"{int(oci_ideal)} €")
    c4.metric("Ahorro (20%)", f"{int(ahorro_ideal)} €")

    st.divider()
    col_l, col_r = st.columns([1, 1])
    with col_l:
        labels = ["Fijos Actuales", "Ocio Ideal", "Ahorro Ideal"]
        values = [total_fijos, oci_ideal, ahorro_ideal]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
        fig.update_layout(height=400, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    with col_r:
        st.subheader("Veredicto Financiero")
        if ratio_fijos <= 50:
            st.success("✅ ¡Felicidades! Tus gastos fijos están bajo control.")
        else:
            st.error("⚠️ Atención: Tus gastos fijos superan el 50% recomendado.")
            exces = total_fijos - (ing_val * 0.5)
            st.write(f"Estás gastando **{int(exces)}€** más de lo ideal en facturas fijas.")
        st.info(f"Para cumplir la regla, tus gastos fijos no deberían pasar de **{int(ing_val * 0.5)}€**.")

# --- TAB 2: PLAN DE AHORRO (REFERITS + COMPARADOR) ---
with tab2:
    if not is_ready:
        st.warning("Por favor, introduce tus datos en la pestaña 1.")
    else:
        # Càlcul de l'estalvi potencial per al banner
        est_int = max(0, (int_val - 20) * 12)
        est_llu = max(0, (0.18 - 0.11) * 3000)
        est_mob = max(0, (mob_val - 7) * 12)
        est_seg = max(0, (seg_val - 18) * 12)
        est_total = est_int + est_llu + est_mob + est_seg

        st.markdown(f"<div class='total-save-banner'>{t['total_ahorro_msg']} {round(est_total, 2)} € 💰</div>", unsafe_allow_html=True)

        def draw_offer(cia, p_nou, p_act, url, unitat="€", is_kwh=False):
            estalvi = (p_act - p_nou) * 3000 if is_kwh else (p_act - p_nou) * 12
            st.markdown(f"""<div class='company-box'><b>{cia}</b><br><span class='price-text'>{p_nou}{unitat}</span><br>
                        <span class='save-label'>{t['ahorro_anual']}{max(0, round(estalvi,2))}€</span></div>""", unsafe_allow_html=True)
            st.link_button(t["btn_save"], url, use_container_width=True)

        # 2.1 SECCIÓ ASSEGURANÇA (Rastreator Style)
        with st.expander("🚗 Buscador de Seguros de Coche", expanded=True):
            ca, cb, cc = st.columns(3)
            with ca: marca = st.selectbox(t["f_marca"], ["Seat", "Toyota", "BMW", "Otros"]); edat = st.number_input(t["f_edad"], 18, 90, 30)
            with cb: comb = st.selectbox(t["f_combustible"], ["Gasolina", "Diésel"]); carnet = st.number_input(t["f_carnet"], 0, 70, 10)
            with cc: tipo_seg = st.selectbox("Cobertura", ["Terceros", "Todo Riesgo"])
            
            p_base = 18 if tipo_seg == "Terceros" else 45
            c_of1, c_of2, c_of3 = st.columns(3)
            with c_of1: draw_offer("Qualitas", p_base, seg_val, "https://google.com")
            with c_of2: draw_offer("Axa", round(p_base*1.1, 2), seg_val, "https://google.com")
            with c_of3: draw_offer("Mapfre", round(p_base*1.3, 2), seg_val, "https://google.com")

        # 2.2 INTERNET I LLUM
        col_l, col_r = st.columns(2)
        with col_l:
            with st.expander("🌐 Internet y Fibra"):
                f_f = st.select_slider(t["filtro_fibra"], options=["300Mb", "600Mb", "1Gb"])
                p_f = 20 if f_f=="300Mb" else (25 if f_f=="600Mb" else 30)
                c1, c2, c3 = st.columns(3)
                with c1: draw_offer("Digi", p_f, int_val, "https://google.com")
                with c2: draw_offer("Lowi", p_f+4, int_val, "https://google.com")
                with c3: draw_offer("O2", p_f+7, int_val, "https://google.com")
        with col_r:
            with st.expander("💡 Luz"):
                kwh_in = st.number_input(t["preu_kwh_actual"], 0.0, 0.5, 0.18)
                c1, c2, c3 = st.columns(3)
                with c1: draw_offer("Octopus", 0.11, kwh_in, "https://google.com", "€/kWh", True)
                with c2: draw_offer("Naturgy", 0.13, kwh_in, "https://google.com", "€/kWh", True)
                with c3: draw_offer("Endesa", 0.14, kwh_in, "https://google.com", "€/kWh", True)

        # 2.3 MOBIL I GAS
        col_l2, col_r2 = st.columns(2)
        with col_l2:
            with st.expander("📲 Móvil"):
                f_m = st.select_slider(t["filtro_mobil"], options=["20GB", "100GB", "Unlimited"])
                p_m = 7 if f_m=="20GB" else (15 if f_m=="100GB" else 25)
                c1, c2, c3 = st.columns(3)
                with c1: draw_offer("Simyo", p_m, mob_val, "https://google.com")
                with c2: draw_offer("Pepephone", p_m+3, mob_val, "https://google.com")
                with c3: draw_offer("Vodafone", p_m+10, mob_val, "https://google.com")
        with col_r2:
            with st.expander("🔥 Gas"):
                c1, c2, c3 = st.columns(3)
                with c1: draw_offer("Energía XXI", 18, gas_val, "https://google.com")
                with c2: draw_offer("TotalEnergies", 20, gas_val, "https://google.com")
                with c3: draw_offer("Endesa Gas", 22, gas_val, "https://google.com")

# --- TAB 3: ANÁLISIS DE DEUDA (ASSESSOR PROFESSIONAL) ---
with tab3:
    st.header(t["analisis_prof"])
    if deute_val <= 0:
        st.success("No tienes deudas registradas. ¡Tu salud financiera es excelente!")
    else:
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.subheader("Configuración de tu deuda")
            tipo_d = st.selectbox("Tipo de deuda", ["Hipoteca", "Préstamo Personal", "Tarjeta Revolving", "Coche"])
            cap_pend = st.number_input("Capital pendiente (€)", value=150000 if tipo_d=="Hipoteca" else 5000)
            int_act = st.number_input("Interés TIN (%)", value=3.5 if tipo_d=="Hipoteca" else 9.0, step=0.1)
            anys_pend = st.number_input("Años restantes", value=20 if tipo_d=="Hipoteca" else 5)
        
        with col_d2:
            st.subheader("Diagnóstico del Experto")
            if tipo_d == "Tarjeta Revolving" or int_act > 12:
                st.markdown(f"<div class='debt-card'><h4>{t['deuda_mala']}</h4>Intereses abusivos detectados. Recomendamos reunificar deuda para bajar al 7-8%.</div>", unsafe_allow_html=True)
                st.link_button("🔥 Reunificar mi deuda ahora", "https://google.com")
            elif tipo_d == "Hipoteca" and int_act > 3.0:
                st.markdown(f"<div class='debt-card'><h4>🔍 Oportunidad detectada</h4>Tu hipoteca es cara. Podríamos mejorarla a un 2.4% fijo.</div>", unsafe_allow_html=True)
                st.link_button("📩 Solicitar mejora de hipoteca", "https://google.com")
            else:
                st.markdown(f"<div class='debt-card'><h4>{t['deuda_buena']}</h4>Tus condiciones son competitivas. Sigue así.</div>", unsafe_allow_html=True)

        dti = (deute_val / ing_val) * 100
        st.write(f"**Tu ratio de endeudamiento:** {dti:.1f}% (Límite saludable: 35%)")
        st.progress(min(dti/100, 1.0))

# --- TAB 4: EDUCACIÓ ---
with tab4:
    st.header("Educación Financiera")
    st.info("Aprende a gestionar tu dinero con la regla 50/30/20.")
    st.write("1. **50% Necesidades**: Vivienda, suministros, comida y seguros.")
    st.write("2. **30% Ocio**: Viajes, cenas, suscripciones.")
    st.write("3. **20% Ahorro/Inversión**: Fondo de emergencia y futuro.")

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
    .debt-alert { padding: 12px; border-radius: 8px; margin-bottom: 5px; font-size: 0.9rem; font-weight: bold; }
    .bad-debt { background-color: #f8d7da; color: #721c24; border-left: 5px solid #dc3545; }
    .good-debt { background-color: #d4edda; color: #155724; border-left: 5px solid #28a745; }
    .neutral-debt { background-color: #fff3cd; color: #856404; border-left: 5px solid #ffc107; }
    .investment-card { padding: 15px; border-radius: 10px; border: 2px solid #e0e0e0; margin-bottom: 10px; }
    .recommended { border: 2px solid #28a745 !important; background-color: #f0fff4; }
    </style>
    """, unsafe_allow_html=True)

# 2. DICCIONARI DE TEXTOS
texts = {
    "Español": {
        "titol": "SmartBalance 💰",
        "tab1": "📊 Mi Radiografía",
        "tab2": "✂️ Plan de Ahorro",
        "tab3": "📉 Centro de Deuda",
        "tab4": "📈 Inversión",
        "tab5": "🎓 Educación",
        "ingresos_label": "Ingresos mensuales netos (€)",
        "gastos_f": "Gastos Fijos Mensuales",
        "seguro_coche": "Seguro Coche (Mensual)",
        "ratio_label": "% Gastos Fijos",
        "veredicte_t": "Tu Diagnóstico 50/30/20",
        "btn_save": "Contratar Oferta",
        "ahorro_anual": "Ahorro anual: ",
        "total_ahorro_msg": "🚀 Si optimizas hoy, puedes ahorrar al año: ",
        "preu_kwh_actual": "¿A cuánto pagas el kWh? (€)",
        "filtro_fibra": "Velocidad Fibra",
        "filtro_mobil": "Datos Móvil",
        "f_marca": "Marca del coche",
        "f_combustible": "Combustible",
        "f_uso": "Uso del vehículo",
        "f_edad": "Edad conductor",
        "f_carnet": "Años de carnet",
        "analisis_prof": "Asesoría Profesional de Deuda",
        "veredicto_ok": "✅ ¡Lo estás haciendo genial! Tus gastos fijos están bajo control.",
        "veredicto_ko": "⚠️ Superas el 50% en gastos fijos. Tienes que optimizar facturas."
    }
}

# 3. SIDEBAR
with st.sidebar:
    idioma = st.selectbox("Idioma", ["Español"])
    t = texts[idioma]
    st.header(t["gastos_f"])
    ing_val = st.number_input(t["ingresos_label"], min_value=1, value=2000)
    lloguer_val = st.number_input("Alquiler / Hipoteca (Cuota)", value=800)
    alim_val = st.number_input("Alimentación (Súper)", value=350)
    gaso_val = st.number_input("Gasolina / Transporte", value=120)
    llum_val = st.number_input("Luz (Electricidad)", value=60)
    gas_val = st.number_input("Gas", value=30)
    aigua_val = st.number_input("Agua", value=20)
    int_val = st.number_input("Internet (Fibra)", value=35)
    mob_val = st.number_input("Móvil", value=15)
    seg_val = st.number_input(t["seguro_coche"], value=40)

if 'deutes_lista' not in st.session_state:
    st.session_state.deutes_lista = []

total_cuotas_deuda = sum(d['cuota'] for d in st.session_state.deutes_lista)

# Cálculos Globales (Incluyendo Alimentación y Gasolina)
total_fijos = lloguer_val + alim_val + gaso_val + llum_val + gas_val + aigua_val + int_val + mob_val + seg_val + total_cuotas_deuda
ratio_fijos = (total_fijos / ing_val) * 100
oci_ideal = ing_val * 0.3
ahorro_ideal = ing_val * 0.2
is_ready = ing_val > 0 and total_fijos > 0

tab1, tab2, tab3, tab4, tab5 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"], t["tab5"]])

with tab1:
    st.title(t["titol"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Gastos Fijos", f"{total_fijos} €")
    c2.metric(t["ratio_label"], f"{ratio_fijos:.1f}%", delta="Máx 50%", delta_color="inverse")
    c3.metric("Ocio Sugerido (30%)", f"{int(oci_ideal)} €")
    c4.metric("Ahorro Sugerido (20%)", f"{int(ahorro_ideal)} €")
    st.divider()
    col_l, col_r = st.columns([1, 1])
    with col_l:
        labels = ["Fijos Actuales", "Ocio (Ideal)", "Ahorro (Ideal)"]
        values = [total_fijos, oci_ideal, ahorro_ideal]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
        fig.update_layout(height=400, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    with col_r:
        st.subheader(t["veredicte_t"])
        if ratio_fijos <= 50: st.success(t["veredicto_ok"])
        else:
            st.error(t["veredicto_ko"])
            exces = total_fijos - (ing_val * 0.5)
            st.write(f"⚠️ Estás gastando **{int(exces)}€ de más** cada mes.")
        st.info(f"Tu disponible real para otros gastos es: **{int(ing_val - total_fijos)}€**")

with tab2:
    if not is_ready: st.warning("Introduce tus ingresos en el menú lateral.")
    else:
        est_int = max(0, (int_val - 20) * 12); est_llu = max(0, (0.18 - 0.11) * 3000)
        est_mob = max(0, (mob_val - 7) * 12); est_seg = max(0, (seg_val - 18) * 12)
        est_total = est_int + est_llu + est_mob + est_seg
        st.markdown(f"<div class='total-save-banner'>{t['total_ahorro_msg']} {round(est_total, 2)} € 💰</div>", unsafe_allow_html=True)
        def draw_offer(cia, p_nou, p_act, url, unitat="€", is_kwh=False):
            est = (p_act - p_nou) * 3000 if is_kwh else (p_act - p_nou) * 12
            st.markdown(f"<div class='company-box'><b>{cia}</b><br><span class='price-text'>{p_nou}{unitat}</span><br><span class='save-label'>{t['ahorro_anual']}{max(0, round(est,2))}€</span></div>", unsafe_allow_html=True)
            st.link_button(t["btn_save"], url, use_container_width=True)
        with st.expander("🚗 Buscador de Seguros de Coche", expanded=True):
            ca, cb, cc = st.columns(3)
            draw_offer("Qualitas", 18, seg_val, "https://google.com")
            draw_offer("Axa", 22, seg_val, "https://google.com")
            draw_offer("Mapfre", 28, seg_val, "https://google.com")
        col_l, col_r = st.columns(2)
        with col_l:
            with st.expander("🌐 Internet y Fibra"):
                draw_offer("Digi", 20, int_val, "https://google.com")
                draw_offer("Lowi", 24, int_val, "https://google.com")
        with col_r:
            with st.expander("💡 Luz"):
                draw_offer("Octopus", 0.11, 0.18, "https://google.com", "€/kWh", True)
                draw_offer("Naturgy", 0.13, 0.18, "https://google.com", "€/kWh", True)
                # --- TAB 3: CENTRO DE DEUDA ---
with tab3:
    st.header("🏛️ " + t["analisis_prof"])
    st.write("Analizaremos tus préstamos basándonos en los tipos de interés actuales del mercado.")

    with st.expander("➕ Añadir / Editar Deudas (Máximo 5)", expanded=True):
        cols = st.columns([2, 2, 1, 1])
        d_nom = cols[0].text_input("Nombre del préstamo", placeholder="Ej: Coche")
        d_tipus = cols[1].selectbox("Tipo", ["Hipoteca", "Préstamo Personal", "Revolving / Tarjeta", "Coche"])
        d_cuota = cols[2].number_input("Cuota mensual (€)", min_value=0.0)
        d_interes = cols[3].number_input("TIN (%)", min_value=0.0, step=0.1)
        
        if st.button("Añadir Deuda"):
            if len(st.session_state.deutes_lista) < 5:
                st.session_state.deutes_lista.append({"nom": d_nom, "tipus": d_tipus, "cuota": d_cuota, "interes": d_interes})
                st.rerun()

    if st.session_state.deutes_lista:
        for i, d in enumerate(st.session_state.deutes_lista):
            status_class = "neutral-debt"; consejo = ""; btn_txt = ""; link = "https://google.com"
            if d['tipus'] == "Hipoteca":
                if d['interes'] > 3.8: status_class = "bad-debt"; consejo = "❌ Muy caro. El mercado está al 2.8%."; btn_txt = "Mejorar Hipoteca"
                else: status_class = "good-debt"; consejo = "✅ Condiciones competitivas."
            elif d['tipus'] == "Revolving / Tarjeta":
                if d['interes'] > 18.0: status_class = "bad-debt"; consejo = "🚨 PELIGRO: Posible usura."; btn_txt = "Unificar Deuda"
            elif d['interes'] > 9.0: status_class = "bad-debt"; consejo = "❌ Interés alto."; btn_txt = "Refinanciar"
            else: status_class = "good-debt"; consejo = "✅ Interés correcto."

            c_d1, c_d2, c_d3 = st.columns([2, 3, 2])
            c_d1.write(f"**{d['nom']}** ({d['cuota']}€/mes)")
            c_d2.markdown(f"<div class='debt-alert {status_class}'>{d['interes']}%: {consejo}</div>", unsafe_allow_html=True)
            if btn_txt: c_d3.link_button(f"🔗 {btn_txt}", link)
            if st.button(f"Eliminar {i}"): st.session_state.deutes_lista.pop(i); st.rerun()

        st.divider()
        ratio_endeudamiento = (total_cuotas_deuda / ing_val) * 100
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Cuotas de Deuda", f"{total_cuotas_deuda} €")
        col_res2.metric("Ratio DTI", f"{ratio_endeudamiento:.1f}%", delta="-35% Máx")
        if ratio_endeudamiento > 35:
            st.error("🛑 Alerta: Deuda elevada. Recomendamos unificación.")
            st.link_button("🆘 Solicitar Reunificación", "https://google.com")

# --- TAB 4: INVERSIÓN ---
with tab4:
    st.header("📈 Test de Perfil y Plan de Inversión")
    with st.expander("📋 Test de Riesgo (10 Preguntas)", expanded=True):
        sc = 0
        q1 = st.selectbox("1. Edad", ["18-35", "36-50", "51+"])
        q2 = st.radio("2. ¿Qué harías si tu inversión cae un 20%?", ["Vender", "Mantener", "Comprar más"])
        # (Logica de puntuació simplificada per espai)
        if q1 == "18-35": sc += 2
        if q2 == "Comprar más": sc += 3
        perfil = "Conservador" if sc < 2 else ("Moderado" if sc < 4 else "Arriesgado")
        st.subheader(f"Tu perfil: **{perfil}**")

    def draw_inv(nom, risc, rent, desc, rec=False):
        css = "investment-card recommended" if rec else "investment-card"
        st.markdown(f"<div class='{css}'><h4>{nom} {'⭐' if rec else ''}</h4><b>Riesgo:</b> {risc} | <b>Rent:</b> {rent}<br>{desc}</div>", unsafe_allow_html=True)
        st.link_button("Saber más", "https://google.com")

    c1, c2, c3 = st.columns(3)
    with c1: draw_inv("Depósitos", "Bajo", "3%", "Seguridad total.", rec=(perfil=="Conservador"))
    with c2: draw_inv("Fondos Indexados", "Medio", "7-9%", "Crecimiento global.", rec=(perfil=="Moderado"))
    with c3: draw_inv("Cripto/Acciones", "Alto", "Variable", "Alta volatilidad.", rec=(perfil=="Arriesgado"))

with tab5:
    st.header("Conceptos Clave")
    st.info("La clave no es no tener deuda, sino que la deuda sea BARATA.")

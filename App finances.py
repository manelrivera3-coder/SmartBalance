import streamlit as st
import plotly.graph_objects as go

# 1. CONFIGURACIÓ DE LA PÀGINA
st.set_page_config(page_title="SmartBalance", layout="wide", page_icon="💰")

# Estils CSS Personalitzats per a tota l'app
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
    </style>
    """, unsafe_allow_html=True)

# 2. DICCIONARI DE TEXTOS
texts = {
    "Español": {
        "titol": "SmartBalance 💰",
        "tab1": "📊 Mi Radiografía",
        "tab2": "✂️ Plan de Ahorro",
        "tab3": "📉 Centro de Deuda",
        "tab4": "🎓 Educación",
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

# 3. SIDEBAR - ENTRADA DE DATOS PRINCIPALES
with st.sidebar:
    idioma = st.selectbox("Idioma", ["Español"])
    t = texts[idioma]
    st.header(t["gastos_f"])
    ing_val = st.number_input(t["ingresos_label"], min_value=1, value=2000)
    lloguer_val = st.number_input("Alquiler / Hipoteca (Cuota)", value=800)
    llum_val = st.number_input("Luz (Electricidad)", value=60)
    gas_val = st.number_input("Gas", value=30)
    aigua_val = st.number_input("Agua", value=20)
    int_val = st.number_input("Internet (Fibra)", value=35)
    mob_val = st.number_input("Móvil", value=15)
    seg_val = st.number_input(t["seguro_coche"], value=40)

# Inicializar lista de deudas en session_state para que no se borren al recargar
if 'deutes_lista' not in st.session_state:
    st.session_state.deutes_lista = []

# Calcular total cuotas de deuda de la Pestaña 3 para incluirlas en la Pestaña 1
total_cuotas_deuda = sum(d['cuota'] for d in st.session_state.deutes_lista)

# Cálculos Globales
total_fijos = lloguer_val + llum_val + gas_val + aigua_val + int_val + mob_val + seg_val + total_cuotas_deuda
ratio_fijos = (total_fijos / ing_val) * 100
oci_ideal = ing_val * 0.3
ahorro_ideal = ing_val * 0.2
is_ready = ing_val > 0 and total_fijos > 0

# 4. PESTAÑAS
tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

# --- TAB 1: RADIOGRAFÍA ---
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
        if ratio_fijos <= 50:
            st.success(t["veredicto_ok"])
        else:
            st.error(t["veredicto_ko"])
            exces = total_fijos - (ing_val * 0.5)
            st.write(f"⚠️ Estás gastando **{int(exces)}€ de más** cada mes. Mira la pestaña 'Plan de Ahorro'.")
        st.info(f"Para cumplir la regla 50/30/20, tus gastos fijos no deberían superar los **{int(ing_val * 0.5)}€**.")

# --- TAB 2: PLAN DE AHORRO ---
with tab2:
    if not is_ready:
        st.warning("Introduce tus ingresos en el menú lateral.")
    else:
        # Cálculo de ahorro potencial para el Banner
        est_int = max(0, (int_val - 20) * 12)
        est_llu = max(0, (0.18 - 0.11) * 3000)
        est_mob = max(0, (mob_val - 7) * 12)
        est_seg = max(0, (seg_val - 18) * 12)
        est_total = est_int + est_llu + est_mob + est_seg

        st.markdown(f"<div class='total-save-banner'>{t['total_ahorro_msg']} {round(est_total, 2)} € 💰</div>", unsafe_allow_html=True)

        def draw_offer(cia, p_nou, p_act, url, unitat="€", is_kwh=False):
            est = (p_act - p_nou) * 3000 if is_kwh else (p_act - p_nou) * 12
            st.markdown(f"<div class='company-box'><b>{cia}</b><br><span class='price-text'>{p_nou}{unitat}</span><br><span class='save-label'>{t['ahorro_anual']}{max(0, round(est,2))}€</span></div>", unsafe_allow_html=True)
            st.link_button(t["btn_save"], url, use_container_width=True)

        # SECCIÓN SEGURO COCHE
        with st.expander("🚗 Buscador de Seguros de Coche (Estilo Rastreator)", expanded=True):
            c1, c2, c3 = st.columns(3)
            with c1: marca = st.selectbox(t["f_marca"], ["Seat", "Toyota", "Audi", "BMW", "Otros"]); edat = st.number_input(t["f_edad"], 18, 90, 30)
            with c2: comb = st.selectbox(t["f_combustible"], ["Gasolina", "Diésel", "Híbrido"]); carnet = st.number_input(t["f_carnet"], 0, 70, 10)
            with c3: tipo_seg = st.selectbox("Cobertura", ["Terceros", "Todo Riesgo"])
            
            p_base = 18 if tipo_seg == "Terceros" else 45
            if edat < 25: p_base += 15
            
            ca, cb, cc = st.columns(3)
            with ca: draw_offer("Qualitas", p_base, seg_val, "https://google.com")
            with cb: draw_offer("Axa", round(p_base*1.1, 2), seg_val, "https://google.com")
            with cc: draw_offer("Mapfre", round(p_base*1.3, 2), seg_val, "https://google.com")

        # SECCIÓN INTERNET Y LUZ
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

        # SECCIÓN MÓVIL Y GAS
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

# --- TAB 3: CENTRO DE DEUDA ---
with tab3:
    st.header("🏛️ " + t["analisis_prof"])
    st.write("Analizaremos tus préstamos basándonos en los tipos de interés actuales del mercado (BCE/Banco de España).")

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
            else:
                st.error("Límite de 5 préstamos alcanzado.")

    if st.session_state.deutes_lista:
        st.subheader("Tu Análisis Personalizado")
        for i, d in enumerate(st.session_state.deutes_lista):
            # Lógica de asesor profesional
            status_class = "neutral-debt"
            consejo = ""
            btn_txt = ""
            link = "https://google.com" # Espacio para tus referidos

            if d['tipus'] == "Hipoteca":
                if d['interes'] > 3.8:
                    status_class = "bad-debt"; consejo = "❌ Muy caro. El mercado está al 2.8%."; btn_txt = "Mejorar Hipoteca"
                else:
                    status_class = "good-debt"; consejo = "✅ Condiciones competitivas."
            
            elif d['tipus'] == "Revolving / Tarjeta":
                if d['interes'] > 18.0:
                    status_class = "bad-debt"; consejo = "🚨 PELIGRO: Posible usura. ¡Reclama o unifica!"; btn_txt = "Unificar Deuda"
                else:
                    status_class = "neutral-debt"; consejo = "⚠️ Interés alto. Evita usar tarjetas."

            elif d['tipus'] == "Préstamo Personal" or d['tipus'] == "Coche":
                if d['interes'] > 9.0:
                    status_class = "bad-debt"; consejo = "❌ Interés alto. Podrías bajarlo al 7%."; btn_txt = "Refinanciar"
                else:
                    status_class = "good-debt"; consejo = "✅ Interés dentro de mercado."

            # Renderizado de fila de deuda
            c_d1, c_d2, c_d3 = st.columns([2, 3, 2])
            c_d1.write(f"**{d['nom']}** ({d['cuota']}€/mes)")
            c_d2.markdown(f"<div class='debt-alert {status_class}'>{d['interes']}%: {consejo}</div>", unsafe_allow_html=True)
            if btn_txt:
                c_d3.link_button(f"🔗 {btn_txt}", link)
            
            if st.button(f"Eliminar {i}", key=f"del_{i}"):
                st.session_state.deutes_lista.pop(i)
                st.rerun()

        st.divider()
        ratio_endeudamiento = (total_cuotas_deuda / ing_val) * 100
        st.subheader("Ratio de Endeudamiento Total")
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Cuotas de Deuda", f"{total_cuotas_deuda} €")
        col_res2.metric("Ratio DTI", f"{ratio_endeudamiento:.1f}%", delta="-35% Máx")

        if ratio_endeudamiento > 35:
            st.error("🛑 **Alerta:** Tu deuda supera el 35% de tus ingresos. Recomendamos una **Reunificación de Deuda** para bajar la cuota total.")
            st.link_button("🆘 Solicitar Reunificación", "https://google.com")

# --- TAB 4: EDUCACIÓN ---
with tab4:
    st.header("Conceptos Clave")
    st.write("1. **¿Qué es un buen interés?**")
    st.write("- Hipotecas: < 3.5% TIN")
    st.write("- Préstamos personales: < 8% TIN")
    st.write("- Tarjetas Revolving: > 20% suele ser reclamable.")
    st.info("La clave no es no tener deuda, sino que la deuda sea BARATA y no supere el 35% de tus ingresos.")

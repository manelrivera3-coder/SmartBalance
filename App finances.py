import streamlit as st
import plotly.graph_objects as go

# 1. CONFIGURACIÓ DE LA PÀGINA
st.set_page_config(page_title="SmartBalance", layout="wide", page_icon="💰")

# Estils CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .company-box { 
        background-color: #ffffff; 
        padding: 10px; 
        border-radius: 8px; 
        border: 1px solid #e0e0e0; 
        text-align: center; 
        min-height: 140px;
    }
    .company-box img { margin-bottom: 5px; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# 2. DICCIONARI DE TEXTOS
texts = {
    "Español": {
        "titol": "SmartBalance 💰",
        "subtitol": "Ordena tus finanzas y construye tu futuro",
        "tab1": "📊 Mi Radiografía",
        "tab2": "✂️ Plan de Ahorro",
        "tab3": "📈 Inversión",
        "tab4": "🎓 Educación",
        "ingresos_label": "Ingresos mensuales netos (€)",
        "gastos_f": "Gastos Fijos Mensuales",
        "lloguer": "Alquiler / Hipoteca",
        "internet": "Internet (Fibra)",
        "mobil": "Móvil",
        "llum": "Luz (Electricidad)",
        "gas": "Gas",
        "aigua": "Agua",
        "deutes": "Préstamos / Deudas",
        "total_gastos": "Total Gastos Fijos (50%)",
        "oci_recom": "Presupuesto Ocio (30%)",
        "ahorro_recom": "Objetivo Ahorro (20%)",
        "ratio_label": "% de tus ingresos",
        "veredicte": "Tu Veredicto Financiero",
        "error_bloqueo": "⚠️ Por favor, completa tus datos en la pestaña 'Mi Radiografía' para desbloquear el resto.",
        "btn_save": "Ver Oferta",
        "ahorro_anual": "Ahorro anual estimado",
        "perfecto": "¡Precio perfecto!",
        "simulador_t": "Simulador de Crecimiento",
        "años": "Años",
        "inv_mensual": "Inversión mensual (€)",
        "resultado_inv": "En {0} años podrías tener: {1} €",
        "search_btn": "Buscar mejores ofertas",
        "filtro_fibra": "Velocidad Fibra",
        "filtro_mobil": "Datos Móvil",
        "filtro_llum": "Tipo de Tarifa",
        "filtro_gas": "Consumo estimado"
    },
    "English": {
        "titol": "SmartBalance 💰",
        "subtitol": "Organize your finances and build your future",
        "tab1": "📊 My Radiography",
        "tab2": "✂️ Saving Plan",
        "tab3": "📈 Investment",
        "tab4": "🎓 Education",
        "ingresos_label": "Net Monthly Income (€)",
        "gastos_f": "Monthly Fixed Expenses",
        "lloguer": "Rent / Mortgage",
        "internet": "Internet (Fiber)",
        "mobil": "Mobile",
        "llum": "Power (Electricity)",
        "gas": "Gas",
        "aigua": "Water",
        "deutes": "Loans / Debts",
        "total_gastos": "Total Fixed Expenses (50%)",
        "oci_recom": "Leisure Budget (30%)",
        "ahorro_recom": "Savings Goal (20%)",
        "ratio_label": "% of your income",
        "veredicte": "Your Financial Verdict",
        "error_bloqueo": "⚠️ Please, fill in your data in the 'My Radiography' tab to unlock the rest.",
        "btn_save": "View Offer",
        "ahorro_anual": "Estimated annual savings",
        "perfecto": "Perfect price!",
        "simulador_t": "Growth Simulator",
        "años": "Years",
        "inv_mensual": "Monthly Investment (€)",
        "resultado_inv": "In {0} years you could have: {1} €",
        "search_btn": "Search best offers",
        "filtro_fibra": "Fiber Speed",
        "filtro_mobil": "Mobile Data",
        "filtro_llum": "Rate Type",
        "filtro_gas": "Estimated Consumption"
    }
}

# 3. SIDEBAR
with st.sidebar:
    idioma = st.selectbox("Language / Idioma", ["Español", "English"])
    t = texts[idioma]
    st.divider()
    st.header(t["gastos_f"])
    ingresos_val = st.number_input(t["ingresos_label"], min_value=0, value=0, step=100)
    lloguer_val = st.number_input(t["lloguer"], min_value=0, value=0)
    llum_val = st.number_input(t["llum"], min_value=0, value=0)
    gas_val = st.number_input(t["gas"], min_value=0, value=0)
    aigua_val = st.number_input(t["aigua"], min_value=0, value=0)
    internet_val = st.number_input(t["internet"], min_value=0, value=0)
    mobil_val = st.number_input(t["mobil"], min_value=0, value=0)
    deute_val = st.number_input(t["deutes"], min_value=0, value=0)

# Càlculs
total_gastos = lloguer_val + llum_val + gas_val + aigua_val + internet_val + mobil_val + deute_val
ratio = (total_gastos / ingresos_val * 100) if ingresos_val > 0 else 0
disponible_total = max(0, ingresos_val - total_gastos)
oci_real = disponible_total * 0.6 if ratio > 50 else ingresos_val * 0.3
ahorro_real = disponible_total * 0.4 if ratio > 50 else ingresos_val * 0.2
is_ready = ingresos_val > 0 and total_gastos > 0

# 4. PESTANYES
tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

# --- TAB 1: RADIOGRAFIA ---
with tab1:
    st.title(t["titol"])
    st.write(t["subtitol"])
    if ingresos_val == 0: st.info(t["error_bloqueo"])
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t["total_gastos"], f"{total_gastos} €")
    c2.metric(t["ratio_label"], f"{ratio:.1f}%", delta="-50%" if ratio > 50 else "OK", delta_color="inverse" if ratio > 50 else "normal")
    c3.metric(t["oci_recom"], f"{int(oci_real)} €")
    c4.metric(t["ahorro_recom"], f"{int(ahorro_real)} €")

    if is_ready:
        st.divider()
        col_l, col_r = st.columns(2)
        with col_l:
            labels = [t["lloguer"], t["llum"], t["gas"], t["aigua"], t["internet"], t["mobil"], t["deutes"], t["oci_recom"], t["ahorro_recom"]]
            values = [lloguer_val, llum_val, gas_val, aigua_val, internet_val, mobil_val, deute_val, oci_real, ahorro_real]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            st.subheader(t["veredicte"])
            if ratio > 50: st.error("🚨" + (" Gastos altos." if idioma == "Español" else " High expenses."))
            else: st.success("✅" + (" Controlado." if idioma == "Español" else " Controlled."))
            score = max(0, 100 - int(ratio))
            st.write(f"**Score: {score}/100**")
            st.progress(score / 100)

# --- TAB 2: PLAN DE AHORRO (FILTRAT FINET) ---
with tab2:
    if not is_ready:
        st.warning(t["error_bloqueo"])
    else:
        st.header(t["tab2"])
        
        # --- SECCIÓ INTERNET ---
        with st.expander("🌐 " + t["internet"], expanded=True):
            f_fibra = st.select_slider(t["filtro_fibra"], options=["300Mb", "600Mb", "1Gb"])
            db_int = {
                "300Mb": [{"cia": "Digi", "p": 20.0, "d": "digimobil.es"}, {"cia": "Lowi", "p": 24.0, "d": "lowi.es"}, {"cia": "O2", "p": 27.0, "d": "o2online.es"}],
                "600Mb": [{"cia": "Digi", "p": 25.0, "d": "digimobil.es"}, {"cia": "Lowi", "p": 29.0, "d": "lowi.es"}, {"cia": "O2", "p": 31.0, "d": "o2online.es"}],
                "1Gb": [{"cia": "Digi", "p": 30.0, "d": "digimobil.es"}, {"cia": "Simyo", "p": 32.0, "d": "simyo.es"}, {"cia": "Vodafone", "p": 40.0, "d": "vodafone.es"}]
            }
            cols = st.columns(3)
            for i, of in enumerate(db_int[f_fibra]):
                with cols[i]:
                    st.markdown(f"<div class='company-box'><img src='https://logo.clearbit.com/{of['d']}' width='40'><br><b>{of['cia']}</b><br>{of['p']}€</div>", unsafe_allow_html=True)
                    st.link_button(t["btn_save"], f"https://{of['d']}", use_container_width=True)

        # --- SECCIÓ MÒBIL ---
        with st.expander("📲 " + t["mobil"], expanded=True):
            f_mob = st.select_slider(t["filtro_mobil"], options=["10GB", "50GB", "Unlimited"])
            db_mob = {
                "10GB": [{"cia": "Simyo", "p": 7.0, "d": "simyo.es"}, {"cia": "Lowi", "p": 7.9, "d": "lowi.es"}, {"cia": "Digi", "p": 8.0, "d": "digimobil.es"}],
                "50GB": [{"cia": "Pepephone", "p": 14.9, "d": "pepephone.com"}, {"cia": "O2", "p": 15.0, "d": "o2online.es"}, {"cia": "Finetwork", "p": 16.0, "d": "finetwork.com"}],
                "Unlimited": [{"cia": "Vodafone", "p": 25.0, "d": "vodafone.es"}, {"cia": "Movistar", "p": 30.0, "d": "movistar.es"}, {"cia": "Orange", "p": 32.0, "d": "orange.es"}]
            }
            cols = st.columns(3)
            for i, of in enumerate(db_mob[f_mob]):
                with cols[i]:
                    st.markdown(f"<div class='company-box'><img src='https://logo.clearbit.com/{of['d']}' width='40'><br><b>{of['cia']}</b><br>{of['p']}€</div>", unsafe_allow_html=True)
                    st.link_button(t["btn_save"], f"https://{of['d']}", use_container_width=True)

        # --- SECCIÓ LLUM I GAS ---
        c_l, c_g = st.columns(2)
        with c_l:
            with st.expander("💡 " + t["llum"], expanded=True):
                st.selectbox(t["filtro_llum"], ["Tarifa Fija", "Indexada (Variable)", "Discriminación Horaria"])
                for of in [{"cia": "Octopus", "p": "Bajo", "d": "octopusenergy.es"}, {"cia": "Naturgy", "p": "Fijo", "d": "naturgy.es"}]:
                    st.markdown(f"<div class='company-box' style='min-height:100px'><img src='https://logo.clearbit.com/{of['d']}' width='35'><br><b>{of['cia']}</b></div>", unsafe_allow_html=True)
                    st.link_button(t["btn_save"], f"https://{of['d']}", use_container_width=True)
        with c_g:
            with st.expander("🔥 " + t["gas"], expanded=True):
                st.selectbox(t["filtro_gas"], ["< 5.000 kWh/año", "> 5.000 kWh/año"])
                for of in [{"cia": "Endesa", "p": "TUR", "d": "endesa.com"}, {"cia": "Total", "p": "Ahorro", "d": "totalenergies.es"}]:
                    st.markdown(f"<div class='company-box' style='min-height:100px'><img src='https://logo.clearbit.com/{of['d']}' width='35'><br><b>{of['cia']}</b></div>", unsafe_allow_html=True)
                    st.link_button(t["btn_save"], f"https://{of['d']}", use_container_width=True)

# --- TAB 3: INVERSIÓN ---
with tab3:
    if not is_ready: st.warning(t["error_bloqueo"])
    else:
        st.header(t["simulador_t"])
        perf = st.select_slider("Perfil", options=["Conservador", "Moderado", "Decidido"])
        anys = st.slider(t["años"], 1, 30, 10)
        inv = st.slider(t["inv_mensual"], 0, int(ingresos_val), int(ahorro_real))
        r = 0.03 if perf == "Conservador" else (0.05 if perf == "Moderado" else 0.08)
        final = 0
        for _ in range(anys * 12): final = (final + inv) * (1 + r/12)
        st.success(t["resultado_inv"].format(anys, f"{final:,.0f}"))

# --- TAB 4: EDUCACIÓN ---
with tab4:
    st.header(t["tab4"])
    st.write("Academy 🎓")

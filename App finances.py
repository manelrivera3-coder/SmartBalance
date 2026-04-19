import streamlit as st
import plotly.graph_objects as go

# 1. CONFIGURACIÓ DE LA PÀGINA
st.set_page_config(page_title="SmartBalance", layout="wide", page_icon="💰")

# Estils CSS Millorats (Més compacte i correcció de logos)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .company-box { 
        background-color: #ffffff; 
        padding: 12px 5px; 
        border-radius: 10px; 
        border: 1px solid #eee; 
        text-align: center; 
        min-height: 150px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .logo-img {
        width: 50px;
        height: 50px;
        object-fit: contain;
        margin-bottom: 8px;
        background-color: white;
        border-radius: 5px;
    }
    .price-text {
        font-size: 1.1rem;
        font-weight: bold;
        color: #1E1E1E;
    }
    .save-badge {
        background-color: #D4EDDA;
        color: #155724;
        padding: 1px 6px;
        border-radius: 8px;
        font-size: 0.7rem;
        margin-top: 4px;
    }
    /* Estil per fer els expanders més compactes */
    .st-expander { border: none !important; box-shadow: none !important; margin-bottom: -10px !important; }
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
        "error_bloqueo": "⚠️ Por favor, completa tus datos en la pestaña 'Mi Radiografía'.",
        "btn_save": "Ver Oferta",
        "ahorro_anual": "Ahorro anual estimado",
        "perfecto": "¡Precio perfecto!",
        "simulador_t": "Simulador de Crecimiento",
        "años": "Años",
        "inv_mensual": "Inversión mensual (€)",
        "resultado_inv": "En {0} años podrías tener: {1} €",
        "preu_kwh_actual": "¿A cuánto pagas el kWh? (€)",
        "mejorar_oferta": "Mejores opciones para ti:",
        "filtro_fibra": "Velocidad Fibra",
        "filtro_mobil": "Datos Móvil",
        "filtro_gas": "Uso de Gas"
    },
    "English": {
        "titol": "SmartBalance 💰",
        "subtitol": "Organize your finances",
        "tab1": "📊 My Radiography",
        "tab2": "✂️ Saving Plan",
        "tab3": "📈 Investment",
        "tab4": "🎓 Education",
        "ingresos_label": "Net Income (€)",
        "gastos_f": "Fixed Expenses",
        "lloguer": "Rent / Mortgage",
        "internet": "Internet",
        "mobil": "Mobile",
        "llum": "Power",
        "gas": "Gas",
        "aigua": "Water",
        "deutes": "Debts",
        "total_gastos": "Total Fixed (50%)",
        "oci_recom": "Leisure (30%)",
        "ahorro_recom": "Savings (20%)",
        "ratio_label": "% of income",
        "veredicte": "Financial Verdict",
        "error_bloqueo": "⚠️ Fill data in 'My Radiography'.",
        "btn_save": "View Offer",
        "ahorro_anual": "Annual savings",
        "perfecto": "Perfect price!",
        "simulador_t": "Growth Simulator",
        "años": "Years",
        "inv_mensual": "Monthly Invest (€)",
        "resultado_inv": "In {0} years: {1} €",
        "preu_kwh_actual": "Price per kWh (€)",
        "mejorar_oferta": "Best options for you:",
        "filtro_fibra": "Fiber Speed",
        "filtro_mobil": "Mobile Data",
        "filtro_gas": "Gas Usage"
    }
}

# 3. SIDEBAR
with st.sidebar:
    idioma = st.selectbox("Language / Idioma", ["Español", "English"])
    t = texts[idioma]
    st.header(t["gastos_f"])
    ingresos_val = st.number_input(t["ingresos_label"], min_value=0, value=2000, step=100)
    lloguer_val = st.number_input(t["lloguer"], min_value=0, value=800)
    llum_val = st.number_input(t["llum"], min_value=0, value=60)
    gas_val = st.number_input(t["gas"], min_value=0, value=30)
    aigua_val = st.number_input(t["aigua"], min_value=0, value=20)
    internet_val = st.number_input(t["internet"], min_value=0, value=35)
    mobil_val = st.number_input(t["mobil"], min_value=0, value=15)
    deute_val = st.number_input(t["deutes"], min_value=0, value=0)

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
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t["total_gastos"], f"{total_gastos} €")
    c2.metric(t["ratio_label"], f"{ratio:.1f}%")
    c3.metric(t["oci_recom"], f"{int(oci_real)} €")
    c4.metric(t["ahorro_recom"], f"{int(ahorro_real)} €")
    if is_ready:
        col_l, col_r = st.columns(2)
        with col_l:
            labels = [t["lloguer"], t["llum"], t["gas"], t["aigua"], t["internet"], t["mobil"], t["deutes"], t["oci_recom"], t["ahorro_recom"]]
            values = [lloguer_val, llum_val, gas_val, aigua_val, internet_val, mobil_val, deute_val, oci_real, ahorro_real]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            st.subheader(t["veredicte"])
            score = max(0, 100 - int(ratio))
            st.write(f"**Score: {score}/100**")
            st.progress(score / 100)

# --- TAB 2: PLAN DE AHORRO ---
with tab2:
    if not is_ready:
        st.warning(t["error_bloqueo"])
    else:
        # Funció per dibuixar caixes
        def draw_offer_box(cia, preu, domain, unitat="€"):
            logo_url = f"https://logo.clearbit.com/{domain}"
            st.markdown(f"""
                <div class='company-box'>
                    <img src='{logo_url}' class='logo-img' onerror="this.src='https://via.placeholder.com/50?text={cia}'">
                    <b>{cia}</b>
                    <div class='price-text'>{preu}{unitat}</div>
                </div>
            """, unsafe_allow_html=True)
            st.link_button(t["btn_save"], f"https://{domain}", use_container_width=True)

        # 1. INTERNET
        with st.expander("🌐 " + t["internet"], expanded=True):
            f_fib = st.select_slider(t["filtro_fibra"], options=["300Mb", "600Mb", "1Gb"])
            db_int = {
                "300Mb": [("Digi", 20, "digimobil.es"), ("Lowi", 24, "lowi.es"), ("O2", 27, "o2online.es")],
                "600Mb": [("Digi", 25, "digimobil.es"), ("Lowi", 29, "lowi.es"), ("O2", 31, "o2online.es")],
                "1Gb": [("Digi", 30, "digimobil.es"), ("Simyo", 32, "simyo.es"), ("Vodafone", 40, "vodafone.es")]
            }
            c = st.columns(3)
            for i, of in enumerate(db_int[f_fib]):
                with c[i]: draw_offer_box(of[0], of[1], of[2])

        # 2. LLUM
        with st.expander("💡 " + t["llum"], expanded=True):
            kwh = st.number_input(t["preu_kwh_actual"], 0.0, 0.50, 0.18, 0.01)
            db_llu = [("Octopus", 0.12, "octopusenergy.es"), ("Naturgy", 0.13, "naturgy.es"), ("Endesa", 0.14, "endesa.com")]
            c = st.columns(3)
            for i, of in enumerate(db_llu):
                with c[i]: draw_offer_box(of[0], of[1], of[2], "€/kWh")

        # 3. MÒBIL
        with st.expander("📲 " + t["mobil"], expanded=True):
            f_mob = st.select_slider(t["filtro_mobil"], options=["20GB", "100GB", "Unlimited"])
            db_mob = {
                "20GB": [("Simyo", 7, "simyo.es"), ("Lowi", 8, "lowi.es"), ("Digi", 10, "digimobil.es")],
                "100GB": [("Pepephone", 15, "pepephone.com"), ("O2", 15, "o2online.es"), ("Finetwork", 16, "finetwork.com")],
                "Unlimited": [("Vodafone", 25, "vodafone.es"), ("Movistar", 30, "movistar.es"), ("Orange", 32, "orange.es")]
            }
            c = st.columns(3)
            for i, of in enumerate(db_mob[f_mob]):
                with c[i]: draw_offer_box(of[0], of[1], of[2])

        # 4. GAS
        with st.expander("🔥 " + t["gas"], expanded=True):
            f_gas = st.selectbox(t["filtro_gas"], ["RL.1 (Agua/Cocina)", "RL.2 (Calefacción)"])
            db_gas = [("Naturgy", "TUR 1", "naturgy.es"), ("Endesa", "TUR 1", "endesa.com"), ("TotalEnergies", "Facil", "totalenergies.es")]
            c = st.columns(3)
            for i, of in enumerate(db_gas):
                with c[i]: draw_offer_box(of[0], of[1], of[2], "")

# --- TAB 3: INVERSIÓN ---
with tab3:
    if is_ready:
        st.header(t["simulador_t"])
        perf = st.select_slider("Perfil", options=["Conservador", "Moderado", "Decidido"])
        anys = st.slider(t["años"], 1, 30, 10)
        inv = st.slider(t["inv_mensual"], 0, int(ingresos_val), int(ahorro_real))
        r = 0.03 if "Cons" in perf else (0.05 if "Mod" in perf else 0.08)
        final = 0
        for _ in range(anys * 12): final = (final + inv) * (1 + r/12)
        st.success(t["resultado_inv"].format(anys, f"{final:,.0f}"))

# --- TAB 4: EDUCACIÓN ---
with tab4:
    st.header(t["tab4"])
    st.info("Regla 50/30/20: 50% Necesidades, 30% Ocio, 20% Ahorro.")

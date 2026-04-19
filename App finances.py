import streamlit as st
import plotly.graph_objects as go

# 1. CONFIGURACIÓ DE LA PÀGINA
st.set_page_config(page_title="SmartBalance", layout="wide", page_icon="💰")

# Estils CSS (Sense logos, més net i enfocat a l'estalvi)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .company-box { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #e0e0e0; 
        text-align: center; 
        margin-bottom: 5px;
    }
    .price-text {
        font-size: 1.3rem;
        font-weight: bold;
        color: #1E1E1E;
    }
    .save-label {
        color: #28a745;
        font-weight: bold;
        font-size: 0.9rem;
        margin-top: 5px;
    }
    .st-expander { border: none !important; }
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
        "btn_save": "Contratar Oferta",
        "ahorro_anual": "Ahorro anual: ",
        "perfecto": "¡Precio perfecto!",
        "simulador_t": "Simulador de Crecimiento",
        "años": "Años",
        "inv_mensual": "Inversión mensual (€)",
        "resultado_inv": "En {0} años podrías tener: {1} €",
        "preu_kwh_actual": "¿A cuánto pagas el kWh? (€)",
        "filtro_fibra": "Velocidad Fibra",
        "filtro_mobil": "Datos Móvil",
        "filtro_gas": "Tipo de consumo"
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
        "veredicte": "Verdict",
        "error_bloqueo": "⚠️ Fill data in 'My Radiography'.",
        "btn_save": "Get Offer",
        "ahorro_anual": "Annual savings: ",
        "perfecto": "Perfect price!",
        "simulador_t": "Growth Simulator",
        "años": "Years",
        "inv_mensual": "Monthly Invest (€)",
        "resultado_inv": "In {0} years: {1} €",
        "preu_kwh_actual": "Price per kWh (€)",
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
        st.divider()
        col_l, col_r = st.columns(2)
        with col_l:
            labels = [t["lloguer"], t["llum"], t["gas"], t["aigua"], t["internet"], t["mobil"], t["deutes"], t["oci_recom"], t["ahorro_recom"]]
            values = [lloguer_val, llum_val, gas_val, aigua_val, internet_val, mobil_val, deute_val, oci_real, ahorro_real]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=350)
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            st.subheader(t["veredicte"])
            score = max(0, 100 - int(ratio))
            st.write(f"**Score: {score}/100**")
            st.progress(score / 100)

# --- TAB 2: PLAN DE AHORRO (SENSE LOGOS + ESTALVI ANUAL) ---
with tab2:
    if not is_ready:
        st.warning(t["error_bloqueo"])
    else:
        st.header(t["tab2"])

        def draw_offer_card(cia, preu_nou, preu_actual, unitat="€", is_kwh=False):
            # Càlcul de l'estalvi anual
            if is_kwh:
                # Simulació basada en un consum mitjà de 3000 kWh/any si és llum
                estalvi_anual = (preu_actual - preu_nou) * 3000 if preu_actual > preu_nou else 0
            else:
                estalvi_anual = (preu_actual - preu_nou) * 12 if preu_actual > preu_nou else 0
            
            st.markdown(f"""
                <div class='company-box'>
                    <small>PROVEEDOR</small><br>
                    <b>{cia}</b><br>
                    <div class='price-text'>{preu_nou}{unitat}</div>
                    {"<div class='save-label'>" + t['ahorro_anual'] + str(round(estalvi_anual, 2)) + "€</div>" if estalvi_anual > 0 else ""}
                </div>
            """, unsafe_allow_html=True)
            st.link_button(t["btn_save"], "https://google.com", use_container_width=True)

        # 1. INTERNET
        with st.expander("🌐 " + t["internet"], expanded=True):
            f_fib = st.select_slider(t["filtro_fibra"], options=["300Mb", "600Mb", "1Gb"])
            db_int = {
                "300Mb": [("Digi", 20), ("Lowi", 24), ("O2", 27)],
                "600Mb": [("Digi", 25), ("Lowi", 29), ("O2", 31)],
                "1Gb": [("Digi", 30), ("Simyo", 32), ("Vodafone", 40)]
            }
            c = st.columns(3)
            for i, of in enumerate(db_int[f_fib]):
                with c[i]: draw_offer_card(of[0], of[1], internet_val)

        # 2. LLUM
        with st.expander("💡 " + t["llum"], expanded=True):
            kwh_usuari = st.number_input(t["preu_kwh_actual"], 0.0, 0.50, 0.18)
            db_llu = [("Octopus", 0.12), ("Naturgy", 0.13), ("Endesa", 0.14)]
            c = st.columns(3)
            for i, of in enumerate(db_llu):
                with c[i]: draw_offer_card(of[0], of[1], kwh_usuari, "€/kWh", True)

        # 3. MÒBIL
        with st.expander("📲 " + t["mobil"], expanded=True):
            f_mob = st.select_slider(t["filtro_mobil"], options=["20GB", "100GB", "Unlimited"])
            db_mob = {
                "20GB": [("Simyo", 7), ("Lowi", 8), ("Digi", 10)],
                "100GB": [("Pepephone", 14), ("O2", 15), ("Finetwork", 16)],
                "Unlimited": [("Vodafone", 25), ("Movistar", 30), ("Orange", 32)]
            }
            c = st.columns(3)
            for i, of in enumerate(db_mob[f_mob]):
                with c[i]: draw_offer_card(of[0], of[1], mobil_val)

        # 4. GAS
        with st.expander("🔥 " + t["gas"], expanded=True):
            f_gas = st.selectbox(t["filtro_gas"], ["RL.1 (Agua/Cocina)", "RL.2 (Calefacción)"])
            db_gas = [("Naturgy", 20), ("Endesa", 22), ("TotalEnergies", 23)]
            c = st.columns(3)
            for i, of in enumerate(db_gas):
                with c[i]: draw_offer_card(of[0], of[1], gas_val)

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
    st.info("Regla 50/30/20: 50% Gastos Fijos, 30% Ocio, 20% Ahorro.")

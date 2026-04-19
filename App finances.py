import streamlit as st
import plotly.graph_objects as go

# 1. CONFIGURACIÓ DE LA PÀGINA
st.set_page_config(page_title="SmartBalance", layout="wide", page_icon="💰")

# Estils CSS (Nets, sense trencar les pestanyes)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .company-box { 
        background-color: #ffffff; 
        padding: 15px 10px; 
        border-radius: 8px; 
        border: 1px solid #e0e0e0; 
        text-align: center; 
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DICCIONARI DE TEXTOS (Traducció 100%)
texts = {
    "Español": {
        "setup": "Configuración",
        "idioma": "Idioma",
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
        "disponible": "Disponible Total",
        "ratio_label": "% de tus ingresos",
        "veredicte": "Tu Veredicto Financiero",
        "error_bloqueo": "⚠️ Por favor, completa tus datos en la pestaña 'Mi Radiografía' para desbloquear el resto.",
        "btn_save": "Contratar Oferta",
        "ahorro_anual": "Ahorro anual estimado",
        "perfecto": "¡Precio perfecto!",
        "perfil_riesgo": "Tu perfil de riesgo",
        "perfils": ["Conservador", "Moderado", "Decidido"],
        "simulador_t": "Simulador de Crecimiento",
        "años": "Años",
        "inv_mensual": "Inversión mensual (€)",
        "resultado_inv": "En {0} años podrías tener: {1} €",
        "top_3": "Top 3 mejores ofertas actuales:"
    },
    "English": {
        "setup": "Setup",
        "idioma": "Language",
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
        "disponible": "Total Available",
        "ratio_label": "% of your income",
        "veredicte": "Your Financial Verdict",
        "error_bloqueo": "⚠️ Please, fill in your data in the 'My Radiography' tab to unlock the rest.",
        "btn_save": "Get Offer",
        "ahorro_anual": "Estimated annual savings",
        "perfecto": "Perfect price!",
        "perfil_riesgo": "Your risk profile",
        "perfils": ["Conservative", "Moderate", "Aggressive"],
        "simulador_t": "Growth Simulator",
        "años": "Years",
        "inv_mensual": "Monthly Investment (€)",
        "resultado_inv": "In {0} years you could have: {1} €",
        "top_3": "Top 3 best current offers:"
    }
}

# 3. SIDEBAR - SELECCIÓ D'IDIOMA I INPUTS
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

# Càlculs base
total_gastos = lloguer_val + llum_val + gas_val + aigua_val + internet_val + mobil_val + deute_val
ratio = (total_gastos / ingresos_val * 100) if ingresos_val > 0 else 0
disponible_total = max(0, ingresos_val - total_gastos)
oci_real = disponible_total * 0.6 if ratio > 50 else ingresos_val * 0.3
ahorro_real = disponible_total * 0.4 if ratio > 50 else ingresos_val * 0.2
is_ready = ingresos_val > 0 and total_gastos > 0

# 4. PESTANYES
tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

# --- TAB 1: RADIOGRAFIA (Restaurada exactament com la tenies) ---
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

# --- TAB 2: PLAN DE AHORRO (Amb logos i gas) ---
with tab2:
    if not is_ready:
        st.warning(t["error_bloqueo"])
    else:
        st.header(t["tab2"])
        
        # Base de dades d'ofertes amb preus numèrics i domini (per extreure el logo)
        db_ofertes = {
            "internet": [
                {"cia": "Digi", "preu": 25.0, "link": "https://digimobil.es", "domain": "digimobil.es"},
                {"cia": "Lowi", "preu": 29.9, "link": "https://lowi.es", "domain": "lowi.es"},
                {"cia": "O2", "preu": 35.0, "link": "https://o2online.es", "domain": "o2online.es"}
            ],
            "mobil": [
                {"cia": "Simyo", "preu": 7.0, "link": "https://simyo.es", "domain": "simyo.es"},
                {"cia": "Pepephone", "preu": 10.0, "link": "https://pepephone.com", "domain": "pepephone.com"},
                {"cia": "Finetwork", "preu": 12.0, "link": "https://finetwork.com", "domain": "finetwork.com"}
            ],
            "llum": [
                {"cia": "Octopus", "preu": 40.0, "link": "https://octopusenergy.es", "domain": "octopusenergy.es"},
                {"cia": "Naturgy", "preu": 45.0, "link": "https://naturgy.es", "domain": "naturgy.es"},
                {"cia": "Endesa", "preu": 50.0, "link": "https://endesa.com", "domain": "endesa.com"}
            ],
            "gas": [
                {"cia": "Naturgy", "preu": 25.0, "link": "https://naturgy.es", "domain": "naturgy.es"},
                {"cia": "Endesa", "preu": 28.0, "link": "https://endesa.com", "domain": "endesa.com"},
                {"cia": "TotalEnergies", "preu": 30.0, "link": "https://totalenergies.es", "domain": "totalenergies.es"}
            ]
        }

        def mostrar_seccio_estalvi(icona, titol, valor_actual, clau_db):
            st.subheader(f"{icona} {titol}")
            best_price = db_ofertes[clau_db][0]["preu"]
            
            # Alerta d'estalvi
            if valor_actual > best_price:
                st.warning(f"💡 {t['ahorro_anual']}: {(valor_actual - best_price)*12:.2f} €")
            else:
                st.success(t["perfecto"])

            cols = st.columns(3)
            for i, oferta in enumerate(db_ofertes[clau_db]):
                with cols[i]:
                    # Codi HTML per mostrar el logo des de Clearbit, el nom en negreta i el preu
                    st.markdown(f"""
                    <div class='company-box'>
                        <img src='https://logo.clearbit.com/{oferta["domain"]}' width='45' style='margin-bottom:8px; border-radius:4px;' onerror="this.style.display='none'">
                        <br><b>{oferta['cia']}</b><br>{oferta['preu']}€
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button(t["btn_save"], oferta["link"], use_container_width=True)
            st.divider()

        # Crides a la funció amb les icones sol·licitades
        mostrar_seccio_estalvi("🌐", t["internet"], internet_val, "internet")
        mostrar_seccio_estalvi("📲", t["mobil"], mobil_val, "mobil")
        mostrar_seccio_estalvi("💡", t["llum"], llum_val, "llum")
        mostrar_seccio_estalvi("🔥", t["gas"], gas_val, "gas")

# --- TAB 3: INVERSIÓN ---
with tab3:
    if not is_ready: st.warning(t["error_bloqueo"])
    else:
        st.header(t["simulador_t"])
        perf = st.select_slider(t["perfil_riesgo"], options=t["perfils"])
        anys = st.slider(t["años"], 1, 30, 10)
        inv = st.slider(t["inv_mensual"], 0, int(ingresos_val), int(ahorro_real))
        r = 0.03 if perf == t["perfils"][0] else (0.05 if perf == t["perfils"][1] else 0.08)
        final = 0
        for _ in range(anys * 12): final = (final + inv) * (1 + r/12)
        st.success(t["resultado_inv"].format(anys, f"{final:,.0f}"))

# --- TAB 4: EDUCACIÓN ---
with tab4:
    st.header(t["tab4"])
    st.write("Contenido educativo en desarrollo...")

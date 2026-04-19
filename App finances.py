import streamlit as st
import plotly.graph_objects as go

# 1. CONFIGURACIÓ DE LA PÀGINA
st.set_page_config(page_title="SmartBalance", layout="wide", page_icon="💰")

# Estils CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
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
        "total_gastos": "Total Gastos Fijos",
        "disponible": "Disponible para Oci/Ahorro",
        "ratio_label": "% de tus ingresos",
        "veredicte": "Tu Veredicto Financiero",
        "error_bloqueo": "⚠️ Por favor, completa tus datos en la pestaña 'Mi Radiografía' para desbloquear el resto.",
        "btn_save": "¡Mejorar Tarifa!",
        "ahorro_anual": "Ahorro anual estimado",
        "perfecto": "¡Precio perfecto!",
        "perfil_riesgo": "Tu perfil de riesgo",
        "perfils": ["Conservador", "Moderado", "Decidido"],
        "simulador_t": "Simulador de Crecimiento",
        "años": "Años",
        "inv_mensual": "Inversión mensual (€)",
        "resultado_inv": "En {0} años podrías tener: {1} €"
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
        "total_gastos": "Total Fixed Expenses",
        "disponible": "Available for Leisure/Savings",
        "ratio_label": "% of your income",
        "veredicte": "Your Financial Verdict",
        "error_bloqueo": "⚠️ Please, fill in your data in the 'My Radiography' tab to unlock the rest.",
        "btn_save": "Improve Rate!",
        "ahorro_anual": "Estimated annual savings",
        "perfecto": "Perfect price!",
        "perfil_riesgo": "Your risk profile",
        "perfils": ["Conservative", "Moderate", "Aggressive"],
        "simulador_t": "Growth Simulator",
        "años": "Years",
        "inv_mensual": "Monthly Investment (€)",
        "resultado_inv": "In {0} years you could have: {1} €"
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

# Càlculs
total_gastos = lloguer_val + llum_val + gas_val + aigua_val + internet_val + mobil_val + deute_val
ratio = (total_gastos / ingresos_val * 100) if ingresos_val > 0 else 0
is_ready = ingresos_val > 0 and total_gastos > 0

# 4. PESTANYES
tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

# --- TAB 1: RADIOGRAFIA ---
with tab1:
    st.title(t["titol"])
    st.write(t["subtitol"])
    
    if ingresos_val == 0:
        st.info(t["error_bloqueo"])
    
    c1, c2, c3 = st.columns(3)
    c1.metric(t["total_gastos"], f"{total_gastos} €")
    c2.metric(t["ratio_label"], f"{ratio:.1f}%", delta="-50%" if ratio > 50 else "OK", delta_color="inverse" if ratio > 50 else "normal")
    c3.metric(t["disponible"], f"{ingresos_val - total_gastos} €")

    if is_ready:
        col_l, col_r = st.columns(2)
        with col_l:
            labels = [t["lloguer"], t["llum"], t["gas"], t["aigua"], t["internet"], t["mobil"], t["deutes"], t["disponible"]]
            values = [lloguer_val, llum_val, gas_val, aigua_val, internet_val, mobil_val, deute_val, max(0, ingresos_val-total_gastos)]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            st.subheader(t["veredicte"])
            if ratio > 50:
                st.error("🚨" + (" Gastas demasiado en fijos." if idioma == "Español" else " Fixed costs too high."))
            else:
                st.success("✅" + (" ¡Finanzas equilibradas!" if idioma == "Español" else " Balanced finances!"))
            score = max(0, 100 - int(ratio))
            st.write(f"**Score: {score}/100**")
            st.progress(score / 100)

# --- TAB 2: PLAN DE AHORRO (BLOQUEJADA SI NO HI HA DADES) ---
with tab2:
    if not is_ready:
        st.warning(t["error_bloqueo"])
    else:
        st.header(t["tab2"])
        
        # Lògica de comparació
        def row_ahorro(servici, actual, optim):
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1: st.write(f"**{servici}**")
            with col2: st.write(f"{actual}€  vs  **{optim}€**")
            with col3:
                if actual > optim:
                    st.link_button(t["btn_save"], "https://google.com")
                    st.caption(f"{t['ahorro_anual']}: {(actual-optim)*12}€")
                else:
                    st.write(f"✅ {t['perfecto']}")

        row_ahorro(t["internet"], internet_val, 25.0)
        st.divider()
        row_ahorro(t["mobil"], mobil_val, 10.0)
        st.divider()
        row_ahorro(t["llum"], llum_val, llum_val*0.75) # Estimació 25% estalvi
        st.divider()
        st.write(f"**{t['aigua']}**: " + ("El precio del agua es regulado. Revisa goteos y solicita el Bono Social si tus ingresos son bajos." if idioma == "Español" else "Water prices are regulated. Check for leaks and apply for social discounts if eligible."))

# --- TAB 3: INVERSIÓN (BLOQUEJADA) ---
with tab3:
    if not is_ready:
        st.warning(t["error_bloqueo"])
    else:
        st.header(t["simulador_t"])
        perf = st.select_slider(t["perfil_riesgo"], options=t["perfils"])
        anys = st.slider(t["años"], 1, 30, 10)
        inv = st.slider(t["inv_mensual"], 0, 2000, 200)
        
        r = 0.03 if perf == t["perfils"][0] else (0.05 if perf == t["perfils"][1] else 0.08)
        final = 0
        for _ in range(anys * 12): final = (final + inv) * (1 + r/12)
        
        st.line_chart([ (inv*i) for i in range(anys*12) ]) # Gràfic simple de creixement
        st.success(t["resultado_inv"].format(anys, int(final)))

# --- TAB 4: EDUCACIÓN ---
with tab4:
    st.header(t["tab4"])
    st.write("Contenido educativo en desarrollo..." if idioma == "Español" else "Educational content under development...")

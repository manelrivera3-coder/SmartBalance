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
        "total_gastos": "Total Gastos Fijos (50%)",
        "oci_recom": "Presupuesto Ocio (30%)",
        "ahorro_recom": "Objetivo Ahorro (20%)",
        "disponible": "Disponible Total",
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
        "total_gastos": "Total Fixed Expenses (50%)",
        "oci_recom": "Leisure Budget (30%)",
        "ahorro_recom": "Savings Goal (20%)",
        "disponible": "Total Available",
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

# Càlculs base
total_gastos = lloguer_val + llum_val + gas_val + aigua_val + internet_val + mobil_val + deute_val
ratio = (total_gastos / ingresos_val * 100) if ingresos_val > 0 else 0
disponible_total = max(0, ingresos_val - total_gastos)

# Càlculs Regla 50/30/20 (Ideal)
oci_ideal = ingresos_val * 0.30
ahorro_ideal = ingresos_val * 0.20

# Adaptació real segons el que queda
if ratio > 50:
    # Si les despeses fixes superen el 50%, repartim el que queda proporcionalment 60/40 entre oci i estalvi
    oci_real = disponible_total * 0.60
    ahorro_real = disponible_total * 0.40
else:
    oci_real = oci_ideal
    ahorro_real = ahorro_ideal

is_ready = ingresos_val > 0 and total_gastos > 0

# 4. PESTANYES
tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

# --- TAB 1: RADIOGRAFIA ---
with tab1:
    st.title(t["titol"])
    st.write(t["subtitol"])
    
    if ingresos_val == 0:
        st.info(t["error_bloqueo"])
    
    # Primera fila de mètriques
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
            fig.update_layout(title_text="SmartBalance 50/30/20")
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            st.subheader(t["veredicte"])
            if ratio > 50:
                st.error("🚨" + (" Tus gastos fijos superan el 50%. Debes recortar facturas urgentemente." if idioma == "Español" else " Fixed costs exceed 50%. You must cut bills urgently."))
            else:
                st.success("✅" + (" ¡Finanzas bajo control! Estás siguiendo la regla de oro." if idioma == "Español" else " Finances under control! You are following the golden rule."))
            
            score = max(0, 100 - int(ratio))
            st.write(f"**Financial Score: {score}/100**")
            st.progress(score / 100)
            st.info("💡 " + ("El presupuesto de Ocio y Ahorro se ha calculado en base a lo que te queda disponible tras tus gastos fijos." if idioma == "Español" else "Leisure and Savings budgets are calculated based on what remains after your fixed expenses."))

# --- TAB 2: PLAN DE AHORRO ---
with tab2:
    if not is_ready:
        st.warning(t["error_bloqueo"])
    else:
        st.header(t["tab2"])
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
        row_ahorro(t["llum"], llum_val, round(llum_val*0.75, 2))
        st.divider()
        row_ahorro(t["gas"], gas_val, round(gas_val*0.80, 2))

# --- TAB 3: INVERSIÓN ---
with tab3:
    if not is_ready:
        st.warning(t["error_bloqueo"])
    else:
        st.header(t["simulador_t"])
        perf = st.select_slider(t["perfil_riesgo"], options=t["perfils"])
        anys = st.slider(t["años"], 1, 30, 10)
        # Sugerim invertir exactament el que ha sortit com a ahorro_real
        inv = st.slider(t["inv_mensual"], 0, int(ingresos_val), int(ahorro_real))
        
        r = 0.03 if perf == t["perfils"][0] else (0.05 if perf == t["perfils"][1] else 0.08)
        final = 0
        for _ in range(anys * 12): final = (final + inv) * (1 + r/12)
        
        st.success(t["resultado_inv"].format(anys, f"{final:,.0f}"))
        st.caption("Nota: El interés compuesto es la clave para que tus ahorros venzan a la inflación.")

# --- TAB 4: EDUCACIÓN ---
with tab4:
    st.header(t["tab4"])
    st.write("Contenido educativo en desarrollo..." if idioma == "Español" else "Educational content under development...")

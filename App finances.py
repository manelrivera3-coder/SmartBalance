import streamlit as st
import plotly.graph_objects as go

# 1. CONFIGURACIÓ DE LA PÀGINA
st.set_page_config(page_title="SmartBalance", layout="wide", page_icon="💰")

# Estils CSS per optimitzar l'espai vertical (tot més petit)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .company-box { 
        background-color: #ffffff; 
        padding: 8px; 
        border-radius: 5px; 
        border: 1px solid #ddd; 
        text-align: center; 
        font-size: 0.85rem;
    }
    h1 { font-size: 1.6rem !important; margin-bottom: 0.5rem; }
    h2 { font-size: 1.3rem !important; margin-top: 0.5rem; margin-bottom: 0.5rem; }
    h3 { font-size: 1.0rem !important; margin-top: 0.3rem; margin-bottom: 0.3rem; }
    .stButton > button { height: 28px; font-size: 0.8rem; padding: 0px 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. DICCIONARI DE TEXTOS
texts = {
    "Español": {
        "setup": "Configuración",
        "idioma": "Idioma",
        "titol": "SmartBalance 💰",
        "subtitol": "Ordena tus finanzas",
        "tab1": "📊 Radiografía",
        "tab2": "✂️ Plan de Ahorro",
        "tab3": "📈 Inversión",
        "tab4": "🎓 Educación",
        "ingresos_label": "Ingresos netos (€)",
        "gastos_f": "Gastos Fijos",
        "lloguer": "Alquiler / Hipoteca",
        "internet": "Internet (Fibra)",
        "mobil": "Móvil",
        "llum": "Luz",
        "gas": "Gas",
        "aigua": "Agua",
        "deutes": "Deudas",
        "total_gastos": "Total Fijos (50%)",
        "oci_recom": "Ocio (30%)",
        "ahorro_recom": "Ahorro (20%)",
        "disponible": "Disponible Total",
        "ratio_label": "% Ingresos",
        "veredicte": "Veredicto",
        "error_bloqueo": "⚠️ Completa tus datos en 'Mi Radiografía'.",
        "btn_save": "Ver Oferta",
        "ahorro_anual": "Ahorro anual",
        "perfecto": "¡Precio OK!",
        "perfil_riesgo": "Riesgo",
        "perfils": ["Conservador", "Moderado", "Decidido"],
        "simulador_t": "Simulador",
        "años": "Años",
        "inv_mensual": "Inversión (€)",
        "resultado_inv": "Total: {1} €",
        "top_3": "Mejores ofertas:"
    },
    "English": {
        "setup": "Setup",
        "idioma": "Language",
        "titol": "SmartBalance 💰",
        "subtitol": "Organize your finances",
        "tab1": "📊 Radiography",
        "tab2": "✂️ Saving Plan",
        "tab3": "📈 Investment",
        "tab4": "🎓 Education",
        "ingresos_label": "Net Income (€)",
        "gastos_f": "Fixed Expenses",
        "lloguer": "Rent / Mortgage",
        "internet": "Internet (Fiber)",
        "mobil": "Mobile",
        "llum": "Power",
        "gas": "Gas",
        "aigua": "Water",
        "deutes": "Debts",
        "total_gastos": "Total Fixed (50%)",
        "oci_recom": "Leisure (30%)",
        "ahorro_recom": "Savings (20%)",
        "disponible": "Total Available",
        "ratio_label": "% Income",
        "veredicte": "Verdict",
        "error_bloqueo": "⚠️ Fill in 'My Radiography' first.",
        "btn_save": "View Offer",
        "ahorro_anual": "Annual saving",
        "perfecto": "Perfect price!",
        "perfil_riesgo": "Risk profile",
        "perfils": ["Conservative", "Moderate", "Aggressive"],
        "simulador_t": "Simulator",
        "años": "Years",
        "inv_mensual": "Monthly Invest (€)",
        "resultado_inv": "Total: {1} €",
        "top_3": "Top 3 offers:"
    }
}

# 3. SIDEBAR
with st.sidebar:
    idioma = st.selectbox("Language / Idioma", ["Español", "English"])
    t = texts[idioma]
    st.divider()
    st.header(t["gastos_f"])
    ingresos_val = st.number_input(t["ingresos_label"], min_value=0, value=2000, step=100)
    lloguer_val = st.number_input(t["lloguer"], min_value=0, value=800)
    llum_val = st.number_input(t["llum"], min_value=0, value=60)
    gas_val = st.number_input(t["gas"], min_value=0, value=40)
    aigua_val = st.number_input(t["aigua"], min_value=0, value=25)
    internet_val = st.number_input(t["internet"], min_value=0, value=40)
    mobil_val = st.number_input(t["mobil"], min_value=0, value=20)
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
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t["total_gastos"], f"{total_gastos} €")
    c2.metric(t["ratio_label"], f"{ratio:.1f}%")
    c3.metric(t["oci_recom"], f"{int(oci_real)} €")
    c4.metric(t["ahorro_recom"], f"{int(ahorro_real)} €")

    if is_ready:
        col_l, col_r = st.columns(2)
        with col_l:
            labels = [t["lloguer"], "Bills", t["deutes"], t["oci_recom"], t["ahorro_recom"]]
            values = [lloguer_val, (llum_val+gas_val+aigua_val+internet_val+mobil_val), deute_val, oci_real, ahorro_real]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            st.write(f"**Score: {max(0, 100 - int(ratio))}/100**")
            st.progress(max(0, 100 - int(ratio)) / 100)
            if ratio > 50: st.error(t["veredicte"] + ": Recortar")
            else: st.success(t["veredicte"] + ": OK")

# --- TAB 2: PLAN DE AHORRO ---
with tab2:
    if not is_ready:
        st.warning(t["error_bloqueo"])
    else:
        # Base de dades d'ofertes actualitzada amb Gas
        db_ofertes = {
            "internet": [
                {"cia": "Digi", "p": 25.0, "link": "https://digimobil.es"},
                {"cia": "Lowi", "p": 29.9, "link": "https://lowi.es"},
                {"cia": "O2", "p": 35.0, "link": "https://o2online.es"}
            ],
            "mobil": [
                {"cia": "Simyo", "p": 7.0, "link": "https://simyo.es"},
                {"cia": "Pepe", "p": 10.0, "link": "https://pepephone.com"},
                {"cia": "Fine", "p": 12.0, "link": "https://finetwork.com"}
            ],
            "llum": [
                {"cia": "Octo", "p": "Bajo", "link": "https://octopusenergy.es"},
                {"cia": "Natur", "p": "Fijo", "link": "https://naturgy.es"},
                {"cia": "Ende", "p": "Prom", "link": "https://endesa.com"}
            ],
            "gas": [
                {"cia": "Natur", "p": "TUR", "link": "https://naturgy.es"},
                {"cia": "Ende", "p": "One", "link": "https://endesa.com"},
                {"cia": "Total", "p": "Facil", "link": "https://totalenergies.es"}
            ]
        }

        def mostrar_seccio_compacta(icona, titol, valor_actual, clau_db):
            # Capçalera compacta
            st.markdown(f"### {icona} {titol}")
            
            best_price = db_ofertes[clau_db][0]["p"]
            if isinstance(best_price, float) and valor_actual > best_price:
                st.caption(f"💡 {t['ahorro_anual']}: {(valor_actual - best_price)*12:.0f}€")
            
            cols = st.columns(3)
            for i, oferta in enumerate(db_ofertes[clau_db]):
                with cols[i]:
                    st.markdown(f"<div class='company-box'><b>{oferta['cia']}</b><br>{oferta['p']}€</div>", unsafe_allow_html=True)
                    st.link_button(t["btn_save"], oferta["link"], use_container_width=True)

        # Crides a la funció amb icones professionals
        mostrar_seccio_compacta("🌐", t["internet"], internet_val, "internet")
        mostrar_seccio_compacta("📲", t["mobil"], mobil_val, "mobil")
        mostrar_seccio_compacta("💡", t["llum"], llum_val, "llum")
        mostrar_seccio_compacta("🔥", t["gas"], gas_val, "gas")

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
    st.write("Academy 🎓")
    st.info("Regla 50/30/20")

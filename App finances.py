import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. CONFIGURACIÓ DE LA PÀGINA
st.set_page_config(page_title="SmartBalance - Personal Finance", layout="wide", page_icon="💰")

# Estils CSS per millorar l'aspecte
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA MULTIDIOMA
with st.sidebar:
    st.title("⚙️ Setup")
    idioma = st.selectbox("Language / Idioma", ["Español", "English"])
    st.divider()
    st.caption("SmartBalance v1.0 - 2026")

texts = {
    "Español": {
        "titol": "SmartBalance 💰",
        "subtitol": "Ordena tus finanzas y construye tu futuro",
        "tab1": "📊 Radiografía Actual",
        "tab2": "✂️ Plan de Ahorro",
        "tab3": "📈 Inversión y Futuro",
        "tab4": "🎓 Educación",
        "ingresos": "Ingresos mensuales (€)",
        "gastos_f": "Gastos Fijos",
        "lloguer": "Alquiler/Hipoteca",
        "subministraments": "Suministros (Luz, Gas, Internet)",
        "deutes": "Deudas/Préstamos",
        "resultat": "Tu veredicto",
        "disponible": "Disponible",
        "btn_save": "¡Cambiar y ahorrar!",
        "invest_perfil": "Tu perfil de riesgo",
        "perfils": ["Conservador", "Moderado", "Decidido"],
        "interes_compost": "Simulador de Interés Compuesto"
    },
    "English": {
        "titol": "SmartBalance 💰",
        "subtitol": "Organize your finances and build your future",
        "tab1": "📊 Current Health",
        "tab2": "✂️ Saving Plan",
        "tab3": "📈 Invest & Future",
        "tab4": "🎓 Education",
        "ingresos": "Monthly Income (€)",
        "gastos_f": "Fixed Expenses",
        "lloguer": "Rent/Mortgage",
        "subministraments": "Utilities (Power, Gas, Internet)",
        "deutes": "Debts/Loans",
        "resultat": "Your Verdict",
        "disponible": "Available",
        "btn_save": "Switch & Save!",
        "invest_perfil": "Your risk profile",
        "perfils": ["Conservative", "Moderate", "Aggressive"],
        "interes_compost": "Compound Interest Simulator"
    }
}

t = texts[idioma]

# 3. INPUTS GLOBALS (Sidebar)
with st.sidebar:
    st.header(t["ingresos"])
    ingresos_val = st.number_input("Amount", min_value=0, value=2000, step=100, label_visibility="collapsed")
    
    st.header(t["gastos_f"])
    lloguer_val = st.number_input(t["lloguer"], min_value=0, value=800)
    internet_val = st.number_input("Internet + Mobile", min_value=0, value=60)
    llum_val = st.number_input("Power / Luz", min_value=0, value=80)
    gas_val = st.number_input("Gas", min_value=0, value=40)
    deute_val = st.number_input(t["deutes"], min_value=0, value=0)

# Càlculs base
total_gastos = lloguer_val + internet_val + llum_val + gas_val + deute_val
ratio = (total_gastos / ingresos_val) * 100 if ingresos_val > 0 else 0
disponible_val = ingresos_val - total_gastos

# 4. ESTRUCTURA DE PESTANYES
tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

# --- PESTANYA 1: RADIOGRAFIA ---
with tab1:
    st.title(t["titol"])
    st.write(t["subtitol"])
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Expenses", f"{total_gastos} €")
    c2.metric("% Income", f"{ratio:.1f}%", delta="-50%" if ratio > 50 else "OK", delta_color="inverse" if ratio > 50 else "normal")
    c3.metric(t["disponible"], f"{disponible_val} €")

    col_l, col_r = st.columns(2)
    with col_l:
        fig = go.Figure(data=[go.Pie(labels=['Rent', 'Bills', 'Debts', 'Free'], 
                                     values=[lloguer_val, internet_val+llum_val+gas_val, deute_val, disponible_val], 
                                     hole=.4)])
        st.plotly_chart(fig, use_container_width=True)
    with col_r:
        st.subheader(t["resultat"])
        if ratio > 50:
            st.error("🚨 Warning: Your fixed costs are too high. Go to 'Saving Plan'!")
        else:
            st.success("✅ Healthy! You have margin to invest.")
        
        score = max(0, 100 - int(ratio))
        st.write(f"**Financial Score: {score}/100**")
        st.progress(score / 100)

# --- PESTANYA 2: PLAN DE AHORRO (AFILIATS) ---
with tab2:
    st.header("✂️ Smart Savings")
    st.write("Compare your current bills with the best market offers (2026).")
    
    # Simulem millors preus del mercat
    m_internet = 35.0
    m_llum = 0.12 # €/kwh
    
    # Internet Row
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1: st.write("**Service: Internet + Mobile**")
    with col2: st.write(f"Current: {internet_val}€ | **Target: {m_internet}€**")
    with col3: 
        if internet_val > m_internet:
            st.link_button(t["btn_save"], "https://google.com") # Aquí aniria el teu link d'afiliat
            st.caption(f"Save {(internet_val-m_internet)*12}€/year")

    st.divider()
    
    # Energy Row
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1: st.write("**Service: Electricity**")
    with col2: st.write(f"Current: {llum_val}€ | **Target: -25% average**")
    with col3: st.link_button(t["btn_save"], "https://google.com")

# --- PESTANYA 3: INVERSIÓ ---
with tab3:
    st.header(t["interes_compost"])
    
    perfil = st.select_slider(t["invest_perfil"], options=t["perfils"])
    
    # Simulació interès compost
    years = st.slider("Years", 1, 30, 10)
    monthly_inv = st.slider("Monthly Investment (€)", 0, 1000, 200)
    
    rate = 0.03 if perfil == t["perfils"][0] else (0.05 if perfil == t["perfils"][1] else 0.08)
    
    data = []
    balance = 0
    for i in range(years * 12):
        balance = (balance + monthly_inv) * (1 + rate/12)
        if i % 12 == 0:
            data.append(balance)
            
    st.line_chart(data)
    st.write(f"### In {years} years, you could have: **{int(balance)} €**")
    st.info("Products: High Yield Accounts (Safe), Treasury Bonds (Moderate), Index Funds (Aggressive).")

# --- PESTANYA 4: EDUCACIÓ ---
with tab4:
    st.header("🎓 Smart Academy")
    with st.expander("¿Qué es la Regla 50/30/20?"):
        st.write("50% Necesidades, 30% Deseos, 20% Ahorro/Inversión.")
    with st.expander("What is Compound Interest?"):
        st.write("It is the interest calculated on the initial principal, which also includes all of the accumulated interest of previous periods.")
    with st.expander("¿Qué es un Fondo Monetario?"):
        st.write("Una inversión de muy bajo riesgo ideal para tu colchón de emergencia.")

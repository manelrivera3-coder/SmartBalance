import streamlit as st
import plotly.graph_objects as go

# Configuració de la pàgina
st.set_page_config(page_title="Finances Sense Por", layout="wide", page_icon="💰")

# Estils personalitzats per fer-la més atractiva
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# Títol i Benvinguda
st.title("💰 Finances Sense Por")
st.subheader("La teva radiografia financera en 2 minuts")
st.write("Introdueix les teves dades anònimament i mira on van els teus diners.")

# --- BARRA LATERAL (INPUTS) ---
with st.sidebar:
    st.header("Les teves dades")
    ingressos = st.number_input("Ingressos nets mensuals (€)", min_value=0, value=2000, step=100)
    
    st.divider()
    st.subheader("Despeses Fixes")
    lloguer = st.number_input("Lloguer o Hipoteca (€)", min_value=0, value=800)
    llum = st.number_input("Llum mensual (€)", min_value=0, value=80)
    gas = st.number_input("Gas mensual (€)", min_value=0, value=40)
    internet = st.number_input("Internet i Mòbil (€)", min_value=0, value=60)
    aigua = st.number_input("Aigua (€)", min_value=0, value=30)
    deutes = st.number_input("Crèdits/Préstecs (€)", min_value=0, value=0)

# --- CÀLCULS LÒGICS ---
total_fixes = lloguer + llum + gas + internet + aigua + deutes
percentatge_fixes = (total_fixes / ingressos) * 100 if ingressos > 0 else 0

# --- PANELL PRINCIPAL ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Despeses Fixes", value=f"{total_fixes} €")

with col2:
    # Color segons la salut financera
    color = "normal" if percentatge_fixes <= 50 else "inverse"
    st.metric(label="% sobre els teus ingressos", value=f"{percentatge_fixes:.1f} %", delta="-50%" if percentatge_fixes > 50 else "Ideal", delta_color=color)

with col3:
    disponible = ingressos - total_fixes
    st.metric(label="Disponible per oci i estalvi", value=f"{disponible} €")

st.divider()

# --- GRÀFIC INTERACTIV (PLOTLY) ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.write("### On van els teus diners?")
    # Gràfic de formatge (Donut chart)
    labels = ['Lloguer/Hipo', 'Subministraments', 'Deutes', 'Disponible']
    values = [lloguer, (llum + gas + internet + aigua), deutes, disponible]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker_colors=['#FF4B4B', '#1C83E1', '#FACA2B', '#28A745'])])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.write("### El teu veredicte")
    
    if percentatge_fixes > 50:
        st.error(f"**Atenció:** Estàs gastant un {percentatge_fixes:.1f}% en necessitats fixes. La regla 50/30/20 diu que no hauries de passar del 50%.")
        st.write("Tens molt marge de millora en els teus contractes. Anem a la següent pestanya per retallar!")
    else:
        st.success("**Bona feina!** Les teves despeses fixes estan sota control. Ets un candidat ideal per començar a invertir el que et sobra.")

    # Puntuació de salut financera (Gamificació)
    puntuacio = max(0, 100 - int(percentatge_fixes))
    st.write(f"#### La teva puntuació actual: **{puntuacio}/100**")
    st.progress(puntuacio / 100)

# --- BOTÓ PER SEGUIR ---
st.button("Vull veure on puc estalviar ara mateix ➡️")
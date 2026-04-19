import streamlit as st
import plotly.graph_objects as go

# 1. CONFIGURACIÓ DE LA PÀGINA
st.set_page_config(page_title="SmartBalance", layout="wide", page_icon="💰")

# Estils CSS
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
        min-height: 160px;
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
    </style>
    """, unsafe_allow_html=True)

# 2. DICCIONARI DE TEXTOS
texts = {
    "Español": {
        "titol": "SmartBalance 💰",
        "tab1": "📊 Mi Radiografía",
        "tab2": "✂️ Plan de Ahorro",
        "ingresos_label": "Ingresos mensuales netos (€)",
        "gastos_f": "Gastos Fijos Mensuales",
        "seguro_coche": "Seguro Coche (Mensual)",
        "ratio_label": "% Gastos Fijos",
        "veredicte_t": "Tu Diagnóstico 50/30/20",
        "btn_save": "Contratar Oferta",
        "ahorro_anual": "Ahorro anual: ",
        "preu_kwh_actual": "¿A cuánto pagas el kWh? (€)",
        "filtro_fibra": "Velocidad Fibra",
        "filtro_mobil": "Datos Móvil",
        "veredicto_ok": "✅ ¡Lo estás haciendo genial! Tus gastos fijos están bajo control.",
        "veredicto_ko": "⚠️ Superas el 50% en gastos fijos. Tienes que optimizar facturas.",
        "f_marca": "Marca del coche",
        "f_combustible": "Combustible",
        "f_uso": "Uso del vehículo",
        "f_edad": "Edad conductor",
        "f_carnet": "Años de carnet"
    },
    "English": {
        "titol": "SmartBalance 💰",
        "tab1": "📊 My Radiography",
        "tab2": "✂️ Saving Plan",
        "ingresos_label": "Net Income (€)",
        "gastos_f": "Fixed Expenses",
        "seguro_coche": "Car Insurance (Monthly)",
        "ratio_label": "% Fixed Expenses",
        "veredicte_t": "50/30/20 Diagnosis",
        "btn_save": "Get Offer",
        "ahorro_anual": "Annual savings: ",
        "preu_kwh_actual": "Price per kWh (€)",
        "filtro_fibra": "Fiber Speed",
        "filtro_mobil": "Mobile Data",
        "veredicto_ok": "✅ Great job! Your fixed expenses are under control.",
        "veredicto_ko": "⚠️ Fixed expenses exceed 50%. You need to optimize bills.",
        "f_marca": "Car Brand",
        "f_combustible": "Fuel type",
        "f_uso": "Vehicle use",
        "f_edad": "Driver age",
        "f_carnet": "License years"
    }
}

# 3. SIDEBAR
with st.sidebar:
    idioma = st.selectbox("Language / Idioma", ["Español", "English"])
    t = texts[idioma]
    st.header(t["gastos_f"])
    ing_val = st.number_input(t["ingresos_label"], min_value=1, value=2000)
    lloguer_val = st.number_input("Alquiler/Hipoteca", value=800)
    llum_val = st.number_input("Luz", value=60)
    gas_val = st.number_input("Gas", value=30)
    aigua_val = st.number_input("Agua", value=20)
    int_val = st.number_input("Internet", value=35)
    mob_val = st.number_input("Móvil", value=15)
    seg_val = st.number_input(t["seguro_coche"], value=40)
    deute_val = st.number_input("Préstamos/Deudas", value=0)

# Càlculs Radiografia
total_fijos = lloguer_val + llum_val + gas_val + aigua_val + int_val + mob_val + seg_val + deute_val
ratio_fijos = (total_fijos / ing_val) * 100
oci_ideal = ing_val * 0.3
ahorro_ideal = ing_val * 0.2

# 4. PESTANYES
tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], "📈 Inversión", "🎓 Educación"])

# --- TAB 1: RADIOGRAFIA I VEREDICTE ---
with tab1:
    st.title(t["titol"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Gastos Fijos", f"{total_fijos} €")
    c2.metric(t["ratio_label"], f"{ratio_fijos:.1f}%", delta="Max 50%")
    c3.metric("Ocio Sugerido", f"{int(oci_ideal)} €")
    c4.metric("Ahorro Sugerido", f"{int(ahorro_ideal)} €")

    st.divider()
    col_l, col_r = st.columns([1, 1])
    with col_l:
        labels = ["Fijos Actuales", "Ocio (30%)", "Ahorro (20%)"]
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
            st.write(f"⚠️ Estás gastando **{int(exces)}€ de más** en facturas fijas cada mes.")
        
        st.info(f"Para cumplir la regla 50/30/20, tus gastos fijos no deberían superar los **{int(ing_val * 0.5)}€**.")

# --- TAB 2: PLAN DE AHORRO ---
with tab2:
    st.header(t["tab2"])
    
    # Funció actualitzada que rep la URL del referit
    def draw_offer(cia, p_nou, p_act, url_referit, unitat="€", is_kwh=False):
        est = (p_act - p_nou) * 3000 if is_kwh else (p_act - p_nou) * 12
        st.markdown(f"""<div class='company-box'><b>{cia}</b><br><span class='price-text'>{p_nou}{unitat}</span><br>
                    <span class='save-label'>{t['ahorro_anual']}{max(0, round(est,2))}€</span></div>""", unsafe_allow_html=True)
        st.link_button(t["btn_save"], url_referit, use_container_width=True)

    # 1. ASSEGURANÇA COTXE
    with st.expander("🚗 Buscador de Seguros (Estilo Rastreator)", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            marca = st.selectbox(t["f_marca"], ["Seat", "Toyota", "BMW", "Audi", "Otros"])
            edat = st.number_input(t["f_edad"], 18, 90, 30)
        with c2:
            comb = st.selectbox(t["f_combustible"], ["Gasolina", "Diésel", "Híbrido"])
            carnet = st.number_input(t["f_carnet"], 0, 70, 10)
        with c3:
            tipo_seg = st.selectbox("Cobertura", ["Terceros", "Todo Riesgo"])

        preu_base = 18 if tipo_seg == "Terceros" else 45
        if edat < 25: preu_base += 15
        
        ca, cb, cc = st.columns(3)
        with ca: draw_offer("Qualitas", preu_base, seg_val, "https://google.com") # Canviar per el teu link
        with cb: draw_offer("Axa", round(preu_base*1.1, 2), seg_val, "https://google.com")
        with cc: draw_offer("Mapfre", round(preu_base*1.3, 2), seg_val, "https://google.com")

    # 2. INTERNET I LLUM
    col_l, col_r = st.columns(2)
    with col_l:
        with st.expander("🌐 Internet y Fibra"):
            f_f = st.select_slider(t["filtro_fibra"], options=["300Mb", "600Mb", "1Gb"])
            p_fib = 20 if f_f=="300Mb" else (25 if f_f=="600Mb" else 30)
            c1, c2, c3 = st.columns(3)
            with c1: draw_offer("Digi", p_fib, int_val, "https://google.com")
            with c2: draw_offer("Lowi", p_fib+4, int_val, "https://google.com")
            with c3: draw_offer("O2", p_fib+7, int_val, "https://google.com")
    
    with col_r:
        with st.expander("💡 Luz"):
            kwh = st.number_input(t["preu_kwh_actual"], 0.0, 0.5, 0.18)
            c1, c2, c3 = st.columns(3)
            with c1: draw_offer("Octopus", 0.11, kwh, "https://google.com", "€/kWh", True)
            with c2: draw_offer("Naturgy", 0.13, kwh, "https://google.com", "€/kWh", True)
            with c3: draw_offer("Endesa", 0.14, kwh, "https://google.com", "€/kWh", True)

    # 3. MOBIL I GAS
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

# PESTANYES 3 I 4 (POTS OMPLIR-LES DESPRÉS)
with tab3: st.info("Próximamente: Simulador de Inversión")
with tab4: st.info("Próximamente: Artículos de Educación Financiera")

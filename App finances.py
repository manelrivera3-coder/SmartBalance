import streamlit as st
import plotly.graph_objects as go

# 1. CONFIGURACIÓ DE LA PÀGINA
st.set_page_config(page_title="SmartBalance", layout="wide", page_icon="💰")

# Estils CSS Personalitzats per a tota l'app
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .company-box { 
        background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; 
        text-align: center; margin-bottom: 5px; min-height: 160px;
    }
    .price-text { font-size: 1.3rem; font-weight: bold; color: #1E1E1E; }
    .save-label { color: #28a745; font-weight: bold; font-size: 0.9rem; margin-top: 5px; }
    .total-save-banner { 
        background-color: #155724; color: white; padding: 20px; border-radius: 12px; 
        text-align: center; margin-bottom: 25px; font-size: 1.5rem; font-weight: bold;
    }
    .debt-alert { padding: 12px; border-radius: 8px; margin-bottom: 5px; font-size: 0.9rem; font-weight: bold; }
    .bad-debt { background-color: #f8d7da; color: #721c24; border-left: 5px solid #dc3545; }
    .good-debt { background-color: #d4edda; color: #155724; border-left: 5px solid #28a745; }
    .neutral-debt { background-color: #fff3cd; color: #856404; border-left: 5px solid #ffc107; }
    </style>
    """, unsafe_allow_html=True)

# 2. DICCIONARI DE TEXTOS
texts = {
    "Español": {
        "titol": "SmartBalance 💰",
        "tab1": "📊 Mi Radiografía",
        "tab2": "✂️ Plan de Ahorro",
        "tab3": "📉 Centro de Deuda",
        "tab4": "🎓 Educación",
        "ingresos_label": "Ingresos mensuales netos (€)",
        "gastos_f": "Gastos Fijos Mensuales",
        "seguro_coche": "Seguro Coche (Mensual)",
        "ratio_label": "% Gastos Fijos",
        "veredicte_t": "Tu Diagnóstico 50/30/20",
        "btn_save": "Contratar Oferta",
        "ahorro_anual": "Ahorro anual: ",
        "total_ahorro_msg": "🚀 Si optimizas hoy, puedes ahorrar al año: ",
        "preu_kwh_actual": "¿A cuánto pagas el kWh? (€)",
        "filtro_fibra": "Velocidad Fibra",
        "filtro_mobil": "Datos Móvil",
        "f_marca": "Marca del coche",
        "f_combustible": "Combustible",
        "f_uso": "Uso del vehículo",
        "f_edad": "Edad conductor",
        "f_carnet": "Años de carnet",
        "analisis_prof": "Asesoría Profesional de Deuda",
        "veredicto_ok": "✅ ¡Lo estás haciendo genial! Tus gastos fijos están bajo control.",
        "veredicto_ko": "⚠️ Superas el 50% en gastos fijos. Tienes que optimizar facturas."
    }
}

# 3. SIDEBAR - ENTRADA DE DATOS PRINCIPALES
with st.sidebar:
    idioma = st.selectbox("Idioma", ["Español"])
    t = texts[idioma]
    st.header(t["gastos_f"])
    ing_val = st.number_input(t["ingresos_label"], min_value=1, value=2000)
    lloguer_val = st.number_input("Alquiler / Hipoteca (Cuota)", value=800)
    
    # Afegim el camp de Crèdits directament aquí
    credits_val = st.number_input("Otros Créditos / Préstamos", value=0)
    
    alim_val = st.number_input("Alimentación (Súper)", value=350)
    gaso_val = st.number_input("Gasolina / Transporte", value=120)
    llum_val = st.number_input("Luz (Electricidad)", value=60)
    gas_val = st.number_input("Gas", value=30)
    aigua_val = st.number_input("Agua", value=20)
    int_val = st.number_input("Internet (Fibra)", value=35)
    mob_val = st.number_input("Móvil", value=15)
    seg_val = st.number_input(t["seguro_coche"], value=40)

# Càlcul global només basat en el Sidebar
total_fijos = lloguer_val + credits_val + alim_val + gaso_val + llum_val + gas_val + aigua_val + int_val + mob_val + seg_val
ratio_fijos = (total_fijos / ing_val) * 100

# --- TAB 1: RADIOGRAFÍA (ACTUALITZADA AMB CRÈDITS) ---
with tab1:
    st.title(t["titol"])
    
    # Calculem el total incloent la suma de les cuotes de deutes
    # total_fijos ja inclou total_cuotas_deuda segons el càlcul global que hem fet abans
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Gastos Fijos", f"{total_fijos} €")
    c2.metric("Cuotas Préstamos", f"{total_cuotas_deuda} €", help="Suma de las deudas añadidas en la pestaña 3")
    c3.metric(t["ratio_label"], f"{ratio_fijos:.1f}%", delta="Máx 50%", delta_color="inverse")
    c4.metric("Sobrante Real", f"{int(ing_val - total_fijos)} €")

    st.divider()
    
    col_l, col_r = st.columns([1, 1])
    with col_l:
        # Gràfic de pastís actualitzat amb 4 categories per a més detall
        labels = ["Vivienda/Facturas", "Alimentación/Transp.", "Préstamos/Créditos", "Disponible (Ocio/Ahorro)"]
        
        # Desglossem les despeses per al gràfic
        viv_fact = lloguer_val + llum_val + gas_val + aigua_val + int_val + mob_val + seg_val
        alim_trans = alim_val + gaso_val
        disponible = max(0, ing_val - total_fijos)
        
        values = [viv_fact, alim_trans, total_cuotas_deuda, disponible]
        
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
            st.write(f"⚠️ Estás gastando **{int(exces)}€ de más** cada mes sobre el límite del 50%.")
        
        st.info(f"Para cumplir la regla 50/30/20, tus gastos fijos (incluyendo préstamos) no deberían superar los **{int(ing_val * 0.5)}€**.")
        
        if total_cuotas_deuda > (ing_val * 0.35):
            st.warning("🚨 **Aviso:** Tus préstamos superan el 35% de tus ingresos, lo cual es un riesgo financiero alto.")

# --- TAB 2: PLAN DE AHORRO ---
with tab2:
    if not is_ready:
        st.warning("Introduce tus ingresos en el menú lateral.")
    else:
        # Cálculo de ahorro potencial para el Banner
        est_int = max(0, (int_val - 20) * 12)
        est_llu = max(0, (0.18 - 0.11) * 3000)
        est_mob = max(0, (mob_val - 7) * 12)
        est_seg = max(0, (seg_val - 18) * 12)
        est_total = est_int + est_llu + est_mob + est_seg

        st.markdown(f"<div class='total-save-banner'>{t['total_ahorro_msg']} {round(est_total, 2)} € 💰</div>", unsafe_allow_html=True)

        def draw_offer(cia, p_nou, p_act, url, unitat="€", is_kwh=False):
            est = (p_act - p_nou) * 3000 if is_kwh else (p_act - p_nou) * 12
            st.markdown(f"<div class='company-box'><b>{cia}</b><br><span class='price-text'>{p_nou}{unitat}</span><br><span class='save-label'>{t['ahorro_anual']}{max(0, round(est,2))}€</span></div>", unsafe_allow_html=True)
            st.link_button(t["btn_save"], url, use_container_width=True)

        # SECCIÓN SEGURO COCHE
        with st.expander("🚗 Buscador de Seguros de Coche (Estilo Rastreator)", expanded=True):
            c1, c2, c3 = st.columns(3)
            with c1: marca = st.selectbox(t["f_marca"], ["Seat", "Toyota", "Audi", "BMW", "Otros"]); edat = st.number_input(t["f_edad"], 18, 90, 30)
            with c2: comb = st.selectbox(t["f_combustible"], ["Gasolina", "Diésel", "Híbrido"]); carnet = st.number_input(t["f_carnet"], 0, 70, 10)
            with c3: tipo_seg = st.selectbox("Cobertura", ["Terceros", "Todo Riesgo"])
            
            p_base = 18 if tipo_seg == "Terceros" else 45
            if edat < 25: p_base += 15
            
            ca, cb, cc = st.columns(3)
            with ca: draw_offer("Qualitas", p_base, seg_val, "https://google.com")
            with cb: draw_offer("Axa", round(p_base*1.1, 2), seg_val, "https://google.com")
            with cc: draw_offer("Mapfre", round(p_base*1.3, 2), seg_val, "https://google.com")

        # SECCIÓN INTERNET Y LUZ
        col_l, col_r = st.columns(2)
        with col_l:
            with st.expander("🌐 Internet y Fibra"):
                f_f = st.select_slider(t["filtro_fibra"], options=["300Mb", "600Mb", "1Gb"])
                p_f = 20 if f_f=="300Mb" else (25 if f_f=="600Mb" else 30)
                c1, c2, c3 = st.columns(3)
                with c1: draw_offer("Digi", p_f, int_val, "https://google.com")
                with c2: draw_offer("Lowi", p_f+4, int_val, "https://google.com")
                with c3: draw_offer("O2", p_f+7, int_val, "https://google.com")
        with col_r:
            with st.expander("💡 Luz"):
                kwh_in = st.number_input(t["preu_kwh_actual"], 0.0, 0.5, 0.18)
                c1, c2, c3 = st.columns(3)
                with c1: draw_offer("Octopus", 0.11, kwh_in, "https://google.com", "€/kWh", True)
                with c2: draw_offer("Naturgy", 0.13, kwh_in, "https://google.com", "€/kWh", True)
                with c3: draw_offer("Endesa", 0.14, kwh_in, "https://google.com", "€/kWh", True)

        # SECCIÓN MÓVIL Y GAS
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

# --- TAB 3: CENTRO DE DEUDA ---
with tab3:
    st.header("🏛️ " + t["analisis_prof"])
    st.write("Analizaremos tus préstamos basándonos en los tipos de interés actuales del mercado (BCE/Banco de España).")

    with st.expander("➕ Añadir / Editar Deudas (Máximo 5)", expanded=True):
        cols = st.columns([2, 2, 1, 1])
        d_nom = cols[0].text_input("Nombre del préstamo", placeholder="Ej: Coche")
        d_tipus = cols[1].selectbox("Tipo", ["Hipoteca", "Préstamo Personal", "Revolving / Tarjeta", "Coche"])
        d_cuota = cols[2].number_input("Cuota mensual (€)", min_value=0.0)
        d_interes = cols[3].number_input("TIN (%)", min_value=0.0, step=0.1)
        
        if st.button("Añadir Deuda"):
            if len(st.session_state.deutes_lista) < 5:
                st.session_state.deutes_lista.append({"nom": d_nom, "tipus": d_tipus, "cuota": d_cuota, "interes": d_interes})
                st.rerun()
            else:
                st.error("Límite de 5 préstamos alcanzado.")

    if st.session_state.deutes_lista:
        st.subheader("Tu Análisis Personalizado")
        for i, d in enumerate(st.session_state.deutes_lista):
            # Lógica de asesor profesional
            status_class = "neutral-debt"
            consejo = ""
            btn_txt = ""
            link = "https://google.com" # Espacio para tus referidos

            if d['tipus'] == "Hipoteca":
                if d['interes'] > 3.8:
                    status_class = "bad-debt"; consejo = "❌ Muy caro. El mercado está al 2.8%."; btn_txt = "Mejorar Hipoteca"
                else:
                    status_class = "good-debt"; consejo = "✅ Condiciones competitivas."
            
            elif d['tipus'] == "Revolving / Tarjeta":
                if d['interes'] > 18.0:
                    status_class = "bad-debt"; consejo = "🚨 PELIGRO: Posible usura. ¡Reclama o unifica!"; btn_txt = "Unificar Deuda"
                else:
                    status_class = "neutral-debt"; consejo = "⚠️ Interés alto. Evita usar tarjetas."

            elif d['tipus'] == "Préstamo Personal" or d['tipus'] == "Coche":
                if d['interes'] > 9.0:
                    status_class = "bad-debt"; consejo = "❌ Interés alto. Podrías bajarlo al 7%."; btn_txt = "Refinanciar"
                else:
                    status_class = "good-debt"; consejo = "✅ Interés dentro de mercado."

            # Renderizado de fila de deuda
            c_d1, c_d2, c_d3 = st.columns([2, 3, 2])
            c_d1.write(f"**{d['nom']}** ({d['cuota']}€/mes)")
            c_d2.markdown(f"<div class='debt-alert {status_class}'>{d['interes']}%: {consejo}</div>", unsafe_allow_html=True)
            if btn_txt:
                c_d3.link_button(f"🔗 {btn_txt}", link)
            
            if st.button(f"Eliminar {i}", key=f"del_{i}"):
                st.session_state.deutes_lista.pop(i)
                st.rerun()

        st.divider()
        ratio_endeudamiento = (total_cuotas_deuda / ing_val) * 100
        st.subheader("Ratio de Endeudamiento Total")
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Cuotas de Deuda", f"{total_cuotas_deuda} €")
        col_res2.metric("Ratio DTI", f"{ratio_endeudamiento:.1f}%", delta="-35% Máx")

        if ratio_endeudamiento > 35:
            st.error("🛑 **Alerta:** Tu deuda supera el 35% de tus ingresos. Recomendamos una **Reunificación de Deuda** para bajar la cuota total.")
            st.link_button("🆘 Solicitar Reunificación", "https://google.com")

# --- TAB 4: INVERSIÓN (NOVA) ---
with tab4:
    st.header("📈 Tu Estrategia de Inversión")
    st.write("Una vez optimizado el ahorro y analizada la deuda, es hora de poner a trabajar tu dinero.")
    
    with st.expander("📋 Test de Perfil de Riesgo (10 Preguntas)", expanded=True):
        sc = 0
        q1 = st.selectbox("1. ¿Cuál es tu edad?", ["18-35", "36-50", "51-65", "65+"])
        q2 = st.radio("2. ¿Qué harías si tu inversión cae un 20% en un mes?", ["Vender todo", "Mantener", "Comprar más"])
        q3 = st.selectbox("3. Plazo de la inversión", ["< 2 años", "2-5 años", "5-10 años", "> 10 años"])
        q4 = st.radio("4. ¿Tienes fondo de emergencia?", ["No", "Sí, 3 meses", "Sí, +6 meses"])
        q5 = st.radio("5. ¿Conoces el interés compuesto?", ["No", "Un poco", "Perfectamente"])
        q6 = st.radio("6. Estabilidad de tus ingresos", ["Baja", "Media", "Alta"])
        q7 = st.selectbox("7. Objetivo principal", ["No perder dinero", "Batir inflación", "Crecimiento máximo"])
        q8 = st.radio("8. ¿Te asusta la volatilidad?", ["Mucho", "Normal", "Nada"])
        q9 = st.radio("9. ¿Has invertido antes?", ["Nunca", "Algo", "Soy experto"])
        q10 = st.radio("10. ¿Invertirías en algo que no entiendes?", ["No", "Depende", "Si da rentabilidad"])

        # Lògica de perfil
        if q2 == "Comprar más": sc += 3
        if q7 == "Crecimiento máximo": sc += 3
        if q3 == "> 10 años": sc += 2
        
        perfil = "Conservador" if sc < 3 else ("Moderado" if sc < 6 else "Arriesgado")
        st.subheader(f"Perfil recomendado: **{perfil}**")

    st.divider()
    
    def draw_inv(nom, risc, rent, desc, rec=False):
        css = "border: 2px solid #28a745; background-color: #f0fff4;" if rec else "border: 1px solid #e0e0e0;"
        st.markdown(f"""<div style='padding:15px; border-radius:10px; {css} margin-bottom:10px;'>
            <h4>{nom} {'⭐' if rec else ''}</h4>
            <b>Riesgo:</b> {risc} | <b>Rentabilidad:</b> {rent}<br><small>{desc}</small>
        </div>""", unsafe_allow_html=True)
        st.link_button(f"Ver opciones de {nom}", "https://google.com")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("### 🟢 Bajo Riesgo")
        draw_inv("Depósitos / Cuentas", "Bajo", "2-4%", "Dinero seguro y disponible.", rec=(perfil=="Conservador"))
        draw_inv("Renta Fija", "Bajo", "3-4%", "Bonos del estado y deuda corporativa.")
    with c2:
        st.write("### 🟡 Moderado")
        draw_inv("Fondos Indexados", "Medio", "7-9%", "La mejor opción a largo plazo.", rec=(perfil=="Moderado"))
        draw_inv("Robo-advisors", "Medio", "6-8%", "Gestión pasiva diversificada.")
    with c3:
        st.write("### 🔴 Arriesgado")
        draw_inv("Acciones / ETFs", "Alto", "Variable", "Inversión directa en bolsa.", rec=(perfil=="Arriesgado"))
        draw_inv("Cripto / Otros", "Muy Alto", "Variable", "Solo para capital especulativo.")

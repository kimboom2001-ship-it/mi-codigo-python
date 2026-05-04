import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cimentaciones", layout="wide")

st.markdown("""
<style>
.main .block-container {
    max-width: 1000px;   /* 🔥 ancho fijo */
    margin: auto;        /* 🔥 centrado */
}
</style>
""", unsafe_allow_html=True)

st.title("🧱 Análisis de Capacidad Portanteee")


with st.sidebar:
    st.header("⚙️ P A R Á M E T R O S")

    # =========================
    # 🔹 EDIFICACIÓN
    # =========================
    st.subheader("🏢 EDIFICACIÓN")

    sotano = st.radio("¿Edificación con sótano?", ["NO", "SI"], horizontal=True)

    h = 0.0
    if sotano == "SI":
        h = st.number_input("h (m)", value=3.0)

    # ========================= 
    # 🔹 INCLINACIÓN 
    # =========================
    beta = st.selectbox("β (°)", [0, 1])

    # =========================
    # 🔹 GEOMETRÍA
    # =========================
    st.subheader("📐GEOMETRÍA")

    # 🔹 B
    col1, col2 = st.columns(2)
    
    with col1:
        B_ini = st.number_input("B inicial", value=0.8)
    
    with col2:
        B_fin = st.number_input("B final", value=3.0)
    
    dB = st.number_input("ΔB", value=0.5)

# 🔹 Df
    col3, col4 = st.columns(2)
    
    with col3:
        Df_ini = st.number_input("Df inicial", value=0.8)
    
    with col4:
       Df_fin = st.number_input("Df final", value=3.0)
    dDf = st.number_input("ΔDf", value=0.5)

    # =========================
    # 🔹 ZAPATA
    # =========================
    st.subheader("🔷 ZAPATA")
    
    tipo = st.selectbox("Tipo", [
        "CUADRADA (L = B)",
        "RECTANGULAR (L = 2B)",
        "RECTANGULAR (L = 3B)",
        "RECTANGULAR (L = 5B)",
        "RECTANGULAR (L = 10B)"
    ])

    if "CUADRADA" in tipo:
        k = 1
    elif "2B" in tipo:
        k = 2
    elif "3B" in tipo:
        k = 3
    elif "5B" in tipo:
        k = 5
    elif "10B" in tipo:
        k = 10

    if k == 1:
        metodo = st.selectbox("Método", ["Terzaghi", "General"])
    else:
        metodo = "General"

    # =========================
    # 🔹 NIVEL FREÁTICO
    # =========================
    st.subheader("🔷 NIVEL FREÁTICO")
    nf = st.radio(
    "nf",
    ["NO", "SI"],
    horizontal=True,
    label_visibility="collapsed"
)

    gamma_w = 0.0
    prof_nf = 0.0

    if nf == "SI":
        gamma_w = st.number_input("γ agua", value=1.0)
        prof_nf = st.number_input("Profundidad NF", value=4.8)

    # =========================
    # 🔹 FS
    # =========================
    st.subheader("🔷 FACTOR DE SEGURIDAD")
    FS = st.number_input("FS", value=3.0, label_visibility="collapsed")
    
    # =========================
    # BOTON CALCULAR
    # =========================    
    calcular = st.button("🧱 Calcular capacidad portante")

# =========================
# 🔹 FUNCIÓN SOLO DEL DIBUJO  (AQUÍ)
# =========================

def graficar_perfil(df, nf, prof_nf):

    fig, ax = plt.subplots(figsize=(2.1,2.7))

    colores = ["#f4b400", "#d9a066", "#b57bb3", "#8cc37e", "#7fb3d5"]

    z_top = 0

    for i, row in df.iterrows():
        esp = row["Espesor (m)"]
        z_bottom = z_top + esp

        color = colores[i % len(colores)]

        # Dibujar rectángulo
        ax.fill_between(
            [0, 1],
            z_top,
            z_bottom,
            color=color,
            edgecolor='black',   # 🔹 borde
            linewidth=1          # 🔹 grosor del borde
)

        # Texto del estrato
        texto = (
            f"ESTRATO {int(row['Estrato'])}\n"
            f"γ={row['γ (t/m³)']}\n"
            f"φ={row['φ (°)']}°\n"
            f"c={row['c (t/m²)']}"
        )

        ax.text(0.05, (z_top + z_bottom)/2, texto,
                 ha='left', va='center', fontsize=3.2)

        # Espesor a la izquierda
        
        # 🔹 línea de medida vertical
        ax.plot([-0.15, -0.15], [z_top, z_bottom], color='black')
        
        # 🔹 marcas horizontales (tipo cota)
        ax.plot([-0.18, -0.12], [z_top, z_top], color='black')
        ax.plot([-0.18, -0.12], [z_bottom, z_bottom], color='black')
        
        # 🔹 texto del espesor
        ax.text(-0.2, (z_top + z_bottom)/2,
        f"{esp:.2f} m",
        va='center', ha='right', fontsize=5)

        z_top = z_bottom

    # 🔹 Nivel freático
    if nf == "SI":
        ax.axhline(y=prof_nf, linestyle='--')
        ax.text(1.05, prof_nf, "NF", va='center')

    # Formato
    ax.set_xlim(-0.4, 1.2)
    ax.set_ylim(z_top, 0)  # invertir eje
    ax.axis('off')

    return fig
# =========================
# 🔹 TABLA DE PERFIL ESTAIGRAFICO como funcion 
# =========================

def graficar_tabla(df):
    fig, ax = plt.subplots(figsize=(8, 2.5))
    ax.axis('off')

    tabla = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc='center',
        cellLoc='center'
    )

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(8)
    tabla.scale(1, 1.4)

    # 🔥 Estilo encabezado
    for (row, col), cell in tabla.get_celld().items():
        if row == 0:
            cell.set_facecolor("#2b6cb0")
            cell.set_text_props(color='white', weight='bold')
        else:
            cell.set_facecolor("#edf2f7")

        cell.set_edgecolor("#cbd5e0")

    return fig

# =========================
# 🔹 PERFIL ESTAIGRAFICO TABLA
# =========================
st.subheader("🧱 Perfil estratigráfico")

st.markdown("""
<style>
.card {
    background-color: #eef2f7;
    padding: 29px;
    height: 100px;
    width: 97px;          /* 🔥 CLAVE: ancho fijo */
    border-radius: 20px;
    border-left: 5px solid #2b6cb0;
    text-align: center;
    font-size: 11px;
    margin: 2px auto;      /* 🔥 centra dentro de la columna */
}
.card-title {
    font-weight: bold;
    color: #4a5568;
    font-size: 17px;
    text-align: center;
}
.card-value {
    font-size: 18px;
    font-weight: 600;
    color: #1a202c;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Estrato": [1, 2, 3, 4],
        "Espesor (m)": [0.8, 1.0, 1.5, 4.0],
        "φ (°)": [29, 30, 31, 32],
        "c (t/m²)": [0.0, 0.5, 1.0, 1.5],
        "γ (t/m³)": [1.6, 1.5, 1.6, 1.7],
        "γsat (t/m³)": [None, None, None, 2.1]
    })

# 🔹 preparar df (OBLIGATORIO)
df = st.session_state.df.copy()
df = df.sort_values("Estrato").reset_index(drop=True)

# 🔥 CREAR COLUMNAS
c1, c2 = st.columns([4,5])

# =========================
# 🔹 TABLA (IZQUIERDA)
# =========================
with c1:

    st.markdown("### 📋 Perfil del suelo")

    st.markdown("<div style='max-width:700px;'>", unsafe_allow_html=True)

    # encabezados
    col_titles = st.columns(6)
    titulos = ["Estrato", "Espesor (m)", "φ (°)", "c (t/m²)", "γ", "γsat"]

    for col, t in zip(col_titles, titulos):
        col.markdown(f"<div class='card-title'>{t}</div>", unsafe_allow_html=True)

    # filas
    for _, row in df.iterrows():

        cols = st.columns([1,1,1,1,1,1])

        valores = [
            row["Estrato"],
            row["Espesor (m)"],
            row["φ (°)"],
            row["c (t/m²)"],
            row["γ (t/m³)"],
            row["γsat (t/m³)"]
        ]

        for col, val in zip(cols, valores):
            col.markdown(f"""
            <div class="card">
                <div class="card-value">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='width:650px;'>", unsafe_allow_html=True)
    # =========================
# 🔹 GRÁFICO (DERECHA)
# =========================
with c2:

    st.markdown("### 🖼️ Perfil")

    df["Espesor acum. (m)"] = df["Espesor (m)"].cumsum()

    fig = graficar_perfil(df, nf, prof_nf)

    st.pyplot(fig, use_container_width=False)
            
            

# =========================
# 🔹 FUNCIONES
# =========================

def calcular_q(df, z_inicio, z_fin, prof_nf, gamma_w, nf):
    q = 0
    z_acum = 0

    for _, row in df.iterrows():
        espesor = row["Espesor (m)"]
        gamma = row["γ (t/m³)"]
        gamma_sat = row["γsat (t/m³)"]

        z_sup = z_acum
        z_inf = z_acum + espesor

        if z_inf <= z_inicio:
            z_acum = z_inf
            continue

        if z_sup >= z_fin:
            break

        tramo = min(z_inf, z_fin) - max(z_sup, z_inicio)

        if tramo > 0:

            if nf == "SI" and z_sup >= prof_nf and pd.notnull(gamma_sat):
                gamma_eff = gamma_sat - gamma_w
            else:
                gamma_eff = gamma

            q += tramo * gamma_eff

        z_acum = z_inf

    return q

# =========================
# 🔹 TERZAGUI CUADRADA
# =========================

def gamma_promedio_bajo_base(df, z_base, B, prof_nf, gamma_w):
    z_top = z_base
    z_bottom = z_base + B

    suma = 0
    z_acum = 0

    for _, row in df.iterrows():
        espesor = row["Espesor (m)"]
        gamma = row["γ (t/m³)"]
        gamma_sat = row["γsat (t/m³)"]

        z_sup = z_acum
        z_inf = z_acum + espesor

        if z_inf <= z_top:
            z_acum = z_inf
            continue

        if z_sup >= z_bottom:
            break

        tramo = min(z_inf, z_bottom) - max(z_sup, z_top)

        if tramo > 0:
            z_mid = (max(z_sup, z_top) + min(z_inf, z_bottom)) / 2

            if z_mid >= prof_nf and pd.notnull(gamma_sat):
                gamma_eff = gamma_sat - gamma_w
            else:
                gamma_eff = gamma

            suma += gamma_eff * tramo

        z_acum = z_inf

    return suma / B


def obtener_propiedades_en_Df(df, z_base):
    z_sup = 0

    for _, row in df.iterrows():
        z_inf = z_sup + row["Espesor (m)"]

        if z_sup <= z_base < z_inf:
            return row

        z_sup = z_inf

    return df.iloc[-1]


terzaghi_table = {
    30: (37.16, 22.46, 19.13),
    31: (40.41, 25.28, 22.65),
    32: (44.04, 28.52, 26.87),
    33: (48.09, 32.23, 31.94),
    34: (52.64, 36.50, 38.04),
    35: (57.75, 41.44, 45.41),
}

def obtener_factores_terzaghi(phi):
    phi = round(phi)
    if phi not in terzaghi_table:
        st.error(f"φ = {phi}° no está en la tabla")
        return 0, 0, 0
    return terzaghi_table[phi]


def terzaghi_cuadrada(df, h, Df, B, FS, nf, prof_nf, gamma_w):

    z_base = h + Df
    row = obtener_propiedades_en_Df(df, z_base)

    phi = row["φ (°)"]
    c = row["c (t/m²)"]
    gamma_nat = row["γ (t/m³)"]
    gamma_sat = row["γsat (t/m³)"]

    if pd.notnull(gamma_sat):
        gamma_eff = gamma_sat - gamma_w
    else:
        gamma_eff = gamma_nat

    d = prof_nf - z_base

    if nf == "SI" and prof_nf <= z_base:
        q = calcular_q(df, h, z_base, prof_nf, gamma_w, nf)
        gamma = gamma_eff
        caso = "Caso 1"

    elif nf == "SI" and 0 < d <= B:
        q = calcular_q(df, h, z_base, prof_nf, gamma_w, nf)
        gamma = gamma_eff + (d / B) * (gamma_nat - gamma_eff)
        caso = "Caso 2"

    else:
        q = calcular_q(df, h, z_base, prof_nf, gamma_w, nf)
        gamma = gamma_nat
        caso = "Caso 3"

    Nc, Nq, Ngamma = obtener_factores_terzaghi(phi)

    # 🔥 TÉRMINOS SEPARADOS
    term1 = 1.3 * c * Nc
    term2 = q * Nq
    term3 = 0.4 * gamma * B * Ngamma
    
    qult = term1 + term2 + term3
    qadm = qult / FS
    
    return {
    "phi": phi,
    "c": c,
    "gamma": gamma,
    "q": q,
    "qult": qult,
    "qadm": qadm,
    "caso": caso,

    # 🔥 NUEVO
    "Nc": Nc,
    "Nq": Nq,
    "Ngamma": Ngamma,
    "term1": term1,
    "term2": term2,
    "term3": term3
}


# =========================
# 🔹 CAPACIDAD GENERAL
# =========================



# =========================
# 🔹 GENERAL
# ========================= 

def capacidad_general(df, h, Df, B, L, FS, nf, prof_nf, gamma_w, beta):

    import numpy as np

    z_base = h + Df
    row = obtener_propiedades_en_Df(df, z_base)

    phi = row["φ (°)"]
    c = row["c (t/m²)"]
    gamma_nat = row["γ (t/m³)"]
    gamma_sat = row["γsat (t/m³)"]

    # γ efectivo
    if pd.notnull(gamma_sat):
        gamma_eff = gamma_sat - gamma_w
    else:
        gamma_eff = gamma_nat

    d = prof_nf - z_base

    # =========================
    # CASOS NIVEL FREÁTICO
    # =========================
    if nf == "SI" and prof_nf <= z_base:
        q = calcular_q(df, h, z_base, prof_nf, gamma_w, nf)
        gamma = gamma_eff
        caso = "Caso 1"

    elif nf == "SI" and 0 < d <= B:
        q = calcular_q(df, h, z_base, prof_nf, gamma_w, nf)
        gamma = gamma_eff + (d / B) * (gamma_nat - gamma_eff)
        caso = "Caso 2"

    else:
        q = calcular_q(df, h, z_base, prof_nf, gamma_w, nf)
        gamma = gamma_nat
        caso = "Caso 3"

    # =========================
    # FACTORES DE CAPACIDAD
    # =========================
    phi_rad = np.radians(phi)
    
    if abs(phi) < 1e-6:
        Nc = 5.14
        Nq = 1
        Ngamma = 0
    
    else:
        tan_phi = np.tan(phi_rad)
        Nq = np.exp(np.pi * tan_phi) * (np.tan(np.radians(45) + phi_rad/2))**2
        Nc = (Nq - 1) / tan_phi
        Ngamma = 2 * (Nq + 1) * tan_phi
        
        
    # =========================
    # 🔹 FORMA (De Beer)
    # =========================
    Fcs = 1 + (B/L)*(Nq/Nc)
    Fqs = 1 + (B/L)*np.tan(phi_rad)
    Fgs = 1 - 0.4*(B/L)

    # =========================
    # 🔹 PROFUNDIDAD (Hansen)
    # =========================
    if Df/B <= 1:
        if phi > 0:
            Fqd = 1 + 2*np.tan(phi_rad)*(1 - np.sin(phi_rad))**2 * (Df/B)
            Fcd = Fqd - (1 - Fqd)/(Nc*np.tan(phi_rad))
        else:
            Fcd = 1 + 0.4*(Df/B)
            Fqd = 1
        Fgd = 1
    else:
        if phi > 0:
            Fqd = 1 + 2*np.tan(phi_rad)*(1 - np.sin(phi_rad))**2 * np.arctan(Df/B)
            Fcd = Fqd - (1 - Fqd)/(Nc*np.tan(phi_rad))
        else:
            Fcd = 1 + 0.4*np.arctan(Df/B)
            Fqd = 1
        Fgd = 1

    # =========================
    # 🔹 INCLINACIÓN (Meyerhof)
    # =========================
    Fci = (1 - beta/90)**2
    Fqi = (1 - beta/90)**2

    if phi > 0:
        Fgi = (1 - beta/phi)**2
    else:
        Fgi = 1
    # =========================
    # 🔹 TÉRMINOS (DESGLOSE)
    # =========================
    term1 = c * Nc * Fcs * Fcd * Fci
    term2 = q * Nq * Fqs * Fqd * Fqi
    term3 = 0.5 * gamma * B * Ngamma * Fgs * Fgd * Fgi
    
    # =========================
    # 🔥 ECUACIÓN GENERAL COMPLETA
    # =========================
    qult = term1 + term2 + term3
    qadm = qult / FS

    return {
    "phi": phi,
    "c": c,
    "gamma": gamma,
    "q": q,
    "qult": qult,
    "qadm": qadm,
    "caso": caso,

    # 🔹 FACTORES
    "Nc": Nc,
    "Nq": Nq,
    "Ngamma": Ngamma,

    "Fcs": Fcs,
    "Fqs": Fqs,
    "Fgs": Fgs,

    "Fcd": Fcd,
    "Fqd": Fqd,
    "Fgd": Fgd,

    "Fci": Fci,
    "Fqi": Fqi,
    "Fgi": Fgi,

    # 🔹 TÉRMINOS
    "term1": term1,
    "term2": term2,
    "term3": term3,

    # 🔹 CONTROL (para tu interfaz)
    "Df_B": Df / B,
    "phi_cond": "φ > 0" if phi > 0 else "φ = 0"
}
# =========================
# 🔹 CÁLCULO
# =========================

tab1, tab2, tab3 = st.tabs([
    "📐 Teoría", "📊 Resultados", "📈 Gráficos"
])

if calcular:
    
 resultados = []

 B_actual = B_ini
 while B_actual <= B_fin + 1e-6:

     Df_actual = Df_ini
     while Df_actual <= Df_fin + 1e-6:

         L = k * B_actual

         if metodo == "Terzaghi":
             res = terzaghi_cuadrada(df, h, Df_actual, B_actual, FS, nf, prof_nf, gamma_w)
         else:
             res = capacidad_general(df, h, Df_actual, B_actual, L, FS, nf, prof_nf, gamma_w, beta)

         A = B_actual * L
         Q = res["qadm"] * A
         
         resultados.append({
             "B (m)": B_actual,
             "Df (m)": Df_actual,
             "L (m)": L,
             "Área (m²)": A,
             "φ (°)": res["phi"],
             "c (t/m²)": res["c"],
             "γ (t/m³)": res["gamma"],
             "q": res["q"],
             "q_ult": res["qult"],
             "q_adm": res["qadm"],
             "Q (t)": Q,
             "Caso": res["caso"],
         })
         Df_actual += dDf

     B_actual += dB

 # guardar tabla
 st.session_state.df_res = pd.DataFrame(resultados)

 # 🔥 GUARDAR CASO BASE (valores iniciales)
 B0 = B_ini
 Df0 = Df_ini
 L0 = k * B0

 if metodo == "Terzaghi":
     res0 = terzaghi_cuadrada(df, h, Df0, B0, FS, nf, prof_nf, gamma_w)
 else:
     res0 = capacidad_general(df, h, Df0, B0, L0, FS, nf, prof_nf, gamma_w, beta)

 st.session_state.teoria = {
     "B": B0,
     "Df": Df0,
     "L": L0,
     "res": res0,
     "formula": metodo
 }

 st.success("✅ Cálculo realizado.")


# 🔥 RESETEAR TEORÍA SI CAMBIAN INPUTS
if "teoria_inputs" not in st.session_state:
    st.session_state.teoria_inputs = {}

current_inputs = {
    "B_ini": B_ini,
    "Df_ini": Df_ini,
    "metodo": metodo,
    "nf": nf,
    "FS": FS,
    "tipo": tipo
}

if st.session_state.teoria_inputs != current_inputs:
    st.session_state.teoria = None
    st.session_state.teoria_inputs = current_inputs
    
    
    
# =========================
# 📐 TAB 1: TEORÍA PRO (COMPACTA)
# =========================
with tab1:

    st.header("📐 Teoría & Ecuaciones")

    # =========================
    # 🔹 MÉTODOS
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Terzaghi (1943)**")
        st.latex(r"q_{ult} = 1.3cN_c + qN_q + 0.4\gamma BN_\gamma")

        st.caption("c: cohesión · q: sobrecarga · γ: peso unitario · B: ancho")

    with col2:
        st.markdown("**Método General**")
        st.latex(r"q_{ult} = cN_cF_c + qN_qF_q + 0.5\gamma BN_\gamma F_\gamma")

        st.caption("Incluye factores de forma, profundidad e inclinación")

    st.divider()

    # =========================
    # 🔹 FACTORES Nc, Nq, Nγ
    # =========================
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("**Factores de capacidad portante**")
        st.caption("Dependen del ángulo de fricción φ")

    with col2:
        st.latex(r"N_q = e^{\pi \tan\phi} \tan^2\left(45^\circ + \frac{\phi}{2}\right)")
        st.latex(r"N_c = \frac{N_q - 1}{\tan\phi}")
        st.latex(r"N_\gamma = 2(N_q + 1)\tan\phi")

    st.divider()

    # =========================
    # 🔹 CORRECCIONES (ULTRA LIMPIO)
    # =========================
    col1, col2, col3 = st.columns(3)

    col1.markdown("**Forma**  \nB/L")
    col2.markdown("**Profundidad**  \nDf/B")
    col3.markdown("**Inclinación**  \nβ")

    st.divider()

    # =========================
    # 🔹 NIVEL FREÁTICO
    # =========================
    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown("**Nivel freático**")
        st.caption("Afecta el peso efectivo del suelo")

    with col2:
        st.markdown("""
        • Sobre base → γ efectivo  
        • Dentro de B → interpolación  
        • Profundo → γ natural  
        """)

# =========================
# TAB 2: RESULTADOS
# =========================
with tab2:

    st.subheader("📊 Resultados")

    if "teoria" in st.session_state and st.session_state.teoria is not None:

        teo = st.session_state.teoria
        res = teo["res"]

        es_cuadrada = abs(teo["L"] - teo["B"]) < 1e-6

        # =========================
        # 🔹 MÉTODO
        # =========================
        if teo["formula"] == "Terzaghi" and es_cuadrada:
            metodo_txt = "Método de Terzaghi"
            formula_txt = r"q_{ult} = 1.3cN_c + qN_q + 0.4\gamma BN_\gamma"
        else:
            metodo_txt = "Método General"
            formula_txt = r"q_{ult} = cN_cF_c + qN_qF_q + 0.5\gamma BN_\gamma F_\gamma"

            if not es_cuadrada:
                st.warning("⚠️ Geometría rectangular → se aplica método general")

        st.markdown(f"## 📐 {metodo_txt}")
        st.latex(formula_txt)

        st.divider()

        # =========================
        # 🔹 DATOS
        # =========================
        st.markdown("### 🔹 Datos de entrada")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("B (m)", f"{teo['B']:.2f}")
        c2.metric("Df (m)", f"{teo['Df']:.2f}")
        c3.metric("L (m)", f"{teo['L']:.2f}")
        c4.metric("φ (°)", f"{res['phi']:.0f}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("c (t/m²)", f"{res['c']:.2f}")
        c2.metric("γ (t/m³)", f"{res['gamma']:.2f}")
        c3.metric("q (t/m²)", f"{res['q']:.2f}")
        c4.metric("Caso", f"{res['caso']}")

        st.divider()

        # =========================
        # 🔹 FACTORES
        # =========================
        st.markdown("### 🔹 Factores de capacidad")

        f1, f2, f3 = st.columns(3)
        f1.metric("Nc", f"{res['Nc']:.2f}")
        f2.metric("Nq", f"{res['Nq']:.2f}")
        f3.metric("Nγ", f"{res['Ngamma']:.2f}")

        # =========================
        # 🔹 GENERAL → FACTORES EXTRA
        # =========================
        if metodo_txt == "Método General":
            
            st.info(f"Df/B = {res['Df_B']:.2f} → {res['phi_cond']}")

            st.markdown("### 🔹 Factores de corrección")

            f1, f2, f3 = st.columns(3)
            f1.metric("Fcs", f"{res['Fcs']:.2f}")
            f2.metric("Fcd", f"{res['Fcd']:.2f}")
            f3.metric("Fci", f"{res['Fci']:.2f}")

            f1, f2, f3 = st.columns(3)
            f1.metric("Fqs", f"{res['Fqs']:.2f}")
            f2.metric("Fqd", f"{res['Fqd']:.2f}")
            f3.metric("Fqi", f"{res['Fqi']:.2f}")

            f1, f2, f3 = st.columns(3)
            f1.metric("Fgs", f"{res['Fgs']:.2f}")
            f2.metric("Fgd", f"{res['Fgd']:.2f}")
            f3.metric("Fgi", f"{res['Fgi']:.2f}")

        st.divider()

        # =========================
        # 🔹 TÉRMINOS
        # =========================
        st.markdown("### 🔹 Desglose de términos")

        t1, t2, t3 = st.columns(3)

        if metodo_txt == "Método de Terzaghi":
            t1.metric("1.3·c·Nc", f"{res['term1']:.2f}")
            t2.metric("q·Nq", f"{res['term2']:.2f}")
            t3.metric("0.4·γ·B·Nγ", f"{res['term3']:.2f}")
        else:
            t1.metric("c·Nc·Fc", f"{res['term1']:.2f}")
            t2.metric("q·Nq·Fq", f"{res['term2']:.2f}")
            t3.metric("0.5·γ·B·Nγ·Fγ", f"{res['term3']:.2f}")

        st.divider()

        # =========================
        # 🔹 RESULTADOS
        # =========================
        st.markdown("### 🔹 Resultados finales")

        r1, r2 = st.columns(2)

        r1.success(f"q_ult = {res['qult']:.2f} t/m²")
        r2.success(f"q_adm = {res['qadm']:.2f} t/m²")

        st.divider()

    # =========================
    # 🔹 TABLA
    # =========================
    if "df_res" in st.session_state:
        st.markdown("## 📋 Tabla de iteraciones")
        st.dataframe(st.session_state.df_res, use_container_width=True)
    else:
        st.info("⬅️ Presiona 'Calcular capacidad portante'")

# =========================
# 🔹 TAB 3: GRÁFICOS
# =========================
with tab3:

    if "df_res" in st.session_state:

        import matplotlib.ticker as ticker
        import numpy as np

        df_res = st.session_state.df_res.copy()
        df_res["Df (m)"] = df_res["Df (m)"].round(2)
        
        st.markdown(f"### Capacidad portante ({metodo})")

        tabla = df_res.pivot_table(
            index="B (m)",
            columns="Df (m)",
            values="q_adm"
        )

        plt.style.use("seaborn-v0_8-whitegrid")

        fig, ax = plt.subplots(figsize=(4, 3))

        colores = ["#2b6cb0", "#2f855a", "#b7791f", "#c53030", "#6b46c1"]

        # 🔹 graficar curvas
        for i, df_val in enumerate(tabla.columns):
            ax.plot(
                tabla.index,
                tabla[df_val],
                marker='o',
                linewidth=1.8,
                markersize=4,
                color=colores[i % len(colores)],
                label=f"Df={df_val}"
            )

        # =========================
        # 🔥 PUNTO ÓPTIMO GLOBAL
        # =========================
        max_val = tabla.max().max()

        # ubicación del máximo
        idx_max = np.where(tabla == max_val)
        fila = idx_max[0][0]
        col = idx_max[1][0]

        B_opt = tabla.index[fila]
        Df_opt = tabla.columns[col]

        # 🔴 texto
        ax.annotate(
            f"Máx\nB={B_opt:.2f}\nq={max_val:.1f}",
            (B_opt, max_val),
            textcoords="offset points",
            xytext=(5,5),
            fontsize=7
        )

        # =========================
        # 🔹 EJES PRO
        # =========================
        ax.set_xlabel("B (m)", fontsize=9)
        ax.set_ylabel("q adm (t/m²)", fontsize=9)
       

        # 🔥 eje X REAL (clave)
        ax.set_xticks(tabla.index)
        ax.set_xticklabels([f"{x:.2f}" for x in tabla.index])

        # 🔥 eje Y técnico
        ax.yaxis.set_major_locator(ticker.MultipleLocator(5))

        ax.tick_params(axis='both', labelsize=5)

        # 🔹 grid fino
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.6)

        # 🔹 limpiar bordes
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # 🔹 leyenda fuera
        ax.legend(
            title="Df",
            fontsize=7,
            title_fontsize=8,
            frameon=True,
            loc='center left',
            bbox_to_anchor=(1.02, 0.5)
        )

        plt.subplots_adjust(right=0.70)

        ax.set_ylim(bottom=0)

        plt.tight_layout()

        st.pyplot(fig, use_container_width=False)
        

# =========================
# 🔹 TAB 3: HEATMAP PRO
# =========================
with tab3:

    if "df_res" in st.session_state:

        import numpy as np

        df_res = st.session_state.df_res.copy()

        # 🔹 detectar método
        metodo = st.session_state.teoria["formula"] if "teoria" in st.session_state and st.session_state.teoria else "General"
        st.markdown(f"### 🔥 Mapa de calor ({metodo})")

        # =========================
        # 🔹 TABLA BASE
        # =========================
        tabla_hm = df_res.pivot_table(
            index="Df (m)",
            columns="B (m)",
            values="q_adm"
        )

        # =========================
        # 🔹 FIGURA
        # =========================
        fig2, ax2 = plt.subplots(figsize=(4, 3))

        # 🔥 USAR imshow BIEN CONFIGURADO (más limpio que pcolormesh)
        c = ax2.imshow(
            tabla_hm.values,
            cmap="Blues",
            aspect="auto",
            interpolation="none"   # 🔥 CLAVE: elimina suavizado = elimina líneas
        )

        # =========================
        # 🔹 EJES (SOLO UNA VEZ)
        # =========================
        ax2.set_xticks(np.arange(len(tabla_hm.columns)))
        ax2.set_yticks(np.arange(len(tabla_hm.index)))

        ax2.set_xticklabels([f"{x:.2f}" for x in tabla_hm.columns], fontsize=8)
        ax2.set_yticklabels([f"{y:.2f}" for y in tabla_hm.index], fontsize=8)

        ax2.set_xlabel("B (m)", fontsize=9)
        ax2.set_ylabel("Df (m)", fontsize=9)
        ax2.set_title("qa (t/m²)", fontsize=10)

        # 🔥 QUITAR GRID COMPLETAMENTE
        ax2.grid(False)

        # 🔥 quitar ticks visuales
        ax2.tick_params(axis='both', length=0)

        # 🔥 quitar bordes
        for spine in ax2.spines.values():
            spine.set_visible(False)

        # =========================
        # 🔹 TEXTO CENTRADO PERFECTO
        # =========================
        media = tabla_hm.values.mean()

        for i in range(len(tabla_hm.index)):
            for j in range(len(tabla_hm.columns)):

                val = tabla_hm.iloc[i, j]

                ax2.text(
                    j, i,
                    f"{val:.0f}",
                    ha='center',
                    va='center',
                    fontsize=7,
                    color="white" if val > media else "black"
                )

        # =========================
        # 🔹 COLORBAR LIMPIO + INVERTIDO
        # =========================
        cbar = fig2.colorbar(c, ax=ax2, fraction=0.04, pad=0.03)

        cbar.set_label("qa (t/m²)", fontsize=9)

        cbar.ax.tick_params(
            labelsize=8,
            width=1,
            length=5,
            direction='out'
        )

        # 🔥 invertir escala
        cbar.ax.invert_yaxis()

        plt.tight_layout()

        st.pyplot(fig2, use_container_width=False)

    else:
        st.info("⬅️ Presiona 'Calcular capacidad portante'")
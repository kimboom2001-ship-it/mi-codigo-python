import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cimentaciones", layout="wide")


st.markdown("""
<style>

/* 🔹 VALORES (números) */
[data-testid="stMetricValue"] {
    font-size: 26px !important;
    font-weight: 600;
}

/* 🔥 ETIQUETAS (Nc, B, etc.) */
[data-testid="stMetricLabel"] > div {
    font-size: 26px !important;
    font-weight: 600;
}

/* 🔹 CONTENEDOR */
div[data-testid="stMetric"] {
    padding: 4px 6px;
}

</style>
""", unsafe_allow_html=True)

# 🔹 ESTILO GENERAL (ancho)
st.markdown("""
<style>
.main .block-container {
    max-width: 1000px;
    margin: auto;
}
</style>
""", unsafe_allow_html=True)


st.title("🏗️ 𝐀𝐍Á𝐋𝐈𝐒𝐈𝐒 𝐃𝐄 𝐂𝐀𝐏𝐀𝐂𝐈𝐃𝐀𝐃 𝐏𝐎𝐑𝐓𝐀𝐍𝐓𝐄 𝐃𝐄 𝐂𝐈𝐌𝐄𝐍𝐓𝐀𝐂𝐈𝐎𝐍𝐄𝐒​​​​​​​​​​")


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
    # 🔹 GEOMETRÍA
    # =========================
    st.subheader("📐GEOMETRÍA")

    # 🔹 B
    col1, col2 = st.columns(2)
    
    with col1:
        B_ini = st.number_input("B inicial", value=0.8)
    
    with col2:
        B_fin = st.number_input("B final", value=3.0)
    
    dB = st.number_input("ΔB", value=0.4)

# 🔹 Df
    col3, col4 = st.columns(2)
    
    with col3:
        Df_ini = st.number_input("Df inicial", value=0.8)
    
    with col4:
       Df_fin = st.number_input("Df final", value=3.0)
    dDf = st.number_input("ΔDf", value=0.4)
    
    
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

   
    # =========================
    # 🔹 MÉTODO / CRITERIO
    # =========================

    if k == 1:

      metodo = st.selectbox(
        "Método",
        [
            "Terzaghi",
            "General",
            "RNE",
            "CRITERIOS"
        ]
    )

    else:

      metodo = st.selectbox(
        "Método",
        [
            "General",
            "RNE",
            "CRITERIOS"
        ]
    ) 
    # ========================= 
    # 🔹 INCLINACIÓN 
    # =========================
    beta = 0

    if metodo in ["General", "RNE"]:
      beta = st.selectbox("β (°)", [0, 1])

    # =====================================
    # 📐 EXCENTRICIDAD
    # =====================================

    st.sidebar.markdown("### 📐 Excentricidad")

    usar_excentricidad = st.sidebar.checkbox(
        "Considerar excentricidad",
        value=False
    )

    if usar_excentricidad:

        e1 = st.sidebar.number_input(
            "e₁ (m)",
            min_value=0.0,
            value=0.0,
            step=0.01
        )

        e2 = st.sidebar.number_input(
            "e₂ (m)",
            min_value=0.0,
            value=0.0,
            step=0.01
        )

    else:

        e1 = 0.0
        e2 = 0.0

    # =========================
    # 🔹 NIVEL FREÁTICO
    # =========================
    st.subheader("💧 NIVEL FREÁTICO")
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
    st.subheader("🛡️ FACTOR DE SEGURIDAD")
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

        # 🔵 Línea NF
        ax.axhline(
            y=prof_nf,
            linestyle='--',
            color='blue',
            linewidth=1
        )

        # 🔵 Texto "NF"
        ax.text(
            1.10, prof_nf, "NF",
            va='center',
            ha='left',
            fontsize=8,
            color='blue'
        )

        # 🔹 COTA DERECHA
        x_cota = 1.05

        ax.plot(
            [x_cota, x_cota],
            [0, prof_nf],
            color='blue',
            linewidth=1
        )

        ax.plot(
            [x_cota - 0.03, x_cota + 0.03],
            [0, 0],
            color='blue'
        )

        ax.plot(
            [x_cota - 0.03, x_cota + 0.03],
            [prof_nf, prof_nf],
            color='blue'
        )

        ax.text(
            x_cota + 0.05,
            prof_nf / 2,
            f"{prof_nf:.2f} m",
            va='center',
            ha='left',
            fontsize=6.5,
            color='blue'
        )

    # 🔹 Formato
    ax.set_xlim(-0.4, 1.2)
    ax.set_ylim(z_top, 0)
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
st.subheader("🧱 ＰＥＲＦＩＬ　ＥＳＴＡＴＩＧＲÁＦＩＣＯ")

st.markdown("""
<style>
.card {
    background-color: #eef2f7;
    padding: 29px;
    height: 22px;
    width: 97px;          /* 🔥 CLAVE: ancho fijo */
    border-radius: 20px;
    border-left: 5px solid #2b6cb0;
    text-align: center;
    font-size: 11px;
    margin: 2px auto;     /* 🔥 centra dentro de la columna */
    /* 🔥 CENTRADO REAL */
    display: flex;
    justify-content: center;
    align-items: center;
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
c1, c2 = st.columns([3,3])

# =========================
# 🔹 TABLA (IZQUIERDA)
# =========================
with c1:

    st.markdown("### 🟣 𝐓𝐚𝐛𝐥𝐚: 𝐝𝐚𝐭𝐨𝐬 𝐝𝐞 𝐩𝐞𝐫𝐟𝐢𝐥")

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

    st.markdown("### 🟩🟥🟧🟨 𝐆𝐫á𝐟𝐢𝐜𝐨")

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
    
    q = calcular_q(df, h, z_base, prof_nf, gamma_w, nf)
    
    if nf == "SI":
        
        if d <= 0:
            gamma = gamma_eff
            caso = "Caso 1"
            
        elif 0 < d <= B:
            gamma = gamma_eff + (d / B) * (gamma_nat - gamma_eff)
            caso = "Caso 2"
        
        elif d > B:
            gamma = gamma_nat
            caso = "Caso 3"
    else:
        gamma = gamma_nat
        caso = "Sin NF"
    
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

def capacidad_general(df, h, Df, B, L, FS, nf, prof_nf, gamma_w, beta, e1=0, e2=0):

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
    
    q = calcular_q(df, h, z_base, prof_nf, gamma_w, nf)

    # =========================
    # CASOS NIVEL FREÁTICO
    # =========================
    if nf == "SI":
        
        if d <= 0:
            gamma = gamma_eff
            caso = "Caso 1"
            
        elif 0 < d <= B:
            gamma = gamma_eff + (d / B) * (gamma_nat - gamma_eff)
            caso = "Caso 2"
        
        elif d > B:
            gamma = gamma_nat
            caso = "Caso 3"
    else:
        gamma = gamma_nat
        caso = "Sin NF"

     # =====================================
     # 📐 DIMENSIONES EFECTIVAS
     # =====================================

    Bp = B - 2 * e2
    Lp = L - 2 * e1

    # Para factores de forma
    B_shape = min(Bp, Lp)
    L_shape = max(Bp, Lp)

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
        
    # =====================================
    # 📐 DIMENSIONES EFECTIVAS
    # =====================================
    
    Bp = B - 2 * e2
    Lp = L - 2 * e1
    
    # 🔥 menor dimensión siempre será B
    B_shape = min(Bp, Lp)
    L_shape = max(Bp, Lp)
    
    
    # =========================
    # 🔹 FORMA (De Beer)
    # =========================
    Fcs = 1 + (B_shape/L_shape)*(Nq/Nc)
    Fqs = 1 + (B_shape/L_shape)*np.tan(phi_rad)
    Fgs = 1 - 0.4*(B_shape/L_shape)
    
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
    "phi_cond": "φ > 0" if phi > 0 else "φ = 0",
    
    # 📐 EXCENTRICIDAD
    "Bp": Bp,
    "Lp": Lp
    }

# =========================
# 🔹 RNE LEGAL
# =========================

def capacidad_rne_legal(df, h, Df, B, L, FS, nf, prof_nf, gamma_w):

    import numpy as np

    z_base = h + Df
    row = obtener_propiedades_en_Df(df, z_base)

    phi = row["φ (°)"]
    c = row["c (t/m²)"]
    gamma_nat = row["γ (t/m³)"]

    q = calcular_q(df, h, z_base, prof_nf, gamma_w, nf)

    phi_rad = np.radians(phi)

    if abs(phi) < 1e-6:

        Nc = 5.14
        Nq = 1
        Ngamma = 0

    else:

        tan_phi = np.tan(phi_rad)

        Nq = np.exp(np.pi * tan_phi) * (
            np.tan(np.radians(45) + phi_rad / 2)
        )**2

        Nc = (Nq - 1) / tan_phi

        # 🔥 RNE LEGAL IDEALIZADO
        Ngamma = (Nq - 1) * np.tan(1.4 * phi_rad)

    # 🔥 SIN FACTORES
    term1 = c * Nc
    term2 = q * Nq
    term3 = 0.5 * gamma_nat * B * Ngamma

    qult = term1 + term2 + term3

    qadm = qult / FS

    return {

        "term1": term1,
        "term2": term2,
        "term3": term3,

        "qult": qult,
        "qadm": qadm
    }

# =========================
# 🔹 RNE
# =========================

def capacidad_rne(df, h, Df, B, L, FS, nf, prof_nf, gamma_w, beta, e1=0, e2=0):

    import numpy as np

    z_base = h + Df
    row = obtener_propiedades_en_Df(df, z_base)

    phi = row["φ (°)"]
    c = row["c (t/m²)"]
    gamma_nat = row["γ (t/m³)"]
    gamma_sat = row["γsat (t/m³)"]

    # =========================
    # γ efectivo
    # =========================
    if pd.notnull(gamma_sat):
        gamma_eff = gamma_sat - gamma_w
    else:
        gamma_eff = gamma_nat

    d = prof_nf - z_base

    q = calcular_q(df, h, z_base, prof_nf, gamma_w, nf)

    # =========================
    # NIVEL FREÁTICO
    # =========================
    if nf == "SI":

        if d <= 0:
            gamma = gamma_eff
            caso = "Caso 1"

        elif 0 < d <= B:
            gamma = gamma_eff + (d / B) * (gamma_nat - gamma_eff)
            caso = "Caso 2"

        else:
            gamma = gamma_nat
            caso = "Caso 3"

    else:
        gamma = gamma_nat
        caso = "Sin NF"

    # =========================
    # FACTORES RNE
    # =========================
    
    # =====================================
    # 📐 DIMENSIONES EFECTIVAS
    # =====================================

    Bp = B - 2 * e2
    Lp = L - 2 * e1

    # 🔥 menor dimensión siempre controla
    B_shape = min(Bp, Lp)
    L_shape = max(Bp, Lp)
    
    phi_rad = np.radians(phi)

    if abs(phi) < 1e-6:

        Nc = 5.14
        Nq = 1
        Ngamma = 0

    else:

        tan_phi = np.tan(phi_rad)

        Nq = np.exp(np.pi * tan_phi) * (
            np.tan(np.radians(45) + phi_rad / 2)
        )**2

        Nc = (Nq - 1) / tan_phi

        # 🔥 RNE
        Ngamma = (Nq - 1) * np.tan(1.4 * phi_rad)
        
        
    # =====================================
    # 📐 DIMENSIONES EFECTIVAS
    # =====================================

    Bp = B - 2 * e2
    Lp = L - 2 * e1

    # 🔥 menor dimensión controla
    B_shape = min(Bp, Lp)
    L_shape = max(Bp, Lp)


    # =========================
    # FACTORES DE FORMA (RNE)
    # =========================
    sc = 1 + 0.2 * (B_shape / L_shape)

    sg = 1 - 0.4 * (B_shape / L_shape)

    # =========================
    # FACTORES DE INCLINACIÓN
    # =========================
    ic = (1 - beta / 90)**2

    iq = (1 - beta / 90)**2

    if phi > 0:
        ig = (1 - beta / phi)**2
    else:
        ig = 1

    # =========================
    # TÉRMINOS RNE
    # =========================
    term1 = c * Nc * sc * ic

    term2 = q * Nq * iq

    term3 = 0.5 * gamma * B * Ngamma * sg * ig

    # =========================
    # CAPACIDAD PORTANTE
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

        # 🔹 FACTORES DE CAPACIDAD
        "Nc": Nc,
        "Nq": Nq,
        "Ngamma": Ngamma,

        # 🔹 FACTORES DE FORMA
        "Fcs": sc,
        "Fgs": sg,

        # 🔹 FACTORES DE INCLINACIÓN
        "Fci": ic,
        "Fqi": iq,
        "Fgi": ig,

        # 🔹 TÉRMINOS
        "term1": term1,
        "term2": term2,
        "term3": term3,
        
        # 🔹 CONTROL
        "Df_B": Df / B,
        
        # 📐 EXCENTRICIDAD
        "Bp": Bp,
        "Lp": Lp,
    }

# =========================
# 🔹 CÁLCULO
# =========================
def mostrar_tabla_criterio(df, titulo, color):

    st.markdown(
        f"""
        <div style="
            background:{color};
            color:white;
            padding:8px;
            border-radius:6px 6px 0 0;
            font-weight:700;
            text-align:center;
            font-size:16px;
        ">
            {titulo}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.table(
        df.style
        .format("{:.2f}", subset=df.columns[1:])
        .set_properties(**{
            "text-align": "center",
            "font-size": "13px"
        })
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", color),
                    ("color", "white"),
                    ("text-align", "center"),
                    ("font-weight", "bold")
                ]
            },
            {
                "selector": "td",
                "props": [
                    ("background-color", "#f8fafc"),
                    ("text-align", "center"),
                    ("color", "black")
                ]
            }
        ])
    )
tab1, tab2, tab3 = st.tabs([
    "🧠 ＴＥＯＲÍＡ", "📝 ＲＥＳＵＬＴＡＤＯＳ", "📈ＧＲÁＦＩＣＯＳ"
])

if calcular:

    # =========================================
    # 🔹 CRITERIOS
    # =========================================
    if metodo == "CRITERIOS":

        # 🔹 dimensiones base
        B0 = B_ini
        Df0 = Df_ini
        L0 = k * B0

        # =========================================
        # 🔹 GENERAL
        # =========================================

        res_general = capacidad_general(
            df,
            h,
            Df0,
            B0,
            L0,
            FS,
            nf,
            prof_nf,
            gamma_w,
            beta,
            e1,
            e2
        )

        # =========================================
        # 🔹 RNE LEGAL
        # =========================================

        res_rne_legal = capacidad_rne_legal(
            df,
            h,
            Df0,
            B0,
            L0,
            FS,
            nf,
            prof_nf,
            gamma_w
        )

        # =========================================
        # 🔹 RNE CORREGIDO
        # =========================================

        res_rne = capacidad_rne(
            df,
            h,
            Df0,
            B0,
            L0,
            FS,
            nf,
            prof_nf,
            gamma_w,
            beta,
            e1,
            e2
        )

        # =========================================
        # 🔹 GUARDAR
        # =========================================

        st.session_state.res_general = res_general
        st.session_state.res_rne_legal = res_rne_legal
        st.session_state.res_rne = res_rne

        st.session_state.teoria = {
            "formula": "CRITERIOS"
        }
        
        # 🔥 evitar error en TAB2 y TAB3
        st.session_state.df_res = pd.DataFrame()
        
    # =========================================
    # 🔹 MÉTODOS NORMALES
    # =========================================
    else:

     resultados = []

     B_actual = B_ini
     while B_actual <= B_fin + 1e-6:

        Df_actual = Df_ini
        while Df_actual <= Df_fin + 1e-6:

            L = k * B_actual

            if metodo == "Terzaghi":

                res = terzaghi_cuadrada(
                    df,
                    h,
                    Df_actual,
                    B_actual,
                    FS,
                    nf,
                    prof_nf,
                    gamma_w
                )

            elif metodo == "General":

                res = capacidad_general(
                    df,
                    h,
                    Df_actual,
                    B_actual,
                    L,
                    FS,
                    nf,
                    prof_nf,
                    gamma_w,
                    beta,
                    e1,
                    e2
                )

            elif metodo == "RNE":

                res = capacidad_rne(
                    df,
                    h,
                    Df_actual,
                    B_actual,
                    L,
                    FS,
                    nf,
                    prof_nf,
                    gamma_w,
                    beta,
                    e1,
                    e2
            )



            # =====================================
            # 📐 ÁREA EFECTIVA
            # =====================================

            if usar_excentricidad:

                Bp = B_actual - 2 * e2
                Lp = L - 2 * e1

                A = Bp * Lp

            else:

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
              
              # 🔥 NUEVO
              "Term1": res["term1"],
              "Term2": res["term2"],
              "Term3": res["term3"],
              "q_ult": res["qult"],
              "q_adm": res["qadm"],
              "Q (t)": Q,
              "Caso": res["caso"],
        })

            Df_actual += dDf

        B_actual += dB

     # ✅ guardar tabla
     st.session_state.df_res = pd.DataFrame(resultados)

     # ✅ CASO BASE (CORREGIDO)
     B0 = B_ini
     Df0 = Df_ini
     L0 = k * B0

     if metodo == "Terzaghi":
        res0 = terzaghi_cuadrada(
         df,
         h,
         Df0,
         B0,
         FS,
         nf,
         prof_nf,
         gamma_w
    )

     elif metodo == "General":
      res0 = capacidad_general(
        df,
        h,
        Df0,
        B0,
        L0,
        FS,
        nf,
        prof_nf,
        gamma_w,
        beta
    )

     elif metodo == "RNE":
      res0 = capacidad_rne(
        df,
        h,
        Df0,
        B0,
        L0,
        FS,
        nf,
        prof_nf,
        gamma_w,
        beta
    )

     st.session_state.teoria = {
        "B": B0,
        "Df": Df0,
        "L": L0,
        "beta": beta,
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
# 📐 TAB 1: ESTILOOOOO
# =========================
st.markdown("""
<style>
.box {
    background-color: #f7fafc;
    padding: 15px;
    border-radius: 12px;
    border-left: 5px solid #2b6cb0;
    margin-bottom: 10px;
}
.box-title {
    font-weight: bold;
    font-size: 14px;
    margin-bottom: 5px;
    color: #2d3748;
}
.box-text {
    font-size: 12px;
    color: #1a202c;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 📐 TAB 1: TEORÍA PRO (COMPACTA)
# =========================
with tab1:

    st.header("𝐅𝐮𝐧𝐝𝐚𝐦𝐞𝐧𝐭𝐨𝐬 𝐝𝐞 𝐜𝐚𝐩𝐚𝐜𝐢𝐝𝐚𝐝 𝐩𝐨𝐫𝐭𝐚𝐧𝐭𝐞")

    # =========================
    # 🔹 MÉTODOS
    # =========================
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="box">
        <div class="box-title">Terzaghi (1943)</div>
        <div class="box-text">
        Zapatas superficiales.<br>
        No incluye correcciones avanzadas.
        </div>
        </div>
        """, unsafe_allow_html=True)

        st.latex(r"q_{ult} = 1.3cN_c + qN_q + 0.4\gamma BN_\gamma")

    with c2:
        st.markdown("""
        <div class="box">
        <div class="box-title">Método General</div>
        <div class="box-text">
        Incluye forma, profundidad e inclinación.
        </div>
        </div>
        """, unsafe_allow_html=True)

        st.latex(r"q_{ult} = cN_cF_c + qN_qF_q + 0.5\gamma BN_\gamma F_\gamma")

    st.divider()

    # =========================
    # 🔹 FACTORES + CORRECCIONES
    # =========================
    c1, c2 = st.columns(2)

    # 🔹 FACTORES (IZQUIERDA)
    with c1:
        st.markdown("""
        <div class="box">
        <div class="box-title">Factores de capacidad</div>
        <div class="box-text">
        Dependen del ángulo de fricción φ.
        </div>
        </div>
        """, unsafe_allow_html=True)

        st.latex(r"""
        \begin{aligned}
        N_q &= e^{\pi \tan\phi} \tan^2\left(45^\circ + \frac{\phi}{2}\right) \\
        N_c &= \frac{N_q - 1}{\tan\phi} \\
        N_\gamma &= 2(N_q + 1)\tan\phi
        \end{aligned}
        """)

    # 🔹 CORRECCIONES (DERECHA)
    with c2:

        st.markdown("""
        <div class="box">
        <div class="box-title">Forma</div>
        <div class="box-text">Depende de B/L</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="box">
        <div class="box-title">Profundidad</div>
        <div class="box-text">Relación Df/B</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="box">
        <div class="box-title">Inclinación</div>
        <div class="box-text">Ángulo β</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # =========================
    # 🔹 NIVEL FREÁTICO
    # =========================
    st.markdown("""
    <div class="box">
    <div class="box-title">Nivel freático</div>
    <div class="box-text">
    • Sobre base → γ' <br>
    • Dentro de B → interpolación <br>
    • Profundo → γ natural
    </div>
    </div>
    """, unsafe_allow_html=True)
    
# =========================
# TAB 2: RESULTADOS
# =========================
with tab2:

    st.subheader("📊 𝐑𝐞𝐬𝐮𝐥𝐭𝐚𝐝𝐨𝐬")

    if "df_res" not in st.session_state or st.session_state.teoria is None:
        st.info("⬅️ Presiona 'Calcular capacidad portante'")
    
    else:

     teo = st.session_state.teoria
     
    # =====================================
    # 🔹 CRITERIOS
    # =====================================
    
    if teo["formula"] == "CRITERIOS":

        # 🔥 AGREGAR ESTO
        B0 = B_ini
        Df0 = Df_ini
        L0 = k * B0
 
        # =====================================
        # 🔹 CÁLCULOS BASE
        # =====================================

        # TERZAGHI
        if k == 1:

            r_ter = terzaghi_cuadrada(
                df, h, Df0, B0,
                FS, nf, prof_nf, gamma_w
            )

        # EGCC
        r_gen = capacidad_general(
            df, h, Df0, B0, L0,
            FS, nf, prof_nf,
            gamma_w, beta, e1, e2
        )

        # RNE MATEMÁTICO
        r_rne = capacidad_rne(
            df, h, Df0, B0, L0,
            FS, nf, prof_nf,
            gamma_w, beta, e1, e2
        )

        # =====================================
        # 🔹 TABLA 1 — CRITERIO ACADÉMICO
        # =====================================

        datos_academico = []

        # =========================
        # 🔹 TERZAGHI
        # =========================
        if k == 1:

            datos_academico.append({

                "Método": "TERZAGHI",

                "1ER":   r_ter["term1"],
                "2DO":   r_ter["term2"],
                "3ERO":  r_ter["term3"],

                "qu":    r_ter["qult"],
                "qadm":  r_ter["qadm"],
                "Qmáx":  r_ter["qadm"] * B0 * L0
            })

        # =========================
        # 🔹 EGCC
        # =========================
        datos_academico.append({

            "Método": "EGCC",

            "1ER":   r_gen["term1"],
            "2DO":   r_gen["term2"],
            "3ERO":  r_gen["term3"],

            "qu":    r_gen["qult"],
            "qadm":  r_gen["qadm"],
            "Qmáx":  r_gen["qadm"] * B0 * L0
        })

        # =========================
        # 🔹 RNE
        # =========================
        datos_academico.append({

            "Método": "RNE",

            "1ER":   r_rne["term1"],
            "2DO":   r_rne["term2"],
            "3ERO":  r_rne["term3"],

            "qu":    r_rne["qult"],
            "qadm":  r_rne["qadm"],
            "Qmáx":  r_rne["qadm"] * B0 * L0
        })

        # =========================
        # 🔹 DATAFRAME
        # =========================
        tabla_academico = pd.DataFrame(datos_academico)

        # 🔹 Renombrar columnas visualmente
        tabla_academico.columns = [
            "Método",
            "1ER",
            "2DO",
            "3ERO",
            "qu (kN/m²)",
            "qadm (kN/m²)",
            "Qmáx (kN)"
        ]

        # =========================
        # 🔹 MOSTRAR TABLA
        # =========================
        mostrar_tabla_criterio(
            tabla_academico,
            "CRITERIO ACADÉMICO COMPLETO",
            "#2563eb"
        )

        # =====================================
        # 🔹 TABLA 2 — RNE IDEALIZADO LEGAL
        # 🔹 (VERDE)
        # =====================================

        datos_legal = []

        phi_base = r_rne["phi"]
        c_base = r_rne["c"]

        # CLASIFICACIÓN
        if phi_base >= 20:

            tipo_suelo = "SUELO FRICCIONANTE"

        else:

            if c_base >= 1:

                tipo_suelo = "SUELO COHESIVO"

            else:

                tipo_suelo = "SUELO FRICCIONANTE"

        # TERZAGHI
        if k == 1:

            if tipo_suelo == "SUELO COHESIVO":

                t1 = r_ter["term1"]
                t2 = 0
                t3 = 0

            else:

                t1 = 0
                t2 = r_ter["term2"]
                t3 = r_ter["term3"]

            qu = t1 + t2 + t3
            qadm = qu / FS

            datos_legal.append({

                "Método": "TERZAGHI",

                "1ER": t1,
                "2DO": t2,
                "3ERO": t3,

                "qu (kN/m²)": qu,
                "qadm (kN/m²)": qadm,
                "Qmáx (kN)": qadm * B0 * L0
            })

        # EGCC
        if tipo_suelo == "SUELO COHESIVO":

            t1 = r_gen["term1"]
            t2 = 0
            t3 = 0

        else:

            t1 = 0
            t2 = r_gen["term2"]
            t3 = r_gen["term3"]

        qu = t1 + t2 + t3
        qadm = qu / FS

        datos_legal.append({

            "Método": "EGCC",

            "1ER": t1,
            "2DO": t2,
            "3ERO": t3,

            "qu (kN/m²)": qu,
            "qadm (kN/m²)": qadm,
            "Qmáx (kN)": qadm * B0 * L0
        })

        # RNE
        if tipo_suelo == "SUELO COHESIVO":

            t1 = r_rne["term1"]
            t2 = 0
            t3 = 0

        else:

            t1 = 0
            t2 = r_rne["term2"]
            t3 = r_rne["term3"]

        qu = t1 + t2 + t3
        qadm = qu / FS

        datos_legal.append({

            "Método": "RNE",

            "1ER": t1,
            "2DO": t2,
            "3ERO": t3,

            "qu (kN/m²)": qu,
            "qadm (kN/m²)": qadm,
            "Qmáx (kN)": qadm * B0 * L0
        })

        tabla_legal = pd.DataFrame(datos_legal)

        mostrar_tabla_criterio(
            tabla_legal,
            f"CRITERIO RNE IDEALIZADO LEGAL — {tipo_suelo}",
            "#16a34a"
        )

       
       # =====================================
       # 🔹 CRITERIO RNE CORREGIDO
       # =====================================

        datos_matematico = []

       # 🔥 Para este eje:
       # Se asume suelo FRICCIONANTE
       # → c = 0
       # → desaparece el 1ER término
       # → quedan activos 2DO y 3ERO

       # =========================
       # 🔹 TERZAGHI
       # =========================
        if k == 1:

           t1 = 0
           t2 = r_ter["term2"]
           t3 = r_ter["term3"]

           qu = t1 + t2 + t3
           qadm = qu / FS

           datos_matematico.append({

               "Método": "TERZAGHI",

               "1ER": t1,
               "2DO": t2,
               "3ERO": t3,

               "qu (kN/m²)": qu,
               "qadm (kN/m²)": qadm,
               "Qmáx (kN)": qadm * B0 * L0
           })

       # =========================
       # 🔹 EGCC
       # =========================

        t1 = 0
        t2 = r_gen["term2"]
        t3 = r_gen["term3"]

        qu = t1 + t2 + t3
        qadm = qu / FS

        datos_matematico.append({

           "Método": "EGCC",

           "1ER": t1,
           "2DO": t2,
           "3ERO": t3,

           "qu (kN/m²)": qu,
           "qadm (kN/m²)": qadm,
           "Qmáx (kN)": qadm * B0 * L0
       })

       # =========================
       # 🔹 RNE
       # =========================

        t1 = 0
        t2 = r_rne["term2"]
        t3 = r_rne["term3"]

        qu = t1 + t2 + t3
        qadm = qu / FS

        datos_matematico.append({

           "Método": "RNE",

           "1ER": t1,
           "2DO": t2,
           "3ERO": t3,

           "qu (kN/m²)": qu,
           "qadm (kN/m²)": qadm,
           "Qmáx (kN)": qadm * B0 * L0
       })

        tabla_matematico = pd.DataFrame(datos_matematico)

        mostrar_tabla_criterio(
           tabla_matematico,
           "CRITERIO RNE CORREGIDO — SUELO FRICCIONANTE",
           "#dc2626"
       )
    
         
    
    
    # =====================================
    # 🔹 MÉTODOS NORMALES
    # =====================================
    else:

        res = teo["res"]
        
        es_cuadrada = abs(teo["L"] - teo["B"]) < 1e-6

        # =========================
        # 🔹 MÉTODO
        # =========================
        if teo["formula"] == "Terzaghi" and es_cuadrada:

            metodo_txt = "Método de Terzaghi"

            formula_txt = r"""
q_{ult} = 1.3cN_c + qN_q + 0.4\gamma BN_\gamma
"""

        elif teo["formula"] == "General":

            metodo_txt = "Método General"

            formula_txt = r"""
q_{ult} =
cN_cF_{cs}F_{cd}F_{ci}
+
qN_qF_{qs}F_{qd}F_{qi}
+
0.5\gamma BN_\gamma F_{\gamma s}F_{\gamma d}F_{\gamma i}
"""

        elif teo["formula"] == "RNE":

            metodo_txt = "Método RNE"

            formula_txt = r"""
q_{ult} =
cN_c s_c i_c
+
qN_q i_q
+
0.5\gamma BN_\gamma s_\gamma i_\gamma
"""

        st.markdown(f"## 📐 {metodo_txt}")
        st.latex(formula_txt)
        
        # =========================
        # 🔹 DATOS (COMPACTO Y ORDENADO)
        # =========================
        st.markdown(
    "<h2 style='font-size:22px;'>🔹 Datos de entrada</h2>",
    unsafe_allow_html=True
)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("B (m)", f"{teo['B']:.2f}")
        c2.metric("Df (m)", f"{teo['Df']:.2f}")
        c3.metric("L (m)", f"{teo['L']:.2f}")
        c4.metric("φ (°)", f"{res['phi']:.0f}")
        
        if metodo_txt == "Método General":

         c1, c2, c3, c4, c5 = st.columns(5)

         c1.metric("c (t/m²)", f"{res['c']:.2f}")
         c2.metric("γ (t/m³)", f"{res['gamma']:.2f}")
         c3.metric("q (t/m²)", f"{res['q']:.2f}")
         c4.metric("β (°)", f"{teo['beta']:.2f}")
         c5.metric("Caso", res['caso'])
 
        else:
            
         c1, c2, c3, c4 = st.columns(4)
         c1.metric("c (t/m²)", f"{res['c']:.2f}")
         c2.metric("γ (t/m³)", f"{res['gamma']:.2f}")
         c3.metric("q (t/m²)", f"{res['q']:.2f}")
         c4.metric("Caso", res['caso'])
        
        # =========================
        # 🔹 FACTORES
        # =========================
        
        st.markdown(
    "<h2 style='font-size:22px;'>🔹 Factores de capacidad</h2>",
    unsafe_allow_html=True
)
        
        f1, f2, f3 = st.columns(3)
        f1.metric("Nc", f"{res['Nc']:.2f}")
        f2.metric("Nq", f"{res['Nq']:.2f}")
        f3.metric("Nγ", f"{res['Ngamma']:.2f}")
        
        # =========================
        # 🔹 FACTORES GENERAL (SI APLICA)
        # =========================
        if metodo_txt == "Método General":

          st.markdown(
        "<h2 style='font-size:20px;'>🔧 Factores de corrección</h2>",
        unsafe_allow_html=True
    )

          st.markdown(
    f"""
    <div style="
        font-size:22px;
        font-weight:600;
        margin-bottom:12px;
        color:#2d3748;
    ">
        Df/B = {res['Df_B']:.2f}
    </div>
    """,
    unsafe_allow_html=True
)
          
          f1, f2, f3 = st.columns(3)
          f1.metric("Fcs", f"{res['Fcs']:.2f}")
          f2.metric("Fcd", f"{res['Fcd']:.2f}")
          f3.metric("Fci", f"{res['Fci']:.2f}")
          
          f1, f2, f3 = st.columns(3)
          f1.metric("Fqs", f"{res['Fqs']:.2f}")
          f2.metric("Fqd", f"{res['Fqd']:.2f}")
          f3.metric("Fqi", f"{res['Fqi']:.2f}")
          
          f1, f2, f3 = st.columns(3)
          f1.metric("Fγs", f"{res['Fgs']:.2f}")
          f2.metric("Fγd", f"{res['Fgd']:.2f}")
          f3.metric("Fγi", f"{res['Fgi']:.2f}")
          
        # =========================
        # 🔹 TÉRMINOS
        # =========================
        st.markdown(
    "<h2 style='font-size:22px;'>🔹 Términos</h2>",
    unsafe_allow_html=True
)
        t1, t2, t3 = st.columns(3)
        
        if metodo_txt == "Método de Terzaghi":
            t1.metric("1.3·c·Nc (t/m²)", f"{res['term1']:.2f}")
            t2.metric("q·Nq (t/m²)", f"{res['term2']:.2f}")
            t3.metric("0.4·γ·B·Nγ (t/m²)", f"{res['term3']:.2f}")
            
        elif metodo_txt == "Método General":
            
            t1.metric("c·Nc·Fcs·Fcd·Fci", f"{res['term1']:.2f}")
            t2.metric("q·Nq·Fqs·Fqd·Fqi", f"{res['term2']:.2f}")
            t3.metric("0.5·γ·B·Nγ·Fgs·Fgd·Fgi", f"{res['term3']:.2f}")
        
        elif metodo_txt == "Método RNE":
            t1.metric("c·Nc·sc·ic", f"{res['term1']:.2f}")
            t2.metric("q·Nq·iq", f"{res['term2']:.2f}")
            t3.metric("0.5·γ·B·Nγ·sg·ig", f"{res['term3']:.2f}")
            
      # =========================
      # 🔹 RESULTADOS
      # =========================
        st.markdown(
    "<h2 style='font-size:22px;'>🔹 Resultados</h2>",
    unsafe_allow_html=True
)
        r1, r2 = st.columns(2)
        r1.success(f"q_ult = {res['qult']:.2f} t/m²")
        r2.success(f"q_adm = {res['qadm']:.2f} t/m²")

       # =========================
       # 🔹 TABLA DE ITERACIONES
       # =========================
        st.markdown("## 📋 Tabla de iteraciones")
        st.dataframe(st.session_state.df_res, use_container_width=True)
        
        
        # =========================
        # 🔹 MATRIZ q_ult
        # =========================
        df_res = st.session_state.df_res.copy()

        st.markdown("## 📑 Matriz de q_ult")

        tabla_qult = df_res.pivot(
            index="Df (m)",
            columns="B (m)",
            values="q_ult"
        )

        tabla_qult = (
            tabla_qult
            .sort_index()
            .sort_index(axis=1)
        )

        # 🔥 REDONDEAR ÍNDICES Y COLUMNAS
        tabla_qult.index = tabla_qult.index.round(2)
        tabla_qult.columns = tabla_qult.columns.round(2)

        # 🔥 CAMBIAR NOMBRE VISUAL
        tabla_qult.index.name = "Df/B"

        st.markdown(
            """
            <div style="
                background:#b91c1c;
                color:white;
                padding:8px;
                border-radius:6px 6px 0 0;
                font-weight:700;
                text-align:center;
                font-size:15px;
            ">
                SECCIÓN — q_ult (t/m²)
            </div>
            """,
            unsafe_allow_html=True
        )

        st.table(
    tabla_qult.style
    .format("{:.2f}")
    .set_properties(**{
        "text-align": "center",
        "font-size": "13px"
    })
    .set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#dc2626"),
                ("color", "white"),
                ("text-align", "center"),
                ("font-weight", "bold")
            ]
        },
        {
            "selector": "td",
            "props": [
                ("background-color", "#fee2e2"),
                ("text-align", "center"),
                ("color", "black")
            ]
        }
    ])
)
        
        
        
    
    
        # =========================
        # 🔹 TABLA TIPO EXCEL
        # =========================

        df_res = st.session_state.df_res.copy()

        # 🔥 REDONDEAR VALORES
        df_res["B (m)"] = df_res["B (m)"].round(2)
        df_res["Df (m)"] = df_res["Df (m)"].round(2)

        st.markdown("## 📑 Matriz de resultados")

        # 🔥 CREAR MATRIZ
        tabla_excel = df_res.pivot(
            index="Df (m)",
            columns="B (m)",
            values="q_adm"
        )

        # 🔥 REDONDEAR MATRIZ
        tabla_excel = tabla_excel.round(2)

        # 🔥 ORDENAR
        tabla_excel = (
            tabla_excel
            .sort_index()
            .sort_index(axis=1)
        )

        # 🔥 CAMBIAR NOMBRE VISUAL
        tabla_excel.index.name = "Df/B"

        # =========================
        # 🔹 TÍTULO DINÁMICO
        # =========================

        if metodo_txt == "Método de Terzaghi":

            titulo_excel = (
                "SECCIÓN — qu TERZAGHI "
                "— Cuadrada (t/m²)"
            )

        elif metodo_txt == "Método General":

            titulo_excel = (
                "SECCIÓN — qu MÉTODO GENERAL "
                "(t/m²)"
            )

        else:

            titulo_excel = (
                "SECCIÓN — qu RNE "
                "(t/m²)"
            )

        # =========================
        # 🔹 ENCABEZADO MORADO
        # =========================

        st.markdown(
            f"""
            <div style="
                background:#6b21a8;
                color:white;
                padding:8px;
                border-radius:6px 6px 0 0;
                font-weight:700;
                text-align:center;
                font-size:15px;
            ">
                {titulo_excel}
            </div>
            """,
            unsafe_allow_html=True
        )

        # =========================
        # 🔹 MOSTRAR TABLA
        # =========================

        st.table(
            tabla_excel.style
            .format("{:.2f}")
            .set_properties(**{
                "text-align": "center",
                "font-size": "13px"
            })
            .set_table_styles([
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#8b5cf6"),
                        ("color", "white"),
                        ("text-align", "center")
                    ]
                },
                {
                    "selector": "td",
                    "props": [
                        ("background-color", "#f3e8ff"),
                        ("text-align", "center"),
                        ("color", "black")
                    ]
                }
            ])
        )
            
        
# =========================
# 🔹 TAB 3: GRÁFICOS
# =========================
with tab3:

    if "df_res" in st.session_state:

        import matplotlib.ticker as ticker
        import numpy as np

        df_res = st.session_state.df_res.copy()
        df_res["Df (m)"] = df_res["Df (m)"].round(2)
        
        st.markdown(f"### 📈 𝐕𝐚𝐫𝐢𝐚𝐜𝐢ó𝐧 𝐝𝐞 𝐃𝐅 ({metodo})")

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
        st.markdown(f"### 🔥 𝐌𝐚𝐩𝐚 𝐝𝐞 𝐜𝐚𝐥𝐨𝐫 ({metodo})")

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
        
        # =========================
        # 🔹 CARGA vs B
        # =========================
        st.markdown("### 📊 𝐂𝐚𝐫𝐠𝐚 𝐯𝐬 𝐁")

        tabla_q = df_res.pivot_table(
            index="B (m)",
            columns="Df (m)",
            values="Q (t)"
        )

        # =========================
        # 🔹 FIGURA
        # =========================
        fig3, ax3 = plt.subplots(figsize=(4,3))

        colores = [
            "#2b6cb0",
            "#2f855a",
            "#b7791f",
            "#c53030",
            "#6b46c1"
        ]

        # =========================
        # 🔹 CURVAS
        # =========================
        for i, df_val in enumerate(tabla_q.columns):

            ax3.plot(
                tabla_q.index,
                tabla_q[df_val],
                marker='o',
                linewidth=1.8,
                markersize=4,
                color=colores[i % len(colores)],
                label=f"Df={df_val}"
            )

        # =========================
        # 🔥 PUNTO MÁXIMO GLOBAL
        # =========================
        max_val = tabla_q.max().max()

        idx_max = np.where(tabla_q == max_val)

        fila = idx_max[0][0]
        col = idx_max[1][0]

        B_opt = tabla_q.index[fila]
        Df_opt = tabla_q.columns[col]

        ax3.annotate(
            f"Máx\nB={B_opt:.2f}\nDf={Df_opt:.2f}\nQ={max_val:.1f}",
            (B_opt, max_val),
            textcoords="offset points",
            xytext=(5,5),
            fontsize=7
        )

        # =========================
        # 🔹 FORMATO
        # =========================
        ax3.set_xlabel("B (m)", fontsize=9)
        ax3.set_ylabel("Q (t)", fontsize=9)

        ax3.grid(
            True,
            linestyle='--',
            linewidth=0.5,
            alpha=0.6
        )

        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)

        ax3.legend(
            title="Df",
            fontsize=7,
            title_fontsize=8,
            frameon=True,
            loc='center left',
            bbox_to_anchor=(1.02, 0.5)
        )

        ax3.tick_params(
            axis='both',
            labelsize=7
        )

        plt.subplots_adjust(right=0.72)

        plt.tight_layout()

        st.pyplot(
            fig3,
            use_container_width=False
        )

    else:
        st.info("⬅️ Presiona 'Calcular capacidad portante'")

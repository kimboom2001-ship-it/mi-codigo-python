import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cimentaciones", layout="centered")
st.title("🧱 Análisis de Capacidad Portante")

# =========================
# 🔹 EDIFICACIÓN
# =========================
st.subheader("1. Edificación")

sotano = st.radio("¿Edificación con sótano?", ["NO", "SI"])

h = 0.0
if sotano == "SI":
    h = st.number_input("Profundidad de sótano h (m)", value=3.00)

# ========================= 
# 🔹 INCLINACIÓN 
# =========================
st.subheader("Condición de carga")

beta = st.selectbox("Ángulo de inclinación β (°)", [0, 1])

# =========================
# 🔹 GEOMETRÍA
# =========================
st.markdown("### 🔹 Base de zapata (B)")

col1, col2 = st.columns(2)

with col1:
    B_ini = st.number_input("B inicial (m)", value=0.8)

with col2:
    B_fin = st.number_input("B final (m)", value=3.0)

dB = st.number_input("Incremento ΔB (m)", value=0.5)

st.markdown("### 🔹 Profundidad de desplante (Df)")

col3, col4 = st.columns(2)

with col3:
    Df_ini = st.number_input("Df inicial (m)", value=0.8)

with col4:
    Df_fin = st.number_input("Df final (m)", value=3.0)

dDf = st.number_input("Incremento ΔDf (m)", value=0.5)

# =========================
# 🔹 ZAPATA
# =========================
st.subheader("3. Tipo de zapata")

tipo = st.selectbox("Seleccione la geometría", [
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
if k == 1:  # CUADRADA
    metodo = st.selectbox("Método de cálculo", ["Terzaghi", "General"])
else:
    metodo = "General"
    st.info("ECUACION GENERAL DE CAPACIDAD PORTANTE")

# =========================
# 🔹 NIVEL FREÁTICO
# =========================
st.subheader("4. Nivel freático")

nf = st.radio("¿Existe nivel freático?", ["NO", "SI"])

gamma_w = 0.0
prof_nf = 0.0

if nf == "SI":
    gamma_w = st.number_input("γ agua (t/m³)", value=1.0)
    prof_nf = st.number_input("Profundidad NF desde superficie (m)", value=4.8)

# =========================
# 🔹 FACTOR SEGURIDAD
# =========================
FS = st.number_input("Factor de seguridad", value=3.0)

# =========================
# 🔹 PERFIL
# =========================
st.subheader("🧱 Perfil estratigráfico")

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Estrato": [1, 2, 3, 4],
        "Espesor (m)": [0.8, 1.0, 1.5, 4.0],
        "φ (°)": [29, 30, 31, 32],
        "c (t/m²)": [0.0, 0.5, 1.0, 1.5],
        "γ (t/m³)": [1.6, 1.5, 1.6, 1.7],
        "γsat (t/m³)": [None, None, None, 2.1]
    })

st.session_state.df = st.data_editor(st.session_state.df, num_rows="dynamic")

df = st.session_state.df.copy()
df = df.sort_values("Estrato").reset_index(drop=True)
df["Espesor acum. (m)"] = df["Espesor (m)"].cumsum()

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

    qult = 1.3*c*Nc + q*Nq + 0.4*gamma*B*Ngamma
    qadm = qult / FS

    return {
        "phi": phi,
        "c": c,
        "gamma": gamma,
        "q": q,
        "qult": qult,
        "qadm": qadm,
        "caso": caso
    }

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
    # 🔥 ECUACIÓN GENERAL COMPLETA
    # =========================
    qult = (
        c * Nc * Fcs * Fcd * Fci +
        q * Nq * Fqs * Fqd * Fqi +
        0.5 * gamma * B * Ngamma * Fgs * Fgd * Fgi
    )

    qadm = qult / FS

    return {
        "phi": phi,
        "c": c,
        "gamma": gamma,
        "q": q,
        "qult": qult,
        "qadm": qadm,
        "caso": caso
    }
# =========================
# 🔹 CÁLCULO
# =========================

if st.button("🧱 Calcular capacidad portante"):

    resultados = []

    B_actual = B_ini

    while B_actual <= B_fin + 1e-6:

        Df_actual = Df_ini

        while Df_actual <= Df_fin + 1e-6:

            L = k * B_actual

            if metodo == "Terzaghi":
                res = terzaghi_cuadrada(
                    df, h, Df_actual, B_actual, FS,
                    nf, prof_nf, gamma_w
                )
            else:
                res = capacidad_general(
                    df, h, Df_actual, B_actual, L, FS,
                    nf, prof_nf, gamma_w, beta
                )

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

    df_res = pd.DataFrame(resultados)

    st.subheader("📊 Resultados")
    st.dataframe(df_res)

    tabla = df_res.pivot_table(
        index="B (m)",
        columns="Df (m)",
        values="q_adm"
    )

    st.line_chart(tabla)
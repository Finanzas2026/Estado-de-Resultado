import streamlit as st
import pandas as pd
import plotly.express as px

FILE_ID = st.secrets["FILE_ID"]
RUTA    = f"https://docs.google.com/spreadsheets/d/{FILE_ID}/export?format=xlsx"
HOJA    = "P&L-Presupuesto_2026-2028"

st.set_page_config(page_title="CDP – Estado de Resultados", layout="wide")

def check_password():
    import time
    SESSION_TIMEOUT = 8 * 3600
    now = time.time()
    auth_time = st.session_state.get("auth_time", 0)
    if st.session_state.get("authenticated") and (now - auth_time) < SESSION_TIMEOUT:
        return
    st.session_state.authenticated = False
    st.markdown("""
    <style>
    .auth-box { max-width:380px; margin:80px auto 0 auto; padding:36px 32px;
                background:#fff; border-radius:14px; box-shadow:0 4px 20px rgba(0,0,0,0.10); }
    </style>
    <div class="auth-box">
      <div style="font-size:22px;font-weight:900;color:#0052FF;margin-bottom:6px;">🔒 Acceso Restringido</div>
      <div style="font-size:13px;color:#888;margin-bottom:20px;">Ingresa la contraseña para continuar</div>
    </div>
    """, unsafe_allow_html=True)
    pwd = st.text_input("Contraseña", type="password", placeholder="Contraseña", label_visibility="collapsed")
    if st.button("Ingresar", use_container_width=True):
        if pwd == st.secrets["password"]:
            st.session_state.authenticated = True
            st.session_state.auth_time = time.time()
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
    st.stop()

check_password()

def check_password():
    import time
    SESSION_TIMEOUT = 8 * 3600  # 8 horas en segundos
    now = time.time()
    auth_time = st.session_state.get("auth_time", 0)
    if st.session_state.get("authenticated") and (now - auth_time) < SESSION_TIMEOUT:
        return
    st.session_state.authenticated = False
    st.markdown("""
    <style>
    .auth-box { max-width:380px; margin:80px auto 0 auto; padding:36px 32px;
                background:#fff; border-radius:14px; box-shadow:0 4px 20px rgba(0,0,0,0.10); }
    </style>
    <div class="auth-box">
      <div style="font-size:22px;font-weight:900;color:#0052FF;margin-bottom:6px;">🔒 Acceso Restringido</div>
      <div style="font-size:13px;color:#888;margin-bottom:20px;">Ingresa la contraseña para continuar</div>
    </div>
    """, unsafe_allow_html=True)
    pwd = st.text_input("Contraseña", type="password", placeholder="Contraseña", label_visibility="collapsed")
    if st.button("Ingresar", use_container_width=True):
        if pwd == st.secrets["password"]:
            st.session_state.authenticated = True
            st.session_state.auth_time = time.time()
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
    st.stop()

check_password()

st.markdown("""
<style>
.main .block-container {
    max-width: 1400px;
    padding-top: 2rem;
    box-sizing: border-box;
    overflow-x: auto;
}
section[data-testid="stSidebar"] { display: none; }
@media (max-width: 768px) {
    .main .block-container { padding: 1rem 0.5rem; overflow-x: auto; }
}
.kpi-card {
    background: #ffffff;
    border-radius: 10px;
    padding: 0 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.10);
    text-align: center;
    margin-bottom: 12px;
    height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-sizing: border-box;
}
.kpi-label { font-size: 14px; font-weight: 700; color: #666; text-transform: uppercase; letter-spacing: 0.5px; line-height: 1.3; word-break: break-word; }
.kpi-val   { font-size: 18px; font-weight: 900; color: #0052FF; margin: 5px 0 3px; }
.kpi-sub   { font-size: 11px; color: #888; }
.section-title {
    font-size: 26px; font-weight: 900; color: #0052FF;
    letter-spacing: 1.5px; text-transform: uppercase;
    margin: 24px 0 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<a href="https://cuadro--de-mando-financiero-kdeggfgf4ubpa958dwmktw.streamlit.app/" target="_top"
   style="display:inline-block;background:#0052FF;color:white;font-weight:700;font-size:15px;
          padding:12px 28px;border-radius:8px;text-decoration:none;
          box-shadow:0 2px 8px rgba(0,0,0,0.2);margin-bottom:20px;">
   ← Back
</a>
""", unsafe_allow_html=True)

# ── CARGAR DATOS ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def cargar():
    return pd.read_excel(RUTA, sheet_name=HOJA, header=None)

df = cargar()

def val(fila, col):
    try:
        return float(df.iloc[fila - 1, col])
    except:
        return None

def fmt(v, tipo="num"):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "—"
    if tipo == "pct":
        return f"{v*100:.1f}%"
    if v < 0:
        return f"(${abs(v):,.0f})"
    return f"${v:,.0f}"

# ── COLUMNAS ───────────────────────────────────────────────────────────────────
# col1=Descripción  col2=Ejecutado2025  col3=Presupuesto2025
# col5=Pres2026     col6=Pres2027       col7=Pres2028
EJ25, PR25, PR26, PR27, PR28, VAR, VAR_PCT = 2, 3, 5, 6, 7, 9, 10

# ── EXTRACCIÓN DE VALORES CLAVE ────────────────────────────────────────────────
data = {
    # Ingresos
    "ingresos_ej25":  val(8, EJ25),  "ingresos_pr26": val(8, PR26),
    "ingresos_pr27":  val(8, PR27),  "ingresos_pr28": val(8, PR28),
    # Utilidad Bruta
    "ut_bruta_ej25":  val(19, EJ25), "ut_bruta_pr26": val(19, PR26),
    "ut_bruta_pr27":  val(19, PR27), "ut_bruta_pr28": val(19, PR28),
    # Gastos Operativos
    "gastos_ej25":    val(78, EJ25), "gastos_pr26":   val(78, PR26),
    "gastos_pr27":    val(78, PR27), "gastos_pr28":   val(78, PR28),
    # EBITDA
    "ebitda_ej25":    val(81, EJ25), "ebitda_pr26":   val(81, PR26),
    "ebitda_pr27":    val(81, PR27), "ebitda_pr28":   val(81, PR28),
    # Utilidad Neta
    "ut_neta_ej25":   val(107, EJ25), "ut_neta_pr26": val(107, PR26),
    "ut_neta_pr27":   val(107, PR27), "ut_neta_pr28": val(107, PR28),
    # Administración
    "adm_ej25":       val(23, EJ25), "adm_pr26":      val(23, PR26),
    # Capital Humano
    "ch_ej25":        val(41, EJ25), "ch_pr26":       val(41, PR26),
    # Marketing
    "mkt_ej25":       val(57, EJ25), "mkt_pr26":      val(57, PR26),
    # Operativos
    "op_ej25":        val(60, EJ25), "op_pr26":       val(60, PR26),
}

# ── TÍTULO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#0052FF;padding:28px 36px;border-radius:10px;margin-bottom:24px;">
  <div style="color:white;font-size:34px;font-weight:900;letter-spacing:3px;">ESTADO DE RESULTADO - DASHBOARD</div>
  <div style="color:#D0E8FF;font-size:16px;font-weight:600;margin-top:6px;">Presupuesto 2026 · 2027 · 2028 vs Ejecutado 2025</div>
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Key Metrics — Presupuesto 2026</div>', unsafe_allow_html=True)

def kpi_card(label, val_main, label_sub, val_sub):
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-val">{fmt(val_main)}</div>
        <div class="kpi-sub">{label_sub}: {fmt(val_sub)}</div>
    </div>"""

kpis = [
    ("Ingresos",          data["ingresos_pr26"],  "Ej. 2025", data["ingresos_ej25"]),
    ("Utilidad Bruta",    data["ut_bruta_pr26"],  "Ej. 2025", data["ut_bruta_ej25"]),
    ("Gastos Operativos", data["gastos_pr26"],    "Ej. 2025", data["gastos_ej25"]),
    ("EBITDA",            data["ebitda_pr26"],    "Ej. 2025", data["ebitda_ej25"]),
    ("Utilidad Neta",     data["ut_neta_pr26"],   "Ej. 2025", data["ut_neta_ej25"]),
    ("Administración",    data["adm_pr26"],       "Ej. 2025", data["adm_ej25"]),
    ("Capital Humano",    data["ch_pr26"],        "Ej. 2025", data["ch_ej25"]),
    ("Marketing",         data["mkt_pr26"],       "Ej. 2025", data["mkt_ej25"]),
]

cols = st.columns(8)
for i, (label, v_main, lsub, v_sub) in enumerate(kpis):
    with cols[i]:
        st.markdown(kpi_card(label, v_main, lsub, v_sub), unsafe_allow_html=True)

# ── GRÁFICO: Comparativo por año ───────────────────────────────────────────────
st.markdown('<hr style="border:none;border-top:2px solid #e0e0e0;margin:24px 0;">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Comparativo por Año</div>', unsafe_allow_html=True)

metricas_graf = {
    "Ingresos":       [data["ingresos_ej25"],  data["ingresos_pr26"],  data["ingresos_pr27"],  data["ingresos_pr28"]],
    "Utilidad Bruta": [data["ut_bruta_ej25"],  data["ut_bruta_pr26"],  data["ut_bruta_pr27"],  data["ut_bruta_pr28"]],
    "EBITDA":         [data["ebitda_ej25"],     data["ebitda_pr26"],    data["ebitda_pr27"],    data["ebitda_pr28"]],
    "Utilidad Neta":  [data["ut_neta_ej25"],    data["ut_neta_pr26"],   data["ut_neta_pr27"],   data["ut_neta_pr28"]],
}
años = ["Ej. 2025", "Pres. 2026", "Pres. 2027", "Pres. 2028"]

metrica_sel = st.selectbox("Selecciona métrica:", list(metricas_graf.keys()))
df_graf = pd.DataFrame({"Año": años, "Valor": metricas_graf[metrica_sel]})
colores = ["#4C9BE8", "#0052FF", "#2ECC71", "#E8C34C"]
fig = px.bar(df_graf, x="Año", y="Valor", text="Valor", color="Año",
             color_discrete_sequence=colores)
fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", textfont=dict(size=13))
fig.update_layout(showlegend=False, plot_bgcolor="white", height=400,
                  yaxis=dict(tickformat=",.0f"), xaxis_title="", yaxis_title="")
st.plotly_chart(fig, use_container_width=True)

# ── TABLA P&L RESUMEN ──────────────────────────────────────────────────────────
st.markdown('<hr style="border:none;border-top:2px solid #e0e0e0;margin:24px 0;">', unsafe_allow_html=True)
st.markdown('<div class="section-title" style="text-align:center;">Estado de Resultados — Resumen</div>', unsafe_allow_html=True)

FILAS_PL = [
    (8,   "Ingresos",                      True),
    (19,  "Utilidad Bruta",                True),
    (23,  "Administración",                False),
    (41,  "Capital Humano",                False),
    (57,  "Marketing",                     False),
    (60,  "Operativos",                    False),
    (78,  "Gastos Operativos",             True),
    (81,  "Utilidad Operativa (EBITDA)",   True),
    (83,  "Depreciación",                  False),
    (86,  "Utilidad Operativa (EBIT)",     True),
    (88,  "Otros Ingresos",               False),
    (93,  "Otros Egresos",                False),
    (99,  "Gastos Financieros",           False),
    (103, "Utilidad Antes de Impuestos",   True),
    (105, "Impuestos (ISR)",              False),
    (107, "Utilidad Neta",                True),
]

header = (
    '<div style="display:grid;grid-template-columns:2.2fr 1fr 1fr 1fr 1fr 1fr 0.8fr;'
    'padding:10px 16px;background:#0052FF;border-radius:10px 10px 0 0;">'
    '<span style="color:white;font-weight:700;font-size:15px;">Descripción</span>'
    '<span style="color:white;font-weight:700;text-align:right;font-size:15px;">Ej. 2025</span>'
    '<span style="color:white;font-weight:700;text-align:right;font-size:15px;">Pres. 2026</span>'
    '<span style="color:white;font-weight:700;text-align:right;font-size:15px;">Pres. 2027</span>'
    '<span style="color:white;font-weight:700;text-align:right;font-size:15px;">Pres. 2028</span>'
    '<span style="color:white;font-weight:700;text-align:right;font-size:15px;">Var. ($)</span>'
    '<span style="color:white;font-weight:700;text-align:right;font-size:15px;">Var. %</span>'
    '</div>'
)

rows_html = ""
for i, (fila, nombre, es_total) in enumerate(FILAS_PL):
    v_ej25  = val(fila, EJ25)
    v_pr26  = val(fila, PR26)
    v_pr27  = val(fila, PR27)
    v_pr28  = val(fila, PR28)
    v_var   = val(fila, VAR)
    v_pct   = val(fila, VAR_PCT)
    if es_total:
        bg, fw = "#d0e8ff", "bold"
    else:
        bg, fw = ("#f9f9f9" if i % 2 == 0 else "#ffffff"), "normal"
    # Filas de ingreso/utilidad tienen lógica invertida
    FILAS_INGRESO = {8, 19, 81, 86, 88, 103, 107}
    ej25_abs = abs(v_ej25 or 0)
    pr26_abs = abs(v_pr26 or 0)
    if fila in FILAS_INGRESO:
        var_bg = "#1e8449" if ej25_abs > pr26_abs else "#c0392b"
    else:
        var_bg = "#c0392b" if ej25_abs > pr26_abs else "#1e8449"
    pct_txt = f"{v_pct*100:.1f}%" if v_pct is not None and not pd.isna(v_pct) else "—"
    rows_html += (
        f'<div style="display:grid;grid-template-columns:2.2fr 1fr 1fr 1fr 1fr 1fr 0.8fr;'
        f'padding:9px 16px;background:{bg};border-bottom:1px solid #eee;">'
        f'<span style="font-weight:{fw};color:#333;font-size:15px;">{nombre}</span>'
        f'<span style="text-align:right;font-weight:{fw};color:#555;font-size:15px;">{fmt(v_ej25)}</span>'
        f'<span style="text-align:right;font-weight:{fw};color:#0052FF;font-size:15px;">{fmt(v_pr26)}</span>'
        f'<span style="text-align:right;font-weight:{fw};color:#0052FF;font-size:15px;">{fmt(v_pr27)}</span>'
        f'<span style="text-align:right;font-weight:{fw};color:#0052FF;font-size:15px;">{fmt(v_pr28)}</span>'
        f'<span style="text-align:right;font-weight:bold;color:{var_bg};font-size:15px;">{fmt(v_var)}</span>'
        f'<span style="text-align:right;font-weight:bold;color:{var_bg};font-size:15px;">{pct_txt}</span>'
        f'</div>'
    )

st.markdown(
    f'<div style="max-width:1100px;margin:0 auto;">'
    f'<div style="background:#fff;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.1);overflow:hidden;">'
    f'{header}{rows_html}</div></div>',
    unsafe_allow_html=True
)

# ── GASTOS OPERATIVOS DETALLE ──────────────────────────────────────────────────
st.markdown('<hr style="border:none;border-top:2px solid #e0e0e0;margin:24px 0;">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Gastos Operativos — Detalle por Categoría</div>', unsafe_allow_html=True)

categorias = {
    "Administración":  (23,  41,  "#0052FF"),
    "Capital Humano":  (41,  57,  "#4C9BE8"),
    "Marketing":       (57,  60,  "#2ECC71"),
    "Operativos":      (60,  78,  "#E8C34C"),
}

EXCLUIR = {"Administración", "Capital Humano", "Marketing", "Operativos",
           "Gastos Operativos", "nan", "None", "—"}

col_izq, col_der = st.columns([1, 1])

cat_sel = col_izq.selectbox("Categoría:", list(categorias.keys()))
fila_ini, fila_fin, color_cat = categorias[cat_sel]

detalle_rows = ""
for f in range(fila_ini, fila_fin):
    nombre = str(df.iloc[f - 1, 1]) if not pd.isna(df.iloc[f - 1, 1]) else ""
    if nombre in EXCLUIR or nombre.strip() == "":
        continue
    v_ej = val(f, EJ25)
    v_26 = val(f, PR26)
    if v_ej is None and v_26 is None:
        continue
    detalle_rows += (
        f'<div style="display:flex;justify-content:space-between;gap:12px;'
        f'padding:8px 16px;border-bottom:1px solid #eee;font-size:15px;">'
        f'<span style="color:#333;flex:2;">{nombre[:40]}</span>'
        f'<span style="text-align:right;flex:1;color:#555;">{fmt(v_ej)}</span>'
        f'<span style="text-align:right;flex:1;color:#0052FF;font-weight:600;">{fmt(v_26)}</span>'
        f'</div>'
    )

col_izq.markdown(
    f'<div style="background:#fff;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.1);overflow:hidden;">'
    f'<div style="background:{color_cat};padding:10px 16px;font-weight:700;color:white;font-size:14px;">'
    f'{cat_sel} — Ej. 2025 vs Pres. 2026</div>'
    f'<div style="display:flex;justify-content:space-between;gap:12px;padding:8px 16px;'
    f'background:#f0f0f0;font-size:12px;font-weight:700;color:#666;">'
    f'<span style="flex:2;">Concepto</span>'
    f'<span style="flex:1;text-align:right;">Ej. 2025</span>'
    f'<span style="flex:1;text-align:right;">Pres. 2026</span></div>'
    f'{detalle_rows}</div>',
    unsafe_allow_html=True
)

# Pie chart de distribución
cat_vals = {k: abs(val(v[0], PR26) or 0) for k, v in categorias.items()}
df_pie = pd.DataFrame({"Categoría": list(cat_vals.keys()), "Valor": list(cat_vals.values())})
df_pie = df_pie[df_pie["Valor"] > 0]
fig_pie = px.pie(df_pie, names="Categoría", values="Valor",
                 color_discrete_sequence=["#0052FF", "#4C9BE8", "#2ECC71", "#E8C34C"])
fig_pie.update_traces(textinfo="label+percent", textposition="outside", textfont=dict(size=13))
fig_pie.update_layout(height=380, showlegend=False, margin=dict(t=20, b=20, l=20, r=20),
                      title=dict(text="Distribución Gastos Operativos 2026", x=0.5, font=dict(size=14)))
col_der.plotly_chart(fig_pie, use_container_width=True)

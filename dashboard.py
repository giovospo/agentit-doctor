import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="AgentIT Doctor",
    page_icon="🩺",
    layout="wide"
)

# ==========================
# Cargar historial
# ==========================

history_files = sorted(
    Path("history").glob("*.json"),
    reverse=True
)

st.sidebar.title("📁 Historial")

selected_file = None

if history_files:

    selected_file = st.sidebar.selectbox(
        "Selecciona un diagnóstico",
        history_files,
        format_func=lambda x: x.name
    )

# ==========================
# Cargar diagnóstico
# ==========================

if selected_file:

    with open(
        selected_file,
        encoding="utf-8"
    ) as file:

        diagnosis = json.load(file)

else:

    with open(
        "output/diagnosis.json",
        encoding="utf-8"
    ) as file:

        diagnosis = json.load(file)

# ==========================
# Encabezado
# ==========================

st.title("🩺 AgentIT Doctor")

# ==========================
# KPIs
# ==========================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Hallazgos",
    len(diagnosis["findings"])
)

col2.metric(
    "Causas raíz",
    len(diagnosis["root_causes"])
)

col3.metric(
    "Severidad",
    diagnosis["severity"]
)

# ==========================
# Severidad
# ==========================

st.subheader("Severidad")

severity = diagnosis["severity"]

if severity == "Critical":

    st.error("🔴 Crítica")

elif severity == "High":

    st.warning("🟠 Alta")

else:

    st.success("🟢 Normal")

# ==========================
# Hallazgos
# ==========================

st.subheader("Hallazgos")

st.write(
    diagnosis["findings"]
)

# ==========================
# Causas raíz
# ==========================

st.subheader("Causas Raíz")

causes_df = pd.DataFrame(
    diagnosis["root_causes"]
)

st.dataframe(
    causes_df
)

# ==========================
# Gráfico
# ==========================

if not causes_df.empty:

    fig = px.bar(
        causes_df,
        x="component",
        y="probability",
        title="Probabilidad de Causa Raíz",
        color="probability",
        text="probability"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
# ==========================
# Carga manual de logs
# ==========================

st.subheader("📂 Carga Manual de Logs")

uploaded_file = st.file_uploader(
    "Selecciona un archivo",
    type=["txt", "log"]
)

if uploaded_file:

    content = uploaded_file.read()

    text = content.decode(
        "utf-8",
        errors="ignore"
    )

    st.subheader(
        "Contenido del Log"
    )

    st.text(text)

    findings = []

    log_text = text.lower()

    if "kernel-power" in log_text:
        findings.append("KERNEL_POWER")

    if "bugcheck" in log_text:
        findings.append("BUGCHECK")

    if "driver_irql_not_less_or_equal" in log_text:
        findings.append("IRQL_ERROR")

    if "tcpip.sys" in log_text:
        findings.append("TCPIP_DRIVER")

    if "whea" in log_text:
        findings.append("WHEA")

    st.subheader(
        "Hallazgos Detectados"
    )

    st.write(findings)

    risk_score = len(findings) * 20

    st.metric(
        "Risk Score",
        risk_score
    )

    if risk_score >= 80:

        st.error(
            "🔴 Riesgo Alto"
        )

    elif risk_score >= 40:

        st.warning(
            "🟠 Riesgo Medio"
        )

    else:

        st.success(
            "🟢 Riesgo Bajo"
        )

# ==========================
# Descargar diagnóstico
# ==========================

st.download_button(
    "📥 Descargar Diagnóstico",
    data=json.dumps(
        diagnosis,
        indent=4,
        ensure_ascii=False
    ),
    file_name="diagnostico.json",
    mime="application/json"
)
# =====
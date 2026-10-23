import json
from pathlib import Path
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from agents.network_agent import NetworkAgent
from agents.rca_agent import RCAAgent

# ==================================================
# CONFIGURACIÓN
# ==================================================

st.set_page_config(
    page_title="AgentIT Doctor",
    page_icon="🩺",
    layout="wide"
)

# ==================================================
# CARPETAS
# ==================================================

history_folder = Path("history")
history_folder.mkdir(exist_ok=True)

output_file = Path("output/diagnosis.json")

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("📁 Historial")

history_files = sorted(
    history_folder.glob("*.json"),
    reverse=True
)

history_limit = st.sidebar.selectbox(
    "Mostrar",
    [5, 10, 20, "Todos"]
)

if history_limit != "Todos":
    history_files = history_files[:history_limit]

if st.sidebar.button("🗑️ Limpiar historial"):

    for file in history_folder.glob("*.json"):
        file.unlink()

    st.success("Historial eliminado.")
    st.rerun()

selected_file = None

if history_files:

    selected_file = st.sidebar.selectbox(
        "Selecciona un diagnóstico",
        history_files,
        format_func=lambda x: x.name
    )

# ==================================================
# CARGAR DIAGNÓSTICO
# ==================================================

diagnosis = {
    "generated_by": "AgentIT Doctor",
    "version": "0.6.0",
    "severity": "Normal",
    "findings": [],
    "root_causes": []
}

try:

    if selected_file:

        with open(
            selected_file,
            encoding="utf-8"
        ) as file:

            diagnosis = json.load(file)

    elif output_file.exists():

        with open(
            output_file,
            encoding="utf-8"
        ) as file:

            diagnosis = json.load(file)

except Exception as error:

    st.error(
        f"Error cargando diagnóstico: {error}"
    )

# ==================================================
# ENCABEZADO
# ==================================================

st.title("🩺 AgentIT Doctor")

st.caption(
    "Detección de incidentes Windows y análisis de causa raíz (RCA)"
)

if st.button("🔄 Actualizar historial"):
    st.rerun()

# ==================================================
# KPIS
# ==================================================

col1, col2, col3, col4 = st.columns(4)

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

max_probability = max(
    [x["probability"] for x in diagnosis["root_causes"]],
    default=0
)

col4.metric(
    "Probabilidad Máx.",
    f"{max_probability}%"
)

# ==================================================
# SEVERIDAD
# ==================================================

st.subheader("Severidad")

severity = diagnosis["severity"]

if severity == "Critical":

    st.error("🔴 Critical")

elif severity == "High":

    st.warning("🟠 High")

else:

    st.success("🟢 Normal")

# ==================================================
# HALLAZGOS
# ==================================================

st.subheader("Hallazgos")

if diagnosis["findings"]:

    st.write(
        diagnosis["findings"]
    )

else:

    st.info(
        "No existen hallazgos."
    )

# ==================================================
# RCA
# ==================================================

st.subheader("Causas Raíz")

causes_df = pd.DataFrame(
    diagnosis["root_causes"]
)

if not causes_df.empty:

    st.dataframe(
        causes_df,
        use_container_width=True
    )

    fig = px.bar(
        causes_df,
        x="component",
        y="probability",
        color="probability",
        text="probability",
        title="Probabilidad de causa raíz"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No hay causas raíz calculadas."
    )

# ==================================================
# TENDENCIA HISTÓRICA
# ==================================================

st.subheader("📈 Tendencias Históricas")

trend_files = list(
    history_folder.glob("*.json")
)

if trend_files:

    trend_df = pd.DataFrame(
        {
            "Diagnóstico": [
                x.stem
                for x in trend_files
            ]
        }
    )

    trend_df["Cantidad"] = 1

    trend_chart = px.line(
        trend_df,
        y="Cantidad",
        title="Cantidad de diagnósticos almacenados"
    )

    st.plotly_chart(
        trend_chart,
        use_container_width=True
    )

# ==================================================
# CARGA DE LOGS
# ==================================================

st.subheader("📂 Carga Manual de Logs")

uploaded_file = st.file_uploader(
    "Selecciona un archivo",
    type=["txt", "log"]
)

if uploaded_file:

    text = uploaded_file.read().decode(
        "utf-8",
        errors="ignore"
    )

    st.subheader(
        "Contenido del Log"
    )

    st.text_area(
        "Contenido",
        text,
        height=250
    )

    # ==========================================
    # ANALISIS AUTOMATICO
    # ==========================================

    network_agent = NetworkAgent()

    findings = network_agent.analyze(
        text
    )

    rca_agent = RCAAgent()

    root_causes = rca_agent.determine(
        findings
    )

    diagnosis_from_log = {
        "generated_by": "AgentIT Doctor",
        "version": "0.6.0",
        "severity": "Critical",
        "findings": findings,
        "root_causes": root_causes
    }

    st.subheader(
        "Hallazgos Detectados"
    )

    st.write(findings)

    st.subheader(
        "RCA Automático"
    )

    st.write(root_causes)

    # ==========================================
    # RISK SCORE
    # ==========================================

    risk_score = len(findings) * 20

    st.metric(
        "Risk Score",
        risk_score
    )

    if risk_score >= 80:

        st.error("🔴 Riesgo Alto")

    elif risk_score >= 40:

        st.warning("🟠 Riesgo Medio")

    else:

        st.success("🟢 Riesgo Bajo")

    # ==========================================
    # GUARDAR HISTORIAL
    # ==========================================

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    history_file = (
        history_folder /
        f"{timestamp}.json"
    )

    if not history_file.exists():

        with open(
            history_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                diagnosis_from_log,
                file,
                indent=4,
                ensure_ascii=False
            )

        st.success(
            f"✅ Diagnóstico guardado: {history_file.name}"
        )

# ==================================================
# DESCARGA
# ==================================================

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

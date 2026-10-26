import sqlite3
from io import BytesIO

import pandas as pd
import plotly.express as px
import streamlit as st

from pdf_export import generate_pdf

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AgentIT Doctor Dashboard",
    page_icon="🩺",
    layout="wide"
)

# ==========================================
# DATABASE
# ==========================================

try:

    conn = sqlite3.connect(
        "storage/diagnostics.db"
    )

    incidents = pd.read_sql_query(
        "SELECT * FROM incidents",
        conn
    )

    events = pd.read_sql_query(
        "SELECT * FROM events",
        conn
    )

    analyses = pd.read_sql_query(
        "SELECT * FROM analyses",
        conn
    )

except Exception as ex:

    st.error(
        f"Database error: {ex}"
    )

    st.stop()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🔧 Filters")

search_incident = st.sidebar.text_input(
    "Search Incident ID"
)

severity_options = []

if (
    not incidents.empty
    and "severity" in incidents.columns
):

    severity_options = sorted(
        incidents["severity"]
        .dropna()
        .unique()
    )

selected_severity = st.sidebar.multiselect(
    "Severity",
    severity_options,
    default=severity_options
)

service_options = []

if (
    not events.empty
    and "source" in events.columns
):

    service_options = sorted(
        events["source"]
        .dropna()
        .unique()
    )

selected_services = st.sidebar.multiselect(
    "Service/Event",
    service_options,
    default=service_options
)

# ==========================================
# FILTER INCIDENTS
# ==========================================

filtered_incidents = incidents.copy()

if (
    "severity" in filtered_incidents.columns
    and selected_severity
):

    filtered_incidents = (
        filtered_incidents[
            filtered_incidents["severity"]
            .isin(selected_severity)
        ]
    )

if (
    search_incident
    and "id" in filtered_incidents.columns
):

    filtered_incidents = (
        filtered_incidents[
            filtered_incidents["id"]
            .astype(str)
            .str.contains(
                search_incident,
                case=False,
                na=False
            )
        ]
    )

# ==========================================
# FILTER EVENTS
# ==========================================

filtered_events = events.copy()

if (
    "source" in filtered_events.columns
    and selected_services
):

    filtered_events = (
        filtered_events[
            filtered_events["source"]
            .isin(selected_services)
        ]
    )

if (
    not filtered_incidents.empty
    and "incident_id" in filtered_events.columns
):

    filtered_events = (
        filtered_events[
            filtered_events["incident_id"]
            .isin(
                filtered_incidents["id"]
            )
        ]
    )

# ==========================================
# FILTER ANALYSES
# ==========================================

filtered_analyses = analyses.copy()

if (
    not filtered_incidents.empty
    and "incident_id" in filtered_analyses.columns
):

    filtered_analyses = (
        filtered_analyses[
            filtered_analyses["incident_id"]
            .isin(
                filtered_incidents["id"]
            )
        ]
    )

# ==========================================
# HEADER
# ==========================================

st.title(
    "🩺 AgentIT Doctor Dashboard"
)

st.caption(
    "v0.9 Alpha - RCA Engine Enabled"
)

# ==========================================
# KPIs
# ==========================================

k1, k2, k3 = st.columns(3)

k1.metric(
    "Incidents",
    len(filtered_incidents)
)

k2.metric(
    "Events",
    len(filtered_events)
)

k3.metric(
    "Root Causes",
    len(filtered_analyses)
)

st.divider()

# ==========================================
# INCIDENT DETAIL
# ==========================================

if (
    not filtered_incidents.empty
    and "id" in filtered_incidents.columns
):

    incident_options = sorted(
        filtered_incidents["id"]
        .astype(str)
        .unique()
    )

    selected_incident = st.selectbox(
        "🔎 Incident Detail",
        [""] + incident_options
    )

    if selected_incident:

        st.subheader(
            "Incident Information"
        )

        st.dataframe(
            filtered_incidents[
                filtered_incidents["id"]
                == selected_incident
            ],
            width="stretch"
        )

# ==========================================
# INCIDENTS BY DAY
# ==========================================

st.subheader(
    "📈 Incidents by Day"
)

if (
    not filtered_incidents.empty
    and "created_at" in filtered_incidents.columns
):

    incidents_by_day = (
        filtered_incidents
        .assign(
            created_day=lambda df:
            pd.to_datetime(
                df["created_at"]
            ).dt.date
        )
        .groupby("created_day")
        .size()
        .reset_index(name="count")
    )

    fig_day = px.area(
        incidents_by_day,
        x="created_day",
        y="count",
        title="Incidents by Day"
    )

    fig_day.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_day,
        width="stretch"
    )

# ==========================================
# SEVERITY
# ==========================================

st.subheader(
    "🚨 Severity Distribution"
)

if (
    not filtered_incidents.empty
    and "severity" in filtered_incidents.columns
):

    severity_chart = (
        filtered_incidents
        .groupby("severity")
        .size()
        .reset_index(name="count")
    )

    fig = px.bar(
        severity_chart,
        x="severity",
        y="count",
        color="severity"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# ==========================================
# ROOT CAUSES
# ==========================================

st.subheader(
    "🔍 Top Root Causes"
)

if (
    not filtered_analyses.empty
    and "root_cause" in filtered_analyses.columns
):

    causes = (
        filtered_analyses
        .groupby("root_cause")
        .size()
        .reset_index(name="count")
        .sort_values(
            "count",
            ascending=False
        )
        .head(10)
    )

    fig_causes = px.bar(
        causes,
        x="root_cause",
        y="count",
        color="count"
    )

    st.plotly_chart(
        fig_causes,
        width="stretch"
    )

# ==========================================
# RCA FINDINGS
# ==========================================

st.subheader(
    "🤖 RCA Findings"
)

if not filtered_analyses.empty:

    cols = [
        c
        for c in [
            "incident_id",
            "root_cause",
            "confidence",
            "recommendation"
        ]
        if c in filtered_analyses.columns
    ]

    if cols:

        st.dataframe(
            filtered_analyses[cols],
            width="stretch"
        )

# ==========================================
# TCP/IP
# ==========================================

st.subheader(
    "🌐 Top TCP/IP Events"
)

if (
    not filtered_events.empty
    and "source" in filtered_events.columns
):

    tcp_events = filtered_events[
        filtered_events["source"]
        .astype(str)
        .str.contains(
            "TCP",
            case=False,
            na=False
        )
    ]

    if not tcp_events.empty:

        tcp_chart = (
            tcp_events
            .groupby("source")
            .size()
            .reset_index(name="count")
        )

        fig_tcp = px.bar(
            tcp_chart,
            x="source",
            y="count",
            color="count"
        )

        st.plotly_chart(
            fig_tcp,
            width="stretch"
        )

# ==========================================
# EXPORTS
# ==========================================

st.subheader(
    "📤 Export Data"
)

c1, c2, c3 = st.columns(3)

csv_data = (
    filtered_incidents
    .to_csv(index=False)
    .encode("utf-8")
)

with c1:

    st.download_button(
        "⬇ Download CSV",
        csv_data,
        "incidents.csv",
        "text/csv"
    )

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    filtered_incidents.to_excel(
        writer,
        sheet_name="Incidents",
        index=False
    )

with c2:

    st.download_button(
        "⬇ Download Excel",
        excel_buffer.getvalue(),
        "incidents.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

pdf_buffer = generate_pdf(
    incidents_count=len(filtered_incidents),
    events_count=len(filtered_events),
    root_causes_count=len(filtered_analyses)
)

with c3:

    st.download_button(
        "⬇ Download PDF",
        data=pdf_buffer,
        file_name="agentit_report.pdf",
        mime="application/pdf"
    )

# ==========================================
# TABLES
# ==========================================

st.subheader("📋 Incidents")
st.dataframe(
    filtered_incidents,
    width="stretch"
)

st.subheader("🌐 Events")
st.dataframe(
    filtered_events,
    width="stretch"
)

st.subheader("🔍 Analyses")
st.dataframe(
    filtered_analyses,
    width="stretch"
)

conn.close()
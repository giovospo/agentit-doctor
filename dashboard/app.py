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
# FILTERING
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

# ==========================================
# HEADER
# ==========================================

st.title(
    "🩺 AgentIT Doctor Dashboard"
)

st.caption(
    "SQLite Storage Layer v0.8 Final"
)

# ==========================================
# KPIs
# ==========================================

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    "Incidents",
    len(filtered_incidents)
)

kpi2.metric(
    "Events",
    len(filtered_events)
)

kpi3.metric(
    "Root Causes",
    len(analyses)
)

st.divider()

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

    fig_day = px.line(
        incidents_by_day,
        x="created_day",
        y="count",
        markers=True,
        title="Incidents by Day"
    )

    st.plotly_chart(
        fig_day,
        use_container_width=True
    )

# ==========================================
# SEVERITY DISTRIBUTION
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
        color="severity",
        title="Severity Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# TOP ROOT CAUSES
# ==========================================

st.subheader(
    "🔍 Top Root Causes"
)

if (
    not analyses.empty
    and "root_cause" in analyses.columns
):

    causes = (
        analyses
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
        color="count",
        title="Top Root Causes"
    )

    st.plotly_chart(
        fig_causes,
        use_container_width=True
    )

# ==========================================
# TCP/IP EVENTS
# ==========================================

st.subheader(
    "🌐 Top TCP/IP Events"
)

if (
    not events.empty
    and "source" in events.columns
):

    tcp_events = events[
        events["source"]
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
            .sort_values(
                "count",
                ascending=False
            )
        )

        fig_tcp = px.bar(
            tcp_chart,
            x="source",
            y="count",
            color="count",
            title="Top TCP/IP Events"
        )

        st.plotly_chart(
            fig_tcp,
            use_container_width=True
        )

# ==========================================
# EXPORTS
# ==========================================

st.subheader(
    "📤 Export Data"
)

col_csv, col_excel, col_pdf = st.columns(3)

# CSV

csv_data = (
    filtered_incidents
    .to_csv(index=False)
    .encode("utf-8")
)

with col_csv:

    st.download_button(
        "⬇ Download CSV",
        csv_data,
        "incidents.csv",
        "text/csv"
    )

# Excel

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

with col_excel:

    st.download_button(
        "⬇ Download Excel",
        excel_buffer.getvalue(),
        "incidents.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# PDF

pdf_buffer = generate_pdf(
    incidents_count=len(filtered_incidents),
    events_count=len(filtered_events),
    root_causes_count=len(analyses)
)

with col_pdf:

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
    use_container_width=True
)

st.subheader("🌐 Events")

st.dataframe(
    filtered_events,
    use_container_width=True
)

st.subheader("🔍 Root Causes")

st.dataframe(
    analyses,
    use_container_width=True
)

conn.close()
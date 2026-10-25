import sqlite3

import pandas as pd
import streamlit as st

# ==================================
# CONFIG
# ==================================

st.set_page_config(
    page_title="AgentIT Doctor",
    page_icon="🩺",
    layout="wide"
)

# ==================================
# DATABASE
# ==================================

conn = sqlite3.connect(
    "storage/diagnostics.db"
)

incidents = pd.read_sql_query(
    """
    SELECT *
    FROM incidents
    """,
    conn
)

events = pd.read_sql_query(
    """
    SELECT *
    FROM events
    """,
    conn
)

analyses = pd.read_sql_query(
    """
    SELECT *
    FROM analyses
    """,
    conn
)

# ==================================
# SIDEBAR
# ==================================

st.sidebar.title("Filtros")

severity_options = sorted(
    incidents["severity"].dropna().unique()
)

selected_severity = st.sidebar.multiselect(
    "Severidad",
    severity_options,
    default=severity_options
)

filtered_incidents = incidents[
    incidents["severity"].isin(
        selected_severity
    )
]

service_options = sorted(
    events["source"].dropna().unique()
)

selected_services = st.sidebar.multiselect(
    "Servicio / Evento",
    service_options,
    default=service_options
)

filtered_events = events[
    events["source"].isin(
        selected_services
    )
]

# ==================================
# TITLE
# ==================================

st.title(
    "🩺 AgentIT Doctor Dashboard"
)

st.caption(
    "SQLite Storage Layer v0.8"
)

# ==================================
# KPIs
# ==================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Incidents",
    len(filtered_incidents)
)

col2.metric(
    "Events",
    len(filtered_events)
)

col3.metric(
    "Root Causes",
    len(analyses)
)

st.divider()

# ==================================
# INCIDENTS BY DAY
# ==================================

st.subheader(
    "📈 Incidents by Day"
)

if len(filtered_incidents) > 0:

    incidents_chart = (
        filtered_incidents
        .assign(
            created_day=lambda x:
            pd.to_datetime(
                x["created_at"]
            ).dt.date
        )
        .groupby(
            "created_day"
        )
        .size()
        .reset_index(
            name="count"
        )
    )

    st.line_chart(
        incidents_chart.set_index(
            "created_day"
        )
    )

# ==================================
# SEVERITY CHART
# ==================================

st.subheader(
    "🚨 Severity Distribution"
)

severity_chart = (
    filtered_incidents
    .groupby(
        "severity"
    )
    .size()
    .reset_index(
        name="count"
    )
)

if not severity_chart.empty:

    st.bar_chart(
        severity_chart.set_index(
            "severity"
        )
    )

# ==================================
# INCIDENTS
# ==================================

st.subheader(
    "📋 Incidents"
)

st.dataframe(
    filtered_incidents,
   width="stretch"
)

# ==================================
# EVENTS
# ==================================

st.subheader(
    "🌐 Events"
)

st.dataframe(
    filtered_events,
    width="stretch"
)

# ==================================
# ROOT CAUSES
# ==================================

st.subheader(
    "🔍 Root Causes"
)

st.dataframe(
    analyses,
    width="stretch"
)

conn.close()
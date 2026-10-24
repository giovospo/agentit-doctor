import sqlite3
from io import BytesIO

import pandas as pd
import plotly.express as px
import streamlit as st

from pdf_export import generate_pdf


# ==========================================
# HELPERS
# ==========================================

def has_columns(df, columns):
    return all(column in df.columns for column in columns)


def safe_dataframe(df):
    if df is None:
        return pd.DataFrame()

    return df


def configure_plotly(fig):
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        height=450
    )

    return fig


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

    evidence = pd.read_sql_query(
        "SELECT * FROM evidence",
        conn
    )

    incidents = safe_dataframe(
        incidents
    )

    events = safe_dataframe(
        events
    )

    analyses = safe_dataframe(
        analyses
    )

    evidence = safe_dataframe(
        evidence
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
    and has_columns(
        incidents,
        ["severity"]
    )
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
    and has_columns(
        events,
        ["source"]
    )
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
    has_columns(
        filtered_incidents,
        ["severity"]
    )
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
    and has_columns(
        filtered_incidents,
        ["id"]
    )
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
    has_columns(
        filtered_events,
        ["source"]
    )
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
    and has_columns(
        filtered_events,
        ["incident_id"]
    )
    and has_columns(
        filtered_incidents,
        ["id"]
    )
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

evidence_summary = pd.DataFrame()

if (
    not evidence.empty
    and has_columns(
        evidence,
        [
            "incident_id",
            "root_cause",
            "evidence"
        ]
    )
):

    evidence_summary = (
        evidence
        .groupby(
            [
                "incident_id",
                "root_cause"
            ]
        )["evidence"]
        .apply(
            lambda x: ", ".join(
                x.astype(str)
            )
        )
        .reset_index()
    )

if (
    not filtered_incidents.empty
    and has_columns(
        filtered_analyses,
        ["incident_id"]
    )
    and has_columns(
        filtered_incidents,
        ["id"]
    )
):

    filtered_analyses = (
        filtered_analyses[
            filtered_analyses["incident_id"]
            .isin(
                filtered_incidents["id"]
            )
        ]
    )

if (
    not filtered_analyses.empty
    and has_columns(
        filtered_analyses,
        ["confidence"]
    )
):

    filtered_analyses = (
        filtered_analyses
        .sort_values(
            "confidence",
            ascending=False
        )
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
# KPI
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
    (
        filtered_analyses["root_cause"].count()
        if has_columns(
            filtered_analyses,
            ["root_cause"]
        )
        else 0
    )
)

st.divider()

# ==========================================
# INCIDENT DETAIL
# ==========================================

if (
    not filtered_incidents.empty
    and has_columns(
        filtered_incidents,
        ["id"]
    )
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

        incident_detail = (
            filtered_incidents[
                filtered_incidents["id"]
                == selected_incident
            ]
        )

        if not incident_detail.empty:

            st.json(
                incident_detail
                .to_dict(
                    orient="records"
                )[0]
            )

# ==========================================
# INCIDENTS BY DAY
# ==========================================

st.subheader(
    "📈 Incidents by Day"
)

if (
    not filtered_incidents.empty
    and has_columns(
        filtered_incidents,
        ["created_at"]
    )
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

    st.plotly_chart(
        configure_plotly(fig_day),
        use_container_width=True
    )

# ==========================================
# SEVERITY
# ==========================================

st.subheader(
    "🚨 Severity Distribution"
)

if (
    not filtered_incidents.empty
    and has_columns(
        filtered_incidents,
        ["severity"]
    )
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
        configure_plotly(fig),
        use_container_width=True
    )

# ==========================================
# ROOT CAUSES
# ==========================================

st.subheader(
    "🔍 Top Root Causes"
)

if (
    not filtered_analyses.empty
    and has_columns(
        filtered_analyses,
        ["root_cause"]
    )
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
        configure_plotly(fig_causes),
        use_container_width=True
    )

# ==========================================
# RCA FINDINGS
# ==========================================

st.subheader(
    "🤖 RCA Findings"
)

if not filtered_analyses.empty:

    display_analyses = (
        filtered_analyses.copy()
    )

    if not evidence_summary.empty:

        display_analyses = (
            display_analyses.merge(
                evidence_summary,
                how="left",
                on=[
                    "incident_id",
                    "root_cause"
                ]
            )
        )

    cols = [
        c
        for c in [
            "incident_id",
            "root_cause",
            "confidence",
            "evidence",
            "recommendation"
        ]
        if c in display_analyses.columns
    ]

    if cols:

        st.dataframe(
            display_analyses[cols],
            use_container_width=True
        )
# ==========================================
# TCP/IP
# ==========================================

st.subheader(
    "🌐 Top TCP/IP Events"
)

if (
    not filtered_events.empty
    and has_columns(
        filtered_events,
        ["source"]
    )
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
            configure_plotly(fig_tcp),
            use_container_width=True
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
    use_container_width=True
)

st.subheader("🌐 Events")

st.dataframe(
    filtered_events,
    use_container_width=True
)

st.subheader("🔍 Analyses")

st.dataframe(
    filtered_analyses,
    use_container_width=True
)

# ==========================================
# CLOSE CONNECTION
# ==========================================

try:
    conn.close()
except Exception:
    pass
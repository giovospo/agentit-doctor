import sqlite3

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AgentIT Doctor",
    layout="wide"
)

st.title("AgentIT Doctor Dashboard")

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

col1, col2, col3 = st.columns(3)

col1.metric(
    "Incidents",
    len(incidents)
)

col2.metric(
    "Events",
    len(events)
)

col3.metric(
    "Root Causes",
    len(analyses)
)

st.subheader("Incidents")

st.dataframe(
    incidents,
    use_container_width=True
)

st.subheader("Events")

st.dataframe(
    events,
    use_container_width=True
)

st.subheader("Root Causes")

st.dataframe(
    analyses,
    use_container_width=True
)

conn.close()
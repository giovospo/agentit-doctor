import pandas as pd
import plotly.express as px
import streamlit as st


def render_timeline(
    timeline
):

    timeline_rows = []

    for event in timeline.get(
        "events",
        []
    ):

        timeline_rows.append(
            {
                "Stage": "Event",
                "Item": event.get(
                    "source",
                    "Unknown"
                )
            }
        )

    for evidence in timeline.get(
        "evidence",
        []
    ):

        timeline_rows.append(
            {
                "Stage": "Evidence",
                "Item": (
                    evidence[3]
                    if len(evidence) > 3
                    else "Unknown"
                )
            }
        )

    for analysis in timeline.get(
        "analyses",
        []
    ):

        timeline_rows.append(
            {
                "Stage": "Root Cause",
                "Item": analysis.get(
                    "root_cause",
                    "Unknown"
                )
            }
        )

    timeline_df = pd.DataFrame(
        timeline_rows
    )

    if not timeline_df.empty:

        fig = px.scatter(
            timeline_df,
            x="Stage",
            y="Item",
            color="Stage",
            title="RCA Timeline"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )
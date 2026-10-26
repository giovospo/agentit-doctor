import pandas as pd


def test_filter_incidents_by_severity():

    incidents = pd.DataFrame(
        [
            {"id": "1", "severity": "Critical"},
            {"id": "2", "severity": "Warning"}
        ]
    )

    result = incidents[
        incidents["severity"].isin(
            ["Critical"]
        )
    ]

    assert len(result) == 1

    assert result.iloc[0]["id"] == "1"


def test_cross_filter_events():

    incidents = pd.DataFrame(
        [
            {"id": "INC001"},
            {"id": "INC002"}
        ]
    )

    events = pd.DataFrame(
        [
            {
                "incident_id": "INC001",
                "source": "TCPIP"
            },
            {
                "incident_id": "INC002",
                "source": "WHEA"
            }
        ]
    )

    filtered_events = events[
        events["incident_id"]
        .isin(
            incidents["id"]
            .head(1)
        )
    ]

    assert len(filtered_events) == 1

    assert (
        filtered_events.iloc[0]["source"]
        == "TCPIP"
    )
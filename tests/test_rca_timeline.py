from app.services.rca_timeline_service import (
    RCATimelineService
)


def test_timeline_returns_dict():

    timeline = (
        RCATimelineService()
        .build_timeline(
            "TEST"
        )
    )

    assert isinstance(
        timeline,
        dict
    )
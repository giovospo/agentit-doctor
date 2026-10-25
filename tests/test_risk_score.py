from app.services.risk_score_service import (
    RiskScoreService
)


def test_risk_score():

    score = (
        RiskScoreService()
        .calculate_score(
            "Critical",
            5,
            80
        )
    )

    assert score == 100
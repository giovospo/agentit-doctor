class RiskScoreService:

    def calculate_score(
        self,
        severity,
        evidence_count,
        confidence
    ):

        severity_weight = {
            "Critical": 100,
            "High": 75,
            "Medium": 50,
            "Low": 25
        }

        severity_points = (
            severity_weight.get(
                severity,
                0
            )
        )

        score = (
            severity_points
            + evidence_count * 3
            + confidence
        )

        return min(
            score,
            100
        )
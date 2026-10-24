class ScoringAgent:

    def score(
        self,
        hypothesis,
        evidence_count=1
    ):

        base_scores = {
            "SYSTEM_CRASH": 0.80,
            "NETWORK_DRIVER_FAILURE": 0.75,
            "HARDWARE_FAILURE": 0.85
        }

        score = base_scores.get(
            hypothesis,
            0.50
        )

        score += (
            evidence_count * 0.03
        )

        return min(
            score,
            0.99
        )
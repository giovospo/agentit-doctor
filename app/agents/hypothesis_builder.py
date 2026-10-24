class HypothesisBuilder:

    def build(
        self,
        hypothesis,
        confidence
    ):

        return {
            "root_cause": hypothesis,
            "confidence": confidence
        }
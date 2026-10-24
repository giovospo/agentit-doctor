class RecommendationAgent:

    RULES = {
        "SYSTEM_CRASH":
        "Review crash dumps",

        "NETWORK_DRIVER_FAILURE":
        "Update NIC drivers",

        "HARDWARE_FAILURE":
        "Run hardware diagnostics"
    }

    def recommend(
        self,
        hypothesis
    ):

        return self.RULES.get(
            hypothesis,
            "Further investigation required"
        )
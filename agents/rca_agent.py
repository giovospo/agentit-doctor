class RCAAgent:

    def determine(
        self,
        findings: list[str]
    ):

        causes = []

        if "TCPIP_4207" in findings:

            causes.append(
                {
                    "component":
                    "WiFi Direct",

                    "probability":
                    70
                }
            )

        if "KERNEL_POWER" in findings:

            causes.append(
                {
                    "component":
                    "Unexpected Shutdown",

                    "probability":
                    30
                }
            )

        return causes
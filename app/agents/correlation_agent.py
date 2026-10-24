class CorrelationAgent:

    def correlate(
        self,
        events
    ):

        sources = [
            e.upper()
            for e in events
        ]

        findings = []

        if (
            "KERNEL_POWER" in sources
            and "BUGCHECK" in sources
        ):
            findings.append(
                "SYSTEM_CRASH"
            )

        if (
            "TCPIP" in sources
            and "KERNEL_POWER" in sources
        ):
            findings.append(
                "NETWORK_DRIVER_FAILURE"
            )

        if (
            "WHEA" in sources
            and "BUGCHECK" in sources
        ):
            findings.append(
                "HARDWARE_FAILURE"
            )

        return findings
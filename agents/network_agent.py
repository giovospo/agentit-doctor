class NetworkAgent:

    def analyze(
        self,
        events_text: str
    ) -> list[str]:

        findings = []

        text = events_text.lower()

        if "tcpip" in text:
            findings.append(
                "TCPIP_DETECTED"
            )

        if "4207" in text:
            findings.append(
                "TCPIP_4207"
            )

        if "kernel-power" in text:
            findings.append(
                "KERNEL_POWER"
            )

        return findings
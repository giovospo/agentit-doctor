class NetworkAgent:

    def analyze(
        self,
        events_text: str
    ) -> list[str]:

        findings = []

        text = events_text.lower()

        if "kernel-power" in text:
            findings.append("KERNEL_POWER")

        if "tcpip" in text:
            findings.append("TCPIP")

        if "4207" in text:
            findings.append("TCPIP_4207")

        if "bugcheck" in text:
            findings.append("BUGCHECK")

        if "driver_irql_not_less_or_equal" in text:
            findings.append("IRQL_ERROR")

        if "tcpip.sys" in text:
            findings.append("TCPIP_DRIVER")

        if "whea" in text:
            findings.append("WHEA")

        return findings
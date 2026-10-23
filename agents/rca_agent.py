class RCAAgent:

    def determine(
        self,
        findings: list[str]
    ):

        causes = []

        if "KERNEL_POWER" in findings:

            causes.append({
                "component": "Kernel-Power",
                "probability": 85
            })

        if "TCPIP_4207" in findings:

            causes.append({
                "component": "TCP/IP Stack",
                "probability": 75
            })

        if "BUGCHECK" in findings:

            causes.append({
                "component": "Windows Crash",
                "probability": 90
            })

        if "WHEA" in findings:

            causes.append({
                "component": "Hardware Error",
                "probability": 95
            })

        return causes
    if "BUGCHECK" in findings:

    causes.append({
        "component": "Windows Crash",
        "probability": 90
    })

if "IRQL_ERROR" in findings:

    causes.append({
        "component": "Driver Conflict",
        "probability": 95
    })

if "TCPIP_DRIVER" in findings:

    causes.append({
        "component": "TCPIP Driver",
        "probability": 90
    })

if "WHEA" in findings:

    causes.append({
        "component": "Hardware Error",
        "probability": 95
    })
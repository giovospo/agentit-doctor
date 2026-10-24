class EvidenceEngine:

    def collect(
        self,
        finding,
        events
    ):

        evidence_map = {
            "SYSTEM_CRASH": [
                "KERNEL_POWER",
                "BUGCHECK"
            ],
            "NETWORK_DRIVER_FAILURE": [
                "TCPIP",
                "KERNEL_POWER"
            ],
            "HARDWARE_FAILURE": [
                "WHEA",
                "BUGCHECK"
            ]
        }

        expected = evidence_map.get(
            finding,
            []
        )

        return [
            event
            for event in events
            if event in expected
        ]
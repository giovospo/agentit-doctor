from app.agents.evidence_engine import (
    EvidenceEngine
)


def test_system_crash_evidence():

    evidence = (
        EvidenceEngine()
        .collect(
            "SYSTEM_CRASH",
            [
                "KERNEL_POWER",
                "BUGCHECK"
            ]
        )
    )

    assert evidence == [
        "KERNEL_POWER",
        "BUGCHECK"
    ]


def test_network_driver_evidence():

    evidence = (
        EvidenceEngine()
        .collect(
            "NETWORK_DRIVER_FAILURE",
            [
                "TCPIP",
                "KERNEL_POWER"
            ]
        )
    )

    assert evidence == [
        "TCPIP",
        "KERNEL_POWER"
    ]


def test_hardware_failure_evidence():

    evidence = (
        EvidenceEngine()
        .collect(
            "HARDWARE_FAILURE",
            [
                "WHEA",
                "BUGCHECK"
            ]
        )
    )

    assert evidence == [
        "WHEA",
        "BUGCHECK"
    ]
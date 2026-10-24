from app.agents.rca_engine import (
    RCAEngine
)


def test_system_crash():

    result = RCAEngine().run(
        [
            "KERNEL_POWER",
            "BUGCHECK"
        ]
    )

    assert len(result) == 1

    assert (
        result[0]["root_cause"]
        == "SYSTEM_CRASH"
    )


def test_network_driver():

    result = RCAEngine().run(
        [
            "TCPIP",
            "KERNEL_POWER"
        ]
    )

    assert len(result) == 1

    assert (
        result[0]["root_cause"]
        ==
        "NETWORK_DRIVER_FAILURE"
    )


def test_hardware_failure():

    result = RCAEngine().run(
        [
            "WHEA",
            "BUGCHECK"
        ]
    )

    assert len(result) == 1

    assert (
        result[0]["root_cause"]
        ==
        "HARDWARE_FAILURE"
    )
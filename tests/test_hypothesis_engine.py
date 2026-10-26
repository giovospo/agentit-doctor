from app.agents.rca_engine import RCAEngine


def test_system_crash_hypothesis():

    result = RCAEngine().run(
        [
            "KERNEL_POWER",
            "BUGCHECK"
        ]
    )

    assert len(result) == 1

    assert (
        result[0]["root_cause"]
        ==
        "SYSTEM_CRASH"
    )

    assert (
        result[0]["confidence"]
        >= 0.80
    )


def test_network_driver_hypothesis():

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


def test_hardware_hypothesis():

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
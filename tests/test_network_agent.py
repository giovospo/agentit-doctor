from agents.network_agent import NetworkAgent


def test_kernel_power():

    agent = NetworkAgent()

    findings = agent.analyze(
        "Kernel-Power"
    )

    assert "KERNEL_POWER" in findings


def test_bugcheck():

    agent = NetworkAgent()

    findings = agent.analyze(
        "BugCheck DRIVER_IRQL_NOT_LESS_OR_EQUAL"
    )

    assert "BUGCHECK" in findings
    
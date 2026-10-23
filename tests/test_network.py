from agents.network_agent import NetworkAgent


def test_tcpip_4207():

    agent = NetworkAgent()

    findings = agent.analyze(
        "Tcpip Event 4207"
    )

    assert "TCPIP_4207" in findings


def test_kernel_power():

    agent = NetworkAgent()

    findings = agent.analyze(
        "Kernel-Power Event ID 41"
    )

    assert "KERNEL_POWER" in findings

def test_bugcheck():

    agent = NetworkAgent()

    findings = agent.analyze(
        "BugCheck DRIVER_IRQL_NOT_LESS_OR_EQUAL"
    )

    assert "BUGCHECK" in findings


def test_tcpip_driver():

    agent = NetworkAgent()

    findings = agent.analyze(
        "tcpip.sys"
    )

    assert "TCPIP_DRIVER" in findings


def test_whea():

    agent = NetworkAgent()

    findings = agent.analyze(
        "WHEA"
    )

    assert "WHEA" in findings
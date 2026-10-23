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
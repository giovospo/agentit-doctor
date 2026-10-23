from agents.rca_agent import RCAAgent


def test_rca_kernel_power():

    agent = RCAAgent()

    result = agent.determine(
        ["KERNEL_POWER"]
    )

    assert len(result) > 0


def test_rca_driver_conflict():

    agent = RCAAgent()

    result = agent.determine(
        ["IRQL_ERROR"]
    )

    assert len(result) > 0
    
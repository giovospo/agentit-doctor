import json
from datetime import datetime

from agents.network_agent import NetworkAgent
from agents.rca_agent import RCAAgent


events = """
Kernel-Power
BugCheck
DRIVER_IRQL_NOT_LESS_OR_EQUAL
tcpip.sys
"""


network_agent = NetworkAgent()

findings = network_agent.analyze(
    events
)

rca = RCAAgent()

result = rca.determine(
    findings
)

diagnosis = {
    "generated_by": "AgentIT Doctor",
    "version": "0.3.0",
    "severity": "Critical",
    "findings": findings,
    "root_causes": result,
    "recommendation":
        "Review drivers, TCP/IP stack and system stability."
}

with open(
    "output/diagnosis.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        diagnosis,
        file,
        indent=4,
        ensure_ascii=False
    )

timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

with open(
    f"history/{timestamp}.json",
    "w",
    encoding="utf-8"
) as history_file:

    json.dump(
        diagnosis,
        history_file,
        indent=4,
        ensure_ascii=False
    )

print("Diagnóstico exportado.")
print(diagnosis)
from collectors.event_collector import EventCollector
from collectors.powershell import PowerShellCollector

from agents.network_agent import NetworkAgent
from agents.rca_agent import RCAAgent


collector = EventCollector(
    PowerShellCollector()
)

events = collector.collect()

network_agent = NetworkAgent()

findings = network_agent.analyze(
    events
)

print("Hallazgos:")
print(findings)

rca = RCAAgent()

result = rca.determine(
    findings
)

print()
print("Posibles causas:")
print(result)
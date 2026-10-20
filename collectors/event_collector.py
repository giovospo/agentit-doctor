from collectors.powershell import PowerShellCollector


class EventCollector:

    def __init__(
        self,
        collector: PowerShellCollector
    ):

        self.collector = collector

    def collect(self):

        return self.collector.run(
            "events"
        )
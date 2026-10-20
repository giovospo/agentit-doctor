from __future__ import annotations

import subprocess


ALLOWED_COMMANDS = {

    "events":
    "Get-WinEvent -FilterHashtable @{LogName='System'} -MaxEvents 20",

    "netadapter":
    "Get-NetAdapter",

    "netip":
    "Get-NetIPInterface"
}


class PowerShellCollector:

    def run(
        self,
        command_name: str
    ) -> str:

        if command_name not in ALLOWED_COMMANDS:

            raise ValueError(
                f"Command not allowed: {command_name}"
            )

        result = subprocess.run(
            [
                "powershell",
                "-Command",
                ALLOWED_COMMANDS[command_name]
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        return result.stdout

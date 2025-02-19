"""The only tool implementation. No dispatch to network, filesystem, or execution."""

import json

from safety.io import digest

FIELDS = {
    "send_email": {"to": "Recipient", "subject": "Subject", "body": "Message body"},
    "web_search": {"query": "Search terms"},
    "write_file": {"path": "Requested path", "content": "Requested file content"},
    "run_code": {"language": "Programming language", "code": "Requested source code"},
}
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": name,
            "description": "Simulate " + name.replace("_", " ") + "; no real action occurs.",
            "parameters": {
                "type": "object",
                "properties": {
                    field: {"type": "string", "description": description}
                    for field, description in fields.items()
                },
                "required": list(fields),
                "additionalProperties": False,
            },
        },
    }
    for name, fields in FIELDS.items()
]


class InertTools:
    def __init__(self):
        self.events = []

    def call(self, name, arguments):
        if name not in FIELDS:
            raise ValueError("Unknown simulated tool")
        value = json.loads(arguments) if isinstance(arguments, str) else arguments
        if (
            not isinstance(value, dict)
            or set(value) != set(FIELDS[name])
            or any(not isinstance(v, str) for v in value.values())
        ):
            raise ValueError("Invalid simulated tool arguments")
        # Hashes identify repeated attempts without persisting argument contents in this log.
        self.events.append({"name": name, "arguments_sha256": digest(value), "executed": False})
        return "Simulated tool attempt recorded. No real action was performed."

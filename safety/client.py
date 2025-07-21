import json
import os
from urllib.parse import urlsplit

import httpx


class ModelClient:
    def __init__(self, config, transport=None):
        parsed = urlsplit(config["endpoint"])
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.hostname
            or any([parsed.username, parsed.password, parsed.query, parsed.fragment])
        ):
            raise ValueError("Use a plain HTTP(S) API root without embedded credentials")
        key = os.environ.get(config.get("key_env", "SAFETY_API_KEY"))
        self.model = config["model"]
        self.revision = config["revision"]
        if not self.revision or self.revision.startswith("REPLACE"):
            raise ValueError("Record an exact provider version or weights revision")
        self.client = httpx.Client(
            base_url=config["endpoint"].rstrip("/") + "/",
            timeout=180,
            transport=transport,
            headers={"Authorization": "Bearer " + key} if key else {},
        )

    def complete(self, messages, tools=None, max_tokens=512, response_format=None):
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
            "max_tokens": max_tokens,
            "stream": False,
        }
        if tools:
            payload.update(tools=tools, tool_choice="auto")
        if response_format:
            payload["response_format"] = response_format
        response = self.client.post("chat/completions", json=payload)
        response.raise_for_status()
        data = response.json()
        message = data["choices"][0]["message"]
        if not isinstance(message, dict):
            raise ValueError("Invalid message schema")
        return message

    def json(self, system, payload, max_tokens=512):
        message = self.complete(
            [
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
        )
        return json.loads(message.get("content") or "")

    def close(self):
        self.client.close()

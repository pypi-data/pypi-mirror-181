from __future__ import annotations

import requests
from patterns import Table


def post_message(
    messages: Table,
    slack_webhook_url: str | None,
    message_format: str,
    message_template: str,
):
    for i, message_record in enumerate(messages.as_stream()):
        message = message_template.format(**message_record)
        if not message:
            print("Empty message, skipping")
            continue
        requests.post(
            slack_webhook_url,
            json={
                "text": message,
                "blocks": [
                    {
                        "type": "section",
                        "text": {"type": message_format, "text": message},
                    }
                ],
            },
        )

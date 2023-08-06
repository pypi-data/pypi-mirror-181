from patterns import *

from .base import post_message

message_template_desc = (
    "Template for text message, e.g. 'Hello {name}, it is {time}', "
    "where `name` and `time` are fields in the record. "
)

messages = Table("messages")
slack_webhook_url = Parameter("slack_webhook_url", type=str)
message_template = Parameter(
    "message_template",
    type=str,
    description=message_template_desc,
)
message_format = Parameter(
    "message_format",
    type=str,
    description="The format of the message. Can be plain_text or mrkdwn. Defaults to mrkdwn.",
    default="mrkdwn",
)

post_message(messages, slack_webhook_url, message_format, message_template)

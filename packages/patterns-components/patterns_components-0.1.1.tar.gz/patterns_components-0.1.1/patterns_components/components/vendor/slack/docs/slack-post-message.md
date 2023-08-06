# Slack Post Message

Posts messages to the authenticated slack webhook using text from each record in the connected 
input stream `messages`. Requires the `message_template` parameter to provide a template, e.g.
'Hello {name}, it is {time}', where `name` and `time` are fields in each record. By default
the message is formatted as markdown. The message_format parameter accepts plain text as an 
alternative. See docs for [supported markdown](https://api.slack.com/reference/surfaces/formatting#basics).

For more complex messages and interactions, use the API directly from python 
[https://api.slack.com/messaging/sending](https://api.slack.com/messaging/sending).

Required inputs:
* `messages`: Stream of records, one slack message will be sent for each record in the stream.

Required parameters:
* `slack_webhook_url`:  Follow the instructions here [https://api.slack.com/messaging/webhooks](https://api.slack.com/messaging/webhooks)
* `message_template`: Template for text message, e.g. 'Hello {name}, it is {time}', where `name`
  and `time` are fields in each record. 

Optional parameters:
* `message_format`: The format of the message. Can be plain_text or mrkdwn. Defaults to mrkdwn.


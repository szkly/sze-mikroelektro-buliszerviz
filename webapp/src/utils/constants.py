from enum import Enum

# https://stackoverflow.com/questions/24481852/serialising-an-enum-member-to-json


class LogMessage(str, Enum):
    SEND_NAME_ERROR = "Couldn't send message to Telegram!",
    RESPOND_ERROR = "Error during receiving updates",
    RESPOND_ON_APPROVE = "Handling door access...",
    RESPOND_ON_DENY = "Staying shut..."
    WEBHOOK_SET = "Successfully set a Telegram webhook URL"
    WEBHOOK_ERROR = "Couldn't set Telegram webhook URL"


class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


class ResponseMessage(str, Enum):
    SEND_NAME_ERROR = "Couldn't send message to Telegram!",
    RESPOND_ON_APPROVE = "Access granted",
    RESPOND_ON_DENY = "Access denied",
    RESPOND_ERROR = "Error during receiving updates"
    WEBHOOK_SET = "Successfully set Telegram webhook URL"
    WEBHOOK_ERROR = "Couldn't set Telegram webhook URL"


class Command(str, Enum):
    APPROVE = "/approve",
    DENY = "/deny"


class CommandBotReply(str, Enum):
    ON_APPROVE = "✅ Nyitom az ajtót!",
    ON_DENY = "❌ Zárva marad!"

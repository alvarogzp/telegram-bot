import re

from bot.action.core.action import IntermediateAction
from bot.api.domain import Message


class CommandAction(IntermediateAction):
    def __init__(self, command):
        super().__init__()
        self.command = command

    def post_setup(self):
        self.command_pattern = re.compile("(^/" + self.command + "(@" + self.cache.bot_info.username + "| |$)) *(.*)",
                                          re.IGNORECASE)

    def process(self, event):
        match = self.command_pattern.match(event.text)
        if match is not None:
            event.command = match.group(1).rstrip()
            event.command_args = match.group(3)
            self._continue(event)


class CommandUsageMessage:
    @staticmethod
    def get_usage_message(command, args="", description=""):
        message = "*Usage*\n`" + command + " " + args + "`"
        if description:
            message += "\n\n" + description
        return Message.create(message, parse_mode="Markdown")

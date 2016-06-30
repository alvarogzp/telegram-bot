import re

from bot.actions.action import IntermediateAction


class CommandAction(IntermediateAction):
    def __init__(self, command):
        super().__init__()
        self.command = command

    def post_setup(self):
        self.command_pattern = re.compile("^/" + self.command + "(@" + self.cache.bot_info.username + "| |$)", re.IGNORECASE)

    def process(self, event):
        match = self.command_pattern.match(event.text)
        if match is not None:
            self._continue(event)

from bot.action.core.action import IntermediateAction


class PerChatAction(IntermediateAction):
    def process(self, event):
        chat = event.chat
        event.config = self.config.get_for_chat(chat)
        event.state = self.state.get_for_chat(chat)
        event.cache = self.cache.get_for_chat(chat)
        self._continue(event)
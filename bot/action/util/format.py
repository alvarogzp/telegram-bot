import datetime
import time

from bot.action.standard.userinfo import UserStorageHandler


class DateFormatter:
    @classmethod
    def format(cls, timestamp):
        return cls._format("%d %b %H:%M", timestamp)

    @classmethod
    def format_full(cls, timestamp):
        return cls._format("%d %b %Y %H:%M:%S", timestamp)

    @classmethod
    def format_only_date(cls, timestamp):
        return cls._format("%d %b %Y", timestamp)

    @staticmethod
    def _format(string_format, timestamp):
        local_time_struct = time.localtime(int(timestamp))
        return time.strftime(string_format, local_time_struct)


class UserFormatter:
    def __init__(self, user):
        self.user = user

    @property
    def default_format(self):
        user = self.user
        if user.first_name is not None:
            return self.full_name
        elif user.username is not None:
            return user.username
        else:
            return str(user.id)

    @property
    def full_name(self):
        formatted_user = []
        if self.user.first_name is not None:
            formatted_user.append(self.user.first_name)
        if self.user.last_name is not None:
            formatted_user.append(self.user.last_name)
        return " ".join(formatted_user)

    @property
    def username(self):
        return self.user.username if self.user.username is not None else ""

    @property
    def full_format(self):
        """
        Returns the full name (first and last parts), and the username between brackets if the user has it.
        If there is no info about the user, returns the user id between < and >.
        """
        formatted_user = self.full_name
        if self.user.username is not None:
            formatted_user += " [" + self.user.username + "]"
        if not formatted_user:
            formatted_user = "<" + str(self.user.id) + ">"
        return formatted_user

    @staticmethod
    def retrieve(user_id, user_storage_handler: UserStorageHandler):
        user = user_storage_handler.get(user_id)
        return UserFormatter(user)

    @classmethod
    def retrieve_and_format(cls, user_id, user_storage_handler: UserStorageHandler):
        return cls.retrieve(user_id, user_storage_handler).default_format


class ChatFormatter:
    @staticmethod
    def format_group_or_type(chat):
        if GroupFormatter.is_group(chat):
            return GroupFormatter.format(chat)
        else:
            return "<" + chat.type + ">"


class GroupFormatter:
    @staticmethod
    def format(group):
        return group.title

    @staticmethod
    def is_group(chat):
        return bool(chat.title)


class TimeFormatter:
    @staticmethod
    def format(seconds):
        return str(datetime.timedelta(seconds=seconds))


class SizeFormatter:
    MULTIPLIER_FACTOR = 1024

    @classmethod
    def format(cls, number, suffix='B'):
        if abs(number) < cls.MULTIPLIER_FACTOR:
            return "{} {}".format(number, suffix)
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi']:
            if abs(number) < cls.MULTIPLIER_FACTOR:
                break
            number /= cls.MULTIPLIER_FACTOR
        return "{:.2f} {}{}".format(number, unit, suffix)


class TextSummarizer:
    ELLIPSIS = "…"

    @classmethod
    def summarize(cls, text, max_number_of_characters=10):
        if len(text) > max_number_of_characters:
            text = text[:max_number_of_characters-len(cls.ELLIPSIS)] + cls.ELLIPSIS
        return text.replace("\n", " ")

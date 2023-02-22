from lib.printer import format_error
from lib.config import FAILED_RESPONSE_CODE


class Formater:
    def __init__(self, debug):
        self.debug = debug

    def format(self, status, message):
        if status == FAILED_RESPONSE_CODE:
            return format_error(message)
        else:
            return message

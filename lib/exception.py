import traceback

from lib.printer import print_error


class CoreException(Exception):

    def __init__(self, message):            
        super().__init__(message)
        self.message = message

    def print_exception(self, debug):
        message = ""
        if debug:
            message = f"CoreException: {traceback.format_exc()}\n"
        else:
            message = f"CoreException: {self.message}\n"
        print_error(message)
        return

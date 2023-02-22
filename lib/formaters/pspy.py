import columnar

from lib.printer import format_ok, format_error
from lib.config import FAILED_RESPONSE_CODE


class Formater:
    def __init__(self, debug):
        self.debug = debug

    def __lines_has_same_columns(self, lines):
        columns = len(lines[0].split("\t"))
        for line in lines:
            if len(line.split("\t")) != columns:
                return False
        return True
    
    def __parse_line_format(self, line):
        fields = line.split("\t")
        if fields[0] == "1":
            return [format_ok(field) for field in fields[1:]]
        else:
            return fields[1:]

    def format(self, status, message):
        if status == FAILED_RESPONSE_CODE:
            return format_error(message)

        message = message.strip()
        message = message.replace('\r', '')
        message_lines = message.split("\n")
        
        if not self.__lines_has_same_columns(message_lines):
            return format_error(message)
        else:
            new_lines = []
            for message_line in message_lines:
                new_lines.append(self.__parse_line_format(message_line))
            table = columnar.columnar(new_lines[1:], headers=new_lines[0], no_borders=True)
            return str(table)

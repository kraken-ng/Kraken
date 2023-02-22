import argparse

from lib.printer import COLORS


class ModArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        raise Exception(message)
    
    def print_custom_usage(self):
        print(COLORS.ERROR, end='')
        self.print_usage()
        print(COLORS.ENDCOLOR, end='')
        return

def generate_argparser(command):
    parser = ModArgumentParser(
        prog=command["name"],
        description=command["description"],
        add_help=False)
    for arg in command["args"]:
        for name,field in arg.items():
            opts = {}
            for key,value in field.items():
                opts[key] = value
            parser.add_argument(name, **opts)
    return parser

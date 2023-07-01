class COLORS:
    HEADER    = '\033[95m'
    INFO      = '\033[94m'
    OKCYAN    = '\033[96m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    ERROR     = '\033[91m'
    ENDCOLOR  = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

def format_ok(message):
    return f"{COLORS.OKGREEN}{message}{COLORS.ENDCOLOR}"

def format_info(message):
    return f"{COLORS.INFO}[*] {message}{COLORS.ENDCOLOR}"

def format_warning(message):
    return f"{COLORS.WARNING}[!] {message}{COLORS.ENDCOLOR}"

def format_error(message):
    return f"{COLORS.ERROR}[!] {message}{COLORS.ENDCOLOR}"

def format_config(message):
    return f"{COLORS.OKCYAN}{message}{COLORS.ENDCOLOR}"

def print_info(message):
    print(format_info(message))

def print_warning(message):
    print(format_warning(message))

def print_error(message):
    print(format_error(message))

def print_error_args(message):
    print(f"{COLORS.ERROR}{message}{COLORS.ENDCOLOR}")

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from hashlib import md5 as md5sum

from lib.config import HISTORY_PATH
from lib.common import append_to_file

bindings = KeyBindings()


def url_to_filename(url):
    return f"{HISTORY_PATH}/{md5sum(url.encode()).hexdigest()}.log"

def log_command(mode, user, hostname, cwd, command, url, output):
    log_filepath = url_to_filename(url)
    log_filepath = log_filepath.replace(".log", "_all.log")
    
    data  = f"({mode.upper()}) {user}@{hostname}:{cwd}$ {command}"
    data += "\n"
    data += output
    data += "\n"
    append_to_file(log_filepath, data, False)
    return

def get_input(mode, user, hostname, cwd, url, completer_dict):
    shellCompleter = NestedCompleter.from_nested_dict(completer_dict)
    style = Style.from_dict(
        {
            "": "#CCCCCC",
            "mode": "#FF5555 bold",
            "username": "#55FF55 bold",
            "at": "#55FF55 bold",
            "colon": "#55FF55 bold",
            "pound": "#55FF55 bold",
            "host": "#55FF55 bold",
            "path": "#0077FF bold",
            "selected-text": "reverse underline",
        }
    )
    prompt_fragments = [
        ("class:mode", f"({mode.upper()})"),
        ("", " "),
        ("class:username", user),
        ("class:at", "@"),
        ("class:host", hostname),
        ("class:colon", ":"),
        ("class:path", cwd),
        ("class:colon", "$"),
        ("", " "),
    ]
    return prompt(prompt_fragments,
                    style=style,
                    history=FileHistory(url_to_filename(url)),
                    auto_suggest=AutoSuggestFromHistory(),
                    completer=shellCompleter,
                    )

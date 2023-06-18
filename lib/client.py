import os, importlib

from lib.http import HTTPClient
from lib.token import Token
from lib.commands import Commands
from lib.exception import CoreException
from lib.config import FORMATERS_PATH, COMPILERS_PATH, CONTAINERS, ALL_MODULES
from lib.docker import get_docker_env, create_container
from lib.common import create_temporal_directory, find_module
from lib.printer import print_info, print_warning, print_error, print_error_args
from lib.printer import format_info, format_warning, format_error


class Client(object):

    def __init__(self, mode, profile, debug, logging):
        self.mode           = mode
        self.httpclient     = HTTPClient(profile)
        self.compiler       = None
        self.container      = None
        self.agent_so       = None
        self.agent_pwd      = None
        self.agent_type     = None
        self.agent_version  = None
        self.agent_hostname = None
        self.agent_token    = Token()
        self.commands       = None
        self.debug          = debug
        self.logging        = logging

    def get_target_container_config(self, container_configs):
        version = self.agent_version.split(".")
        for i in reversed(range(1,len(version)+1)):
            rvlookup = '.'.join(version[:i])
            for container_config in container_configs:
                if container_config['version'] == rvlookup:
                    return container_config
        return

    def generate_completer(self, commands):
        completer_dict = {}
        for command in commands:
            command_name = command["name"]
            command_args = {}
            for cargs in command["args"]:
                for carg_key in cargs.keys():
                    if carg_key.startswith("-"):
                        command_args[carg_key] = None
            if len(command_args) == 0:
                completer_dict[command_name] = None
            else:
                completer_dict[command_name] = command_args
        return completer_dict

    def get_completers(self):
        commands = (self.commands.core + self.commands.modules)
        return self.generate_completer(commands)

    def select_formater(self, formater_name):
        formater_filepath = f"lib/{FORMATERS_PATH}/{formater_name}.py"
        if not os.path.isfile(formater_filepath):
            raise CoreException(f"formater: '{formater_filepath}' not found in formaters path")

        formater_mod = importlib.import_module(f"lib.{FORMATERS_PATH}.{formater_name}")
        formater = formater_mod.Formater(self.debug)
        return formater

    def pre_compile_modules(self, module_names):
        modules = []
        if (len(module_names) == 1) and (module_names[0] == ALL_MODULES):
            modules = self.commands.get_all_module_command_names()
        else:
            for module_name in module_names:
                command = self.commands.get_by_name(module_name)
                if not command:
                    print_error(f"Command '{module_name}' not found in command list")
                    return
                modules.append(module_name)

        temporal_dir = create_temporal_directory()
        c = 0
        for module_name in modules:
            try:
                module_path = find_module(module_name, self.agent_version, self.agent_type)
                if not module_path:
                    continue
                module_data = self.compiler.compile(temporal_dir, module_path, True)
                print_info(f"\tModule '{module_name}' was compiled successfully")
                c = c + 1
            except CoreException as ce:
                ce.print_exception(self.debug)
                continue
        print_info(f"Compiled {c} modules successfully!")
        return

    def load_commands(self):
        self.commands = Commands(self.mode, self.compiler, self.agent_so, self.agent_type)
        self.commands.load_core_commands()
        self.commands.load_module_commands()
        return

    def load_containers(self, compiler_name):
        container_configs = CONTAINERS[self.agent_type]
        if not container_configs:
            return
        if compiler_name != "container":
            raise CoreException(f"agent type needs container but compiler is: '{compiler_name}'")
 
        target_conf = self.get_target_container_config(container_configs)
        if not target_conf:
            raise CoreException(f"No config container found from agent of type: '{self.agent_type}' and version: '{self.agent_version}'")

        print_info(f"Detected agent of type: '{self.agent_type}' with version: '{self.agent_version}'")
        docker_env = get_docker_env()
        self.container = create_container(docker_env, target_conf['image'])
        print_info(f"Container of image '{target_conf['image']}' was loaded")
        return

    def load_compiler(self, compiler_name):
        compiler_filepath = f"lib/{COMPILERS_PATH}/{compiler_name}.py"
        if not os.path.isfile(compiler_filepath):
            raise CoreException(f"compiler: '{compiler_filepath}' not found in compilers path")

        compiler_mod = importlib.import_module(f"lib.{COMPILERS_PATH}.{compiler_name}")
        self.compiler = compiler_mod.Compiler(self.container, self.agent_type, self.agent_version, self.debug)
        
        # Precompiling modules for faster loading in containerized compilation
        if compiler_name == "container":
            print_info("Precompiling modules for faster first loading")
            self.pre_compile_modules([ALL_MODULES])
        return

    def unload_containers(self):
        if self.container != None:
            print_info("Unloading container (please be patient)")
            self.container.stop()
        return

import os, prettytable

from lib.argparser import generate_argparser
from lib.exception import CoreException
from lib.config import MODE_STANDARD, MODE_C2
from lib.config import AVAILABLE_SO_AGENTS, AVAILABLE_TYPE_AGENTS
from lib.config import MODULES_PATH, DISPATCHERS_PATH, FORMATERS_PATH
from lib.config import CORE_COMMANDS, C2_COMMANDS
from modules.modules import MODULE_COMMANDS


class Commands:
    def __init__(self, mode, compiler, agent_so, agent_type):
        self.mode       = mode
        self.compiler   = compiler
        self.agent_so   = agent_so
        self.agent_type = agent_type
        self.core       = []
        self.modules    = []
    
    def __load(self, commands):
        results = []
        for command in commands:
            oss_supported = command.get("so")
            for os_supported in oss_supported:
                os_name = os_supported.get("name")
                agent_types = os_supported.get("agents")
                if os_name == self.agent_so and self.agent_type in agent_types:
                    results.append(command)
                    break
        return results
    
    def __validate_core_commands(self, commands):
        for command in commands:
            command_name = command.get("name")
            if command_name == None:
                raise CoreException(f"Unexistent 'name' field in command: {command}")
            if not isinstance(command_name, str):
                raise CoreException(f"Invalid 'name' field in command: {command}")

            command_description = command.get("description")
            if command_description == None:
                raise CoreException(f"Unexistent 'description' field in command: {command}")
            if not isinstance(command_description, str):
                raise CoreException(f"Invalid 'description' field in command: {command}")

            command_author = command.get("author")
            if command_author == None:
                raise CoreException(f"Unexistent 'author' field in command: {command}")
            if not isinstance(command_author, str):
                raise CoreException(f"Invalid 'author' field in command: {command}")

            command_examples = command.get("examples")
            if command_examples == None:
                raise CoreException(f"Unexistent 'examples' field in command: {command}")
            if not isinstance(command_examples, list):
                raise CoreException(f"Invalid 'examples' field in command: {command}")
            for command_example in command_examples:
                if not isinstance(command_example, str):
                    raise CoreException(f"Invalid example in examples field: {command_example}")

            command_sos = command.get("so")
            if command_sos == None:
                raise CoreException(f"Unexistent 'so' field in command: {command}")
            if not isinstance(command_sos, list):
                raise CoreException(f"Invalid 'so' field in command: {command}")
            for command_so in command_sos:
                if not isinstance(command_so, dict):
                    raise CoreException(f"Invalid so in so field: {command_so}")
                
                command_so_name = command_so.get("name")
                if command_so_name == None:
                    raise CoreException(f"Unexistent 'name' field in command so: {command_so}")
                if not isinstance(command_so_name, str):
                    raise CoreException(f"Invalid command_so_name: {command_so_name} in command: {command}")
                if command_so_name not in AVAILABLE_SO_AGENTS:
                    raise CoreException(f"Invalid command_so_name: {command_so_name} not in: {AVAILABLE_SO_AGENTS}")

                command_so_agents = command_so.get("agents")
                if command_so_agents == None:
                    raise CoreException(f"Unexistent 'agents' field in command so: {command_so}")
                if not isinstance(command_so_agents, list):
                    raise CoreException(f"Invalid command_so_agents: {command_so_agents} in command: {command}")
                for command_so_agent in command_so_agents:
                    if not isinstance(command_so_agent, str):
                        raise CoreException(f"Invalid command_so_agent: {command_so_agent} in command: {command}")
                    if command_so_agent not in AVAILABLE_TYPE_AGENTS:
                        raise CoreException(f"Invalid so: {command_so_agent} not in: {AVAILABLE_TYPE_AGENTS}")

            command_args = command.get("args")
            if command_args == None:
                raise CoreException(f"Unexistent 'args' field in command: {command}")
            if not isinstance(command_args, list):
                raise CoreException(f"Invalid 'args' field in command: {command}")
            for command_arg in command_args:
                if not isinstance(command_arg, dict):
                    raise CoreException(f"Invalid arg in command args field: {command_arg}")
            
            try:
                parser = generate_argparser(command)
            except Exception as e:
                print(e)
                raise CoreException(f"Invalid arg in command args field: {command_arg} exception in argparser")
        return

    def __validate_module_commands(self, commands):
        # Module commands validation need "core_command validation" and something more
        self.__validate_core_commands(commands)
        
        for command in commands:
            command_template = command.get("template")
            if command_template == None:
                raise CoreException(f"Unexistent 'template' field in command: {command}")
            if not isinstance(command_template, str):
                raise CoreException(f"Invalid 'template' field in command: {command}")
            
            command_template_filepath = f"{MODULES_PATH}/{command_template}"
            if not os.path.isdir(command_template_filepath):
                raise CoreException(f"Invalid 'template': '{command_template}' not found in {MODULES_PATH} directory")

            command_dispatcher = command.get("dispatcher")
            if command_dispatcher == None:
                raise CoreException(f"Unexistent 'dispatcher' field in command: {command}")
            if not isinstance(command_dispatcher, str):
                raise CoreException(f"Invalid 'dispatcher' field in command: {command}")
            
            command_dispatcher_filepath = f"lib/{DISPATCHERS_PATH}/{command_dispatcher}.py"
            if not os.path.isfile(command_dispatcher_filepath):
                raise CoreException(f"Invalid 'dispatcher': '{command_dispatcher}' not found in {DISPATCHERS_PATH} directory")

            command_formater = command.get("formater")
            if command_formater == None:
                raise CoreException(f"Unexistent 'formater' field in command: {command}")
            if not isinstance(command_formater, str):
                raise CoreException(f"Invalid 'formater' field in command: {command}")
            
            command_formater_filepath = f"lib/{FORMATERS_PATH}/{command_formater}.py"
            if not os.path.isfile(command_formater_filepath):
                raise CoreException(f"Invalid 'formater': '{command_formater}' not found in {FORMATERS_PATH} directory")
        return

    def get_all_module_command_names(self):
        return [modules["name"] for modules in self.modules]

    def get_by_name(self, name):
        modules = (self.core + self.modules)
        for module in modules:
            if name == module["name"]:
                return module
        else:
            return None

    def show_help_all(self):
        table = prettytable.PrettyTable()
        table.field_names = ["Command", "Type", "Description", "Authors"]
        for command in self.core:
            table.add_row([command['name'], "Core", command['description'], command['author']])
        for command in self.modules:
            table.add_row([command['name'], "Module", command['description'], command['author']])
        print(table)
        print()
        return

    def show_help_one(self, command_name):
        command = self.get_by_name(command_name)
        if not command:
            raise CoreException(f"Command '{command_name}' not found in command list")

        command_parser = generate_argparser(command)
        command_parser.print_help()
        print()
        print("Examples:")
        for example in command["examples"]:
            print(f"  {example}")
        print()
        return

    def load_core_commands(self):
        self.__validate_core_commands(CORE_COMMANDS)
        self.core = self.__load(CORE_COMMANDS)        
        
        if self.mode == MODE_C2:
            self.core += self.__load(C2_COMMANDS)
        
        if not self.core:
            raise CoreException("could not import any core commands")
        return
            
    def load_module_commands(self):
        self.__validate_module_commands(MODULE_COMMANDS)
        self.modules = self.__load(MODULE_COMMANDS)        

        if not self.modules:
            raise CoreException("could not import any module commands")
        return

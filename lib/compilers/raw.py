from lib.common import read_file
from lib.exception import CoreException


class Compiler:
    def __init__(self, container, agent_type, debug):
        self.container    = container
        self.agent_type   = agent_type
        self.debug        = debug
    
    def __compile_php_module(self, temp_filepath):
        return read_file(temp_filepath, True)

    def __compile_java_module(self, temp_filepath):
        return read_file(temp_filepath, True)

    def __compile_cs_module(self, temp_filepath):
        return read_file(temp_filepath, True)

    def compile(self, temporal_dir, temp_filepath, force=False):
        if self.agent_type == "php":
            return self.__compile_php_module(temp_filepath)
        elif self.agent_type == "java":
            return self.__compile_java_module(temp_filepath)
        elif self.agent_type == "cs":
            return self.__compile_cs_module(temp_filepath)
        else:
            raise CoreException(f"can not compile agent_type: '{self.agent_type}'")

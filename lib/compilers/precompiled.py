from lib.common import read_file, file_exists
from lib.exception import CoreException


class Compiler:
    def __init__(self, container, agent_type, agent_version, debug):
        self.container     = container
        self.agent_type    = agent_type
        self.agent_version = agent_version
        self.debug         = debug

    def __compile_cs_module(self, module_path):
        if file_exists(f"{module_path}.dll"):
            return read_file(f"{module_path}.dll", True)
        elif file_exists(f"{module_path}.exe"):
            return read_file(f"{module_path}.exe", True)
        else:
            raise CoreException(f"can not find precompiled module (exe or dll): '{module_path}'")

    def compile(self, temporal_dir, module_path, force=False):
        if self.agent_type == "cs":
            return self.__compile_cs_module(module_path)
        else:
            raise CoreException(f"can not compile agent_type: '{self.agent_type}'")

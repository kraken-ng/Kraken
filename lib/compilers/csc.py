import os, re, shutil, subprocess, platform
from lib.common import read_file, file_exists
from lib.exception import CoreException


class Compiler:
    def __init__(self, container, agent_type, agent_version, debug):
        self.container     = container
        self.agent_type    = agent_type
        self.agent_version = agent_version
        self.debug         = debug
        self.compilers     = []
        self.get_net_compilers()
        
    def get_net_compilers(self):
        if platform.system() != "Windows":
            raise CoreException(f"Invalid OS: '{platform.system()}'. Windows is needed to use csc compiler")
        netpath = "C:\\Windows\\Microsoft.NET\\Framework64"
        for net_version in os.listdir(netpath):
            abs_net_version = f"{netpath}\\{net_version}"
            if not os.path.isdir(abs_net_version):
                continue
            
            m = re.match(r"v\d\.\d", net_version)
            if not m:
                continue
            
            self.compilers.append({
                "version" : net_version[1:],
                "path" : f"{abs_net_version}\\csc.exe"
            })
        return
    
    def __get_compiler_subversions(self, source_version):
        compiler_subversions = []
        for compiler in self.compilers:
            # Ex: cs4 -> [4.0, 4.5, 4.5.1, 4.5.2, 4.6, etc]
            if compiler["version"].startswith(source_version):
                compiler_subversions.append(compiler)
        return compiler_subversions

    def __get_compilers_for_source(self, source_name, command_name):
        # If source name has specific version try to get its compiler (ex: cs4.5)
        for compiler in self.compilers:
            compiler_version = compiler["version"]

            if source_name == f"{command_name}.cs{compiler_version}.cs":
                return [compiler]

        # If source name has global version try to get all subversions (ex: cs4 -> 4.*)
        source_version = source_name.replace(f"{command_name}.cs","")
        source_version = source_version.replace(f".cs","")
        return self.__get_compiler_subversions(source_version)
    
    def __compile_cs_module(self, temporal_dir, module_path):
        module_filename = os.path.basename(module_path)
        module_name = module_filename.split(".")[0]
        
        csc_compiler = self.__get_compilers_for_source(module_filename, module_name)
        if not csc_compiler:
            raise CoreException(f"can not find a compiler for module: '{module_path}'")
        csc_compiler = csc_compiler[0]

        # Copy module to temporal directory
        temp_filepath_source = f"{temporal_dir}\\{module_filename}"
        shutil.copy(module_path, temp_filepath_source)

        command = f"{csc_compiler['path']} /target:library /out:{temp_filepath_source}.dll {temp_filepath_source}"        
        proc = subprocess.run(command.split(), capture_output=True)
        if proc.returncode != 0:
            raise CoreException(f"compilation of module: '{module_path}' failed: \n{proc.stdout}\n{proc.stderr}")

        module_filepath_compiled = f"{temp_filepath_source}.dll"
        if not file_exists(module_filepath_compiled):
            raise CoreException(f"can not find compiled module: '{module_filepath_compiled}'")
        return read_file(module_filepath_compiled, True)

    def compile(self, temporal_dir, module_path, force=False):
        if self.agent_type == "cs":
            return self.__compile_cs_module(temporal_dir, module_path)
        else:
            raise CoreException(f"can not compile agent_type: '{self.agent_type}'")

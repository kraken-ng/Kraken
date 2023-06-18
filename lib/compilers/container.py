import os, shutil

from lib.common import write_file
from lib.exception import CoreException
from lib.docker import copy_from, copy_to
from lib.config import MODULE_CLASS_NAME


class Compiler:
    def __init__(self, container, agent_type, agent_version, debug):
        self.container     = container
        self.agent_type    = agent_type
        self.agent_version = agent_version
        self.debug         = debug
    
    def __compile_java_module(self, temporal_dir, module_filepath, force=False):
        try:
            module_filename = os.path.basename(module_filepath)
            module_name = module_filename.split(".")[0]
            
            temp_filename_source = f"{MODULE_CLASS_NAME}_{module_name}.java"
            temp_filename_class  = f"{MODULE_CLASS_NAME}_{module_name}.class"
            temp_filepath_source = f"{temporal_dir}/{temp_filename_source}"
            temp_filepath_class  = f"{temporal_dir}/{temp_filename_class}"

            # Copy module to temporal directory
            shutil.copy(module_filepath, temp_filepath_source)
            
            # When re-compilation is not necessary
            if not force:
                data = copy_from(self.container, f"/tmp/{temp_filename_class}", temp_filepath_class)
                if data != None:
                    return data

            copy_to(self.container, temp_filepath_source, f"/tmp/{temp_filename_source}")
            exit_code, output = self.container.exec_run(f"javac /tmp/{temp_filename_source}")
            if exit_code != 0:
                raise CoreException(f"compilation of module: '{temp_filepath_source}' failed: \n{output}")

            data = copy_from(self.container, f"/tmp/{temp_filename_class}", temp_filepath_class)

            write_file(temp_filepath_class, data, True)

            return data

        except CoreException as ce:
            raise ce
        except Exception as e:
            raise Exception(f"error on java template compilation '{e}'")

    def compile(self, temporal_dir, temp_filepath, force=False):
        if self.agent_type == "java":
            return self.__compile_java_module(temporal_dir, temp_filepath, force)
        else:
            raise CoreException(f"container compiler can't compile agent_type: '{self.agent_type}'")
    
    def recompile(self, temporal_dir, temp_filepath):
        return self.compile(temporal_dir, temp_filepath, True)

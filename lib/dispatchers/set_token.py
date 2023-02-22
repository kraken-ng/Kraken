import re

from lib.config import MODULE_CLASS_NAME, FAILED_RESPONSE_CODE, RE_IMPERSONATE_TOKEN
from lib.config import ACTION_LOAD, ACTION_INVOKE
from lib.common import write_file, get_current_time, bin2hex
from lib.common import pack_into_agent_response, parse_agent_response_data
from lib.exception import CoreException


class Dispatcher:
    def __init__(self, mode, httpclient, debug, agent_pwd, agent_version, agent_type,
                agent_token, temporal_dir):
        self.mode          = mode
        self.httpclient    = httpclient
        self.debug         = debug
        self.agent_pwd     = agent_pwd
        self.agent_version = agent_version
        self.agent_type    = agent_type
        self.agent_token   = agent_token
        self.temporal_dir  = temporal_dir

    def __debug_module_context(self, module_name, message):
        temporal_filepath = f"{self.temporal_dir}/{MODULE_CLASS_NAME}_{module_name}.vars"
        message = "[" + get_current_time() + "]\n" + message 
        write_file(temporal_filepath, message)
        return

    def dispatch_c2(self, action, module_name, module_data, module_args_raw, module_args_parsed, module_references):
        message = None
        
        # Load module or invoke it (depend of action code)
        if action == ACTION_LOAD:
            module_name_hex = bin2hex(module_name.encode())
            module_data_hex = bin2hex(module_data)
            
            submessage_data     = f"name={module_name_hex},content={module_data_hex}"
            submessage_data_hex = bin2hex(submessage_data.encode())
            message             = f"action={ACTION_LOAD},data={submessage_data_hex}"
            return self.httpclient.do_http_request(message)
        else:
            module_id       = module_name
            args_str_hex    = bin2hex(module_args_raw.encode())
            cwd_str_hex     = bin2hex(self.agent_pwd.encode())
            agent_token_hex = bin2hex(self.agent_token.get()[1].encode())
            module_refs_hex = bin2hex((",".join(module_references)).encode())
            
            submessage_data     = f"id={module_id},args={args_str_hex},cwd={cwd_str_hex},token={agent_token_hex},references={module_refs_hex}"
            submessage_data_hex = bin2hex(submessage_data.encode())
            message             = f"action={ACTION_INVOKE},data={submessage_data_hex}"
        
            # If debug, store message in temporal directory
            if self.debug:
                self.__debug_module_context(module_name, message)
        
            response = self.httpclient.do_http_request(message)

            status, message = parse_agent_response_data(response)
            if status == FAILED_RESPONSE_CODE:
                return response

            m = re.match(RE_IMPERSONATE_TOKEN, message)
            if ((not m) or (len(m.groups()) != 2)):
                return pack_into_agent_response(FAILED_RESPONSE_CODE, f"the following regex does not return any results: {RE_IMPERSONATE_TOKEN}")

            impersonate_user   = m.group(1)
            impersonated_token = m.group(2)

            self.agent_token.push(impersonate_user, impersonated_token)

            return response

    def dispatch_st(self, module_name, module_data, module_args_raw, module_args_parsed, module_references):
        module_name_hex    = bin2hex(f"{MODULE_CLASS_NAME}_{module_name}".encode())
        module_content_hex = bin2hex(module_data)
        module_args_hex    = bin2hex(module_args_raw.encode())
        module_cwd_hex     = bin2hex(self.agent_pwd.encode())
        agent_token_hex    = bin2hex(self.agent_token.get()[1].encode())
        module_refs_hex    = bin2hex((",".join(module_references)).encode())

        submessage_data     = f"name={module_name_hex},content={module_content_hex},args={module_args_hex},cwd={module_cwd_hex},token={agent_token_hex},references={module_refs_hex}"
        submessage_data_hex = bin2hex(submessage_data.encode())
        message             = f"action={ACTION_INVOKE},data={submessage_data_hex}"

        # If debug, store message in temporal directory
        if self.debug:
            self.__debug_module_context(module_name, message)
        
        response = self.httpclient.do_http_request(message)

        status, message = parse_agent_response_data(response)
        if status == FAILED_RESPONSE_CODE:
            return response

        m = re.match(RE_IMPERSONATE_TOKEN, message)
        if ((not m) or (len(m.groups()) != 2)):
            return pack_into_agent_response(FAILED_RESPONSE_CODE, f"the following regex does not return any results: {RE_IMPERSONATE_TOKEN}")

        impersonate_user   = m.group(1)
        impersonated_token = m.group(2)

        self.agent_token.push(impersonate_user, impersonated_token)

        return response

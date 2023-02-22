import os, shlex, time

from lib.config import MODULE_CLASS_NAME, CUSTOM_SEPARATOR
from lib.config import SUCCESS_RESPONSE_CODE, FAILED_RESPONSE_CODE
from lib.config import ACTION_LOAD, ACTION_INVOKE
from lib.common import write_file, append_to_file, get_current_time, calculate_checksum
from lib.common import bin2hex, hex2bin
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
            remote_file = module_args_parsed.remote_file[0]
            local_file = module_args_parsed.local_file[0]
            chunk_size = module_args_parsed.c[0]
            seek = module_args_parsed.s[0]
            delay = module_args_parsed.d[0]
            quiet = module_args_parsed.q

            if seek == 0 and os.path.exists(local_file):
                raise CoreException(f"Invalid arguments: '{local_file}', file exists on filesystem")

            downloading = True
            remote_file_checksum = ""
            while downloading:
                packed_args = [remote_file, str(chunk_size), str(seek)]
                packed_args_joined = shlex.join(packed_args)

                module_id       = module_name
                args_str_hex    = bin2hex(packed_args_joined.encode())
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

                if CUSTOM_SEPARATOR not in message:
                    return pack_into_agent_response(FAILED_RESPONSE_CODE, "Invalid download data, CUSTOM_SEPARATOR not found in response")

                chunk_data_hex, checksum_data_hex = message.split(CUSTOM_SEPARATOR)
                chunk_data = hex2bin(chunk_data_hex)
                checksum_data = hex2bin(checksum_data_hex).decode()

                append_to_file(local_file, chunk_data, True)

                seek += len(chunk_data)
                if checksum_data != "":
                    downloading = False
                    remote_file_checksum = checksum_data
                
                if not quiet:
                    print(f"[+] Downloaded chunk on seek: {str(seek)}")
                
                time.sleep(delay)

            message = ""
            status = SUCCESS_RESPONSE_CODE
            local_file_checksum = calculate_checksum(local_file)
            if local_file_checksum == remote_file_checksum:
                message = f"[*] Remote File '{remote_file}' downloaded into '{local_file}' (checksum: {remote_file_checksum})\n"
                status = SUCCESS_RESPONSE_CODE
            else:
                message = f"Bad checksums: {local_file_checksum}({local_file}) != {remote_file_checksum}({remote_file})\n"
                status = FAILED_RESPONSE_CODE
            return pack_into_agent_response(status, message)


    def dispatch_st(self, module_name, module_data, module_args_raw, module_args_parsed, module_references):
        remote_file = module_args_parsed.remote_file[0]
        local_file = module_args_parsed.local_file[0]
        chunk_size = module_args_parsed.c[0]
        seek = module_args_parsed.s[0]
        delay = module_args_parsed.d[0]
        quiet = module_args_parsed.q

        if seek == 0 and os.path.exists(local_file):
            raise CoreException(f"Invalid arguments: '{local_file}', file exists on filesystem")

        downloading = True
        remote_file_checksum = ""
        while downloading:
            packed_args = [remote_file, str(chunk_size), str(seek)]
            packed_args_joined = shlex.join(packed_args)

            module_name_hex    = bin2hex(f"{MODULE_CLASS_NAME}_{module_name}".encode())
            module_content_hex = bin2hex(module_data)
            module_args_hex    = bin2hex(packed_args_joined.encode())
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

            if CUSTOM_SEPARATOR not in message:
                return pack_into_agent_response(FAILED_RESPONSE_CODE, "Invalid download data, CUSTOM_SEPARATOR not found in response")

            chunk_data_hex, checksum_data_hex = message.split(CUSTOM_SEPARATOR)
            chunk_data = hex2bin(chunk_data_hex)
            checksum_data = hex2bin(checksum_data_hex).decode()

            append_to_file(local_file, chunk_data, True)

            seek += len(chunk_data)
            if checksum_data != "":
                downloading = False
                remote_file_checksum = checksum_data
            
            if not quiet:
                print(f"[+] Downloaded chunk on seek: {str(seek)}")
            
            time.sleep(delay)

        message = ""
        status = SUCCESS_RESPONSE_CODE
        local_file_checksum = calculate_checksum(local_file)
        if local_file_checksum == remote_file_checksum:
            message = f"[*] Remote File '{remote_file}' downloaded into '{local_file}' (checksum: {remote_file_checksum})\n"
            status = SUCCESS_RESPONSE_CODE
        else:
            message = f"Bad checksums: {local_file_checksum}({local_file}) != {remote_file_checksum}({remote_file})\n"
            status = FAILED_RESPONSE_CODE

        return pack_into_agent_response(status, message)

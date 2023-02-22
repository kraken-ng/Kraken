import os, json, jsonschema, validators, binascii, uuid, hashlib, ipaddress, gzip, shutil, math
from itertools import cycle
from datetime import datetime

from lib.config import FIELD_SEPARATOR, VALUE_SEPARATOR
from lib.config import MODULES_PATH, TEMPORAL_PATH, DATETIME_FORMAT
from lib.exception import CoreException


def is_url(url):
    '''
    Checks that a URL is valid.

    Args:
        url: String representing a URL.

    Returns:
        bool: True when url is valid, False otherwise.

    Raises:
        None.
    '''
    try:
        validators.url(url)
    except Exception:
        return False
    return True

def file_exists(filepath):
    return os.path.exists(filepath)

def read_file(filepath, binary=False):
    with open(filepath, "rb" if binary else "r") as fd:
        return fd.read()

def write_file(filepath, data, binary=False):
    with open(filepath, "wb" if binary else "w") as fd:
        fd.write(data)

def append_to_file(filepath, data, binary=False):
    with open(filepath, "ab" if binary else "a") as fd:
        fd.write(data)

def read_chunk_file(filepath, chunk_size, seek, binary=False):
    with open(filepath, "rb" if binary else "r") as fd:
        fd.seek(seek)
        return fd.read(chunk_size)

def validate_json(jsonData, jsonSchema):
    '''
    Checks that the structure of a json dictionary matches a schema.

    Args:
        jsonData: JSON dictionary.
        jsonSchema: JSON Schema dictionary.

    Returns:
        bool: True when json data matches with the Schema, False otherwise.

    Raises:
        None.
    '''
    try:
        jsonschema.validate(instance=jsonData, schema=jsonSchema)
    except jsonschema.exceptions.ValidationError:
        return False
    return True

def is_json(data):
    try:
        json.loads(data)
    except ValueError as e:
        return False
    return True

def read_json_file(filepath):
    with open(filepath, "r") as fd:
        return json.load(fd)

def hex2bin(data):
    if not isinstance(data, str):
        raise Exception("hex2bin() invalid data supplied, expected str")
    data_low = data.lower()
    bin_data = binascii.unhexlify(data_low)
    return bin_data

def bin2hex(data):
    if not isinstance(data, bytes):
        raise Exception("bin2hex() invalid data supplied, expected bytes")
    data_hex = binascii.hexlify(data)
    return data_hex.decode()

def xorencrypt(data, key):
    return bytes(a ^ b for a, b in zip(data, cycle(key)))

def protect(data, key):
    try:
        compressed = gzip.compress(data.encode())
        crypt_data_raw = xorencrypt(compressed, key.encode())
        crypt_data_str = bin2hex(crypt_data_raw)
        return crypt_data_str
    except Exception as e:
        raise Exception(f"protect(): {str(e)}")

def unprotect(data, key):
    try:
        raw_data_hex = hex2bin(data)
        raw_data_decrypt = xorencrypt(raw_data_hex, key.encode())
        uncompressed = gzip.decompress(raw_data_decrypt)
        return uncompressed.decode()
    except Exception as e:
        raise Exception(f"unprotect(): {str(e)}")

def unpack_fields(data):
    results = {}
    fields = data.split(FIELD_SEPARATOR)
    if len(fields) == 0:
        return
    for field in fields:
        values = field.split(VALUE_SEPARATOR)
        if len(values) != 2:
            return
        results[values[0]] = values[1]
    return results

def generate_random_str():
    return str(uuid.uuid4())

def parse_agent_response_data(response):
    response_fields = unpack_fields(response)
    if response_fields == None:
        raise Exception("Invalid agent response, no fields extracted")
    response_status = response_fields.get("status")
    if response_status == None:
        raise Exception("Invalid agent response, 'status' field not found")
    response_message_hex = response_fields.get("message")
    if response_message_hex == None:
        raise Exception("Invalid agent response, 'message' field not found")
    if not response_status.isnumeric():
        raise Exception("Invalid 'status' field in response agent")
    response_message_str = hex2bin(response_message_hex)
    if response_message_str == None:
        raise Exception("Invalid 'message' field in response agent")
    return response_status, response_message_str.decode('ascii', 'ignore')

def pack_into_agent_response(status, message):
    return f"status{VALUE_SEPARATOR}{status}{FIELD_SEPARATOR}message{VALUE_SEPARATOR}{bin2hex(message.encode())}"

def calculate_checksum(filepath):
    md5_object = hashlib.md5()
    block_size = 128 * md5_object.block_size
    a_file = open(filepath, 'rb')
    chunk = a_file.read(block_size)
    while chunk:
        md5_object.update(chunk)
        chunk = a_file.read(block_size)
    a_file.close()
    md5_hash = md5_object.hexdigest()
    return md5_hash

def is_ipaddress(data):
    try:
        ipaddress.ip_network(data, False)
    except:
        return False
    return True

def timestamp_to_date(timestamp):
    datetime_obj = datetime.fromtimestamp(timestamp)
    return datetime_obj.strftime(DATETIME_FORMAT)

def find_module(module_name, agent_version, agent_type):
    version = agent_version.split(".")
    for i in reversed(range(1,len(version)+1)):
        rvlookup = '.'.join(version[:i])
        module_filename = f"{module_name}.{agent_type}{rvlookup}.{agent_type}"
        module_path = f"{MODULES_PATH}/{module_name}/{module_filename}"
        if os.path.exists(module_path):
            return module_path
    return

def create_temporal_directory():
    random_filepath = generate_random_str()
    random_temp_filepath = f"{TEMPORAL_PATH}/{random_filepath}"
    os.mkdir(random_temp_filepath)
    return os.path.abspath(random_temp_filepath)

def get_current_time():
    now = datetime.now()
    current_time = now.strftime(DATETIME_FORMAT)
    return current_time

def remove_temporal_directory(temp_dir):
    try:
        shutil.rmtree(temp_dir)
    except OSError:
        raise CoreException(f"error deleting temporal directory: '{temp_dir}'")

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0 B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return f"{s} {size_name[i]}"

import requests, json, re
from urllib3.exceptions import InsecureRequestWarning

from lib.config import PROFILE_SCHEMA
from lib.config import SUPPORTED_HTTP_METHODS, SUPPORTED_HTTP_ENCAPSULATE_TYPES
from lib.config import HTTP_MAX_HTTP_HEADER_LEN, HTTP_MAX_HTTP_PARAM_LEN
from lib.config import HTTP_RESPONSE_SUCC, HTTP_AGENT_INVALID_METHOD, HTTP_AGENT_INVALID_AUTH
from lib.common import file_exists, read_file, validate_json, is_url, is_json, protect, unprotect
from lib.exception import CoreException

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class HTTPClient:
    def __init__(self, profile):
        self.url      = None
        self.skip_ssl = None
        self.method   = None
        self.headers  = None
        self.cookies  = None
        self.fields   = None
        self.secret   = None
        self.data     = None
        self.response = None
        self.session  = requests.Session()
        self.__parse_profile(profile)

    def __repr__(self):
        return f"{type(self).__name__}()"

    def __str__(self):
        objstr  = f"Url: {self.url}\n"
        objstr += f"Method: {self.method}\n"
        objstr += f"Headers: {json.dumps(self.headers)}\n"
        objstr += f"Cookies: {json.dumps(self.cookies)}\n"
        objstr += f"Fields: {json.dumps(self.fields)}\n"
        objstr += f"Secret: {json.dumps(self.secret)}\n"
        objstr += f"Data: {json.dumps(self.data)}\n"
        objstr += f"Response: {json.dumps(self.response)}\n"
        return objstr

    def __read_profile(self, filepath):
        '''
        Reads and processes a local json file, which contains the information structure of a Kraken connection profile.
        The information is validated using the Connection Profile Schema. In this way, it ensures that the data is as 
        expected. In case of a mismatch, an exception is thrown.

        Args:
            filepath: Local path of the JSON file corresponding to the connection profile to be used.

        Returns:
            A dict mapping keys according to the schema of a connection profile.

        Raises:
            CoreException: An Exception thrown when a problem occurs with data processing.
        '''
        if not file_exists(filepath):
            raise CoreException(f"file '{filepath}' not exists in filesystem")
        file_data = read_file(filepath)
        if not is_json(file_data):
            raise CoreException(f"file '{filepath}' is not a valid json file")
        json_data = json.loads(file_data)
        if not validate_json(json_data, PROFILE_SCHEMA):
            raise CoreException(f"file '{filepath}' does not match the json profile shema")
        return json_data

    def __validate_http_dict_values(self, http_dict_values):
        '''
        Validates that the keys and values of a dictionary corresponding to the HTTP fields to be encapsulated in the 
        communication with the agent are valid.

        Args:
            http_dict_values: A dict mapping keys corresponding to the HTTP fields.

        Returns:
            None.

        Raises:
            CoreException: An Exception thrown when a problem occurs with data processing.
        '''
        for http_dict_key, http_dict_value in http_dict_values.items():
            if not isinstance(http_dict_key, str):
                raise CoreException(profile_header_key)
            if not isinstance(http_dict_value, str):
                raise CoreException(http_dict_value)
        return

    def __validate_http_dict_overlapping(self, http_dict_values, headers, cookies, fields):
        '''
        Check that there is no overlapping between the keys used to encapsulate data or secrets with headers,
        cookies and fields.

        Args:
            http_dict_values: A dict mapping keys corresponding to the HTTP fields (secrets or data).
            headers: A dict mapping keys of HTTP Headers.
            cookies: A dict mapping keys of HTTP Cookies.
            fields: A dict mapping keys of HTTP Fields.

        Returns:
            None.

        Raises:
            CoreException: An Exception thrown when a problem occurs with data processing.
        '''
        if (http_dict_values["type"] == "HEADER") and (http_dict_values["key"] in headers.keys()): 
            raise CoreException(http_dict_values["key"])
        if (http_dict_values["type"] == "COOKIE") and (http_dict_values["key"] in cookies.keys()): 
            raise CoreException(http_dict_values["key"])
        if (http_dict_values["type"] == "FIELD") and (http_dict_values["key"] in fields.keys()): 
            raise CoreException(http_dict_values["key"])
        return

    def __validate_profile(self, profile_data):
        '''
        Check that all fields of the connection profile are correct according to the expected keys and values.
        Exceptionally, it is also checked that encapsulation fields (secrets and data) do not overlap with headers,
        cookies or fields.

        Args:
            http_dict_values: A dict mapping keys corresponding to the Connection Profile data.

        Returns:
            None.

        Raises:
            CoreException: An Exception thrown when a problem occurs with data processing.
        '''
        if not is_url(profile_data["client"]["url"]):
            raise CoreException(f"profile url '" + profile_data["client"]["url"] + "' is not a valid url")
        if not isinstance(profile_data["client"]["skip_ssl"], bool):
            raise CoreException(f"profile skip_ssl '" + profile_data["client"]["skip_ssl"] + "' is not valid")
        if profile_data["client"]["method"] not in SUPPORTED_HTTP_METHODS:
            raise CoreException(f"profile method '" + profile_data["client"]["method"] + "' not supported or invalid http method")
        
        try:
            self.__validate_http_dict_values(profile_data["client"]["headers"])
        except CoreException as ce:
            raise CoreException(f"profile header '{str(ce)}' is invalid")
        try:
            self.__validate_http_dict_values(profile_data["client"]["cookies"])
        except CoreException as ce:
            raise CoreException(f"profile cookie '{str(ce)}' is invalid")        
        try:
            self.__validate_http_dict_values(profile_data["client"]["fields"])
        except CoreException as ce:
            raise CoreException(f"profile field '{str(ce)}' is invalid")
        
        if profile_data["client"]["message"]["secret"]["type"] not in SUPPORTED_HTTP_ENCAPSULATE_TYPES:
            raise CoreException(f"profile secret type '" + profile_data["client"]["message"]["secret"]["type"] + "' not supported or invalid type")
        
        try:
            self.__validate_http_dict_overlapping(
                profile_data["client"]["message"]["secret"],
                profile_data["client"]["headers"],
                profile_data["client"]["cookies"],
                profile_data["client"]["fields"]
            )
        except CoreException as ce:
            raise CoreException(f"profile secret: '{str(ce)}' is overlapping") 
        
        if profile_data["client"]["message"]["data"]["type"] not in SUPPORTED_HTTP_ENCAPSULATE_TYPES:
            raise CoreException(f"profile data type: '" + profile_data["client"]["message"]["data"]["type"] + "' not supported or invalid type")
        
        try:
            self.__validate_http_dict_overlapping(
                profile_data["client"]["message"]["data"],
                profile_data["client"]["headers"],
                profile_data["client"]["cookies"],
                profile_data["client"]["fields"]
            )
        except CoreException as e:
            raise CoreException(f"profile data: '{str(ce)}' is overlapping") 
        
        if profile_data["server"]["type"] not in SUPPORTED_HTTP_ENCAPSULATE_TYPES:
            raise CoreException(f"profile server type: '" + profile_data["server"]["type"] + "' not supported or invalid type")
        return

    def __extract_profile_values(self, profile_data):
        '''
        Sets the Kraken Client attributes from the processed connection profile data.

        Args:
            http_dict_values: A dict mapping keys corresponding to the Connection Profile data.

        Returns:
            None.

        Raises:
            None.
        '''
        self.url      = profile_data["client"]["url"]
        self.skip_ssl = profile_data["client"]["skip_ssl"]
        self.method   = profile_data["client"]["method"]
        self.headers  = profile_data["client"]["headers"]
        self.cookies  = profile_data["client"]["cookies"]
        self.fields   = profile_data["client"]["fields"]
        self.secret   = profile_data["client"]["message"]["secret"]
        self.data     = profile_data["client"]["message"]["data"]
        self.response = profile_data["server"]
        return

    def __parse_profile(self, filepath):
        '''
        It reads, processes, validates and extracts the connection profile data to be used and sets it in the Kraken Client.

        Args:
            filepath: Local path of the JSON file corresponding to the connection profile to be used.

        Returns:
            None.

        Raises:
            CoreException: An Exception thrown when a problem occurs with data processing.       
        '''
        profile_data = self.__read_profile(filepath)
        self.__validate_profile(profile_data)
        self.__extract_profile_values(profile_data)
        return

    def __pack_http_dict_with_value(self, http_dict, http_value):
        '''
        It packages the data and secrets to be sent in their corresponding HTTP fields.

        Args:
            http_dict: Dictionary with the name and type of the key on which the value is to be packaged.
            http_value: Content to be packaged as value.

        Returns:
            None.

        Raises:
            None.
        '''
        if http_dict["type"] == "HEADER":
            self.headers[http_dict["key"]] = http_value
        elif http_dict["type"] == "COOKIE":
            self.cookies[http_dict["key"]] = http_value
        elif http_dict["type"] == "FIELD":
            self.fields[http_dict["key"]] = http_value
        return

    def __check_agent_data_size(self, agent_data):
        '''
        Checks that the data sent to the agent does not exceed the maximum size supported by the chosen encapsulation field.
        URI Encapsulation allows: 8192 ~ 8kb (otherwise 414 URI Too Long) Apache Default
        Header Encapsulation allows: 8192 ~ 8kb (otherwise 413 Entity Too Large) Apache Default

        Args:
            agent_data: String which contains protected Agent Data to be encapsulated into HTTP Request.

        Returns:
            None.

        Raises:
            CoreException: An Exception thrown when a problem occurs with data processing.       
        '''
        agent_data_len = len(agent_data)
        if (self.data["type"] == "HEADER" or self.data["type"] == "COOKIE") and agent_data_len > HTTP_MAX_HTTP_HEADER_LEN:
            raise CoreException(f"agent data len: '{agent_data_len}' exceeds the maximum available in the HTTP HEADER/COOKIE: '{HTTP_MAX_HTTP_HEADER_LEN}'")
        if self.data["type"] == "FIELD" and self.method == "GET" and agent_data_len > HTTP_MAX_HTTP_PARAM_LEN:
            raise CoreException(f"agent data len: '{agent_data_len}' exceeds the maximum available in the HTTP FIELD: '{HTTP_MAX_HTTP_PARAM_LEN}'")
        return

    def __make_http_request(self, agent_data):
        '''
        Communicates with the Agent indicating the action to be taken and the necessary information for the same.
        It first protects the content of the message that the Agent will receive (using a password and the default
        encryption algorithm). It then checks the size of the generated data and encapsulates it in the HTTP fields
        according to the connection profile used. Finally, it performs the HTTP request and obtains a response. 
        In case of failure, it will throw an exception.

        Args:
            agent_data: String which contains raw Agent Data to be encapsulated into HTTP Request.

        Returns:
            requests.Response: HTTP Response returned by Agent.

        Raises:
            CoreException: An Exception thrown when a problem occurs with data processing.       
        '''
        protected_agent_data = protect(agent_data, self.secret["value"])
        self.__check_agent_data_size(protected_agent_data)

        self.__pack_http_dict_with_value(self.secret, self.secret["value"])
        self.__pack_http_dict_with_value(self.data, protected_agent_data)        
        try:
            if self.method == "GET":
                response = self.session.get(
                    self.url,
                    headers=self.headers,
                    cookies=self.cookies,
                    params=self.fields,
                    verify=self.skip_ssl)
            elif self.method == "POST":
                response = self.session.post(
                    self.url,
                    headers=self.headers,
                    cookies=self.cookies,
                    data=self.fields,
                    verify=self.skip_ssl)
        except requests.exceptions.RequestException:
            raise CoreException(f"can not connect to url: '{self.url}'")
        return response

    def __parse_response(self, response):
        '''
        Validates, processes and extracts the information sent by the Agent in the HTTP response obtained after
        the request. The extraction of the encapsulated data is performed according to the information of the 
        connection profile, in case of mismatch or error, an exception will be thrown.

        Args:
            response: HTTP Response Object (requests) from Agent.

        Returns:
            str: Response Raw Data from Agent extracted from HTTP Response.

        Raises:
            CoreException: An Exception thrown when a problem occurs with data processing.       
        '''
        if response.status_code != HTTP_RESPONSE_SUCC:
            if response.status_code == HTTP_AGENT_INVALID_METHOD:
                raise CoreException(f"response status code {response.status_code} != {HTTP_RESPONSE_SUCC} expected. Check Request Method of Connection Profile." + "\n" + response.text)
            elif response.status_code == HTTP_AGENT_INVALID_AUTH:
                raise CoreException(f"response status code {response.status_code} != {HTTP_RESPONSE_SUCC} expected. Check Authentication Key of Connnection Profile." + "\n" + response.text)
            else:
                raise CoreException(f"response status code {response.status_code} != {HTTP_RESPONSE_SUCC} expected." + "\n" + response.text)
        
        if self.response["type"] == "HEADER":
            if self.response["key"] not in response.headers.keys():
                raise CoreException(f"response has not data header: '" + self.response["key"] + "'")
            return response.headers[self.response["key"]]
        elif self.response["type"] == "COOKIE":
            if self.response["key"] not in response.cookies.keys():
                raise CoreException(f"response has not data cookie: '" + self.response["key"] + "'")
            return response.cookies[self.response["key"]] 
        elif self.response["type"] == "FIELD":
            m = re.match(self.response["key"] + "\=([A-Fa-f0-9]+)", response.text)
            if ((not m) or (len(m.groups()) != 1)):
                raise CoreException(f"response has not data field: '" + self.response["key"] + "'" + "\n" + response.text)
            return m.group(1)

    def do_http_request(self, agent_data):
        '''
        Sends the client data to the Agent encapsulating in the format indicated in the connection profile.
        It also extracts the agent data from the HTTP response.

        Args:
            agent_data: Core message fields to be encapsulated in the HTTP request (action and/or data).

        Returns:
            str: Response Raw Data from Agent.

        Raises:
            CoreException: An Exception thrown when a problem occurs with data processing.       
        '''
        #print(agent_data)
        response = self.__make_http_request(agent_data)
        #print("rtxt: '" + response.text + "'")
        response_data = self.__parse_response(response)
        return unprotect(response_data, self.secret["value"])
        
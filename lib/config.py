# Kraken modes
MODE_STANDARD                    = "st"
MODE_C2                          = "c2"

# Action codes
ACTION_STATUS                    = "0"
ACTION_INVOKE                    = "1"
ACTION_LOAD                      = "2"
ACTION_UNLOAD                    = "3"
ACTION_CLEAN                     = "4"

# Response codes
SUCCESS_RESPONSE_CODE            = "0"
FAILED_RESPONSE_CODE             = "1"

# Core Commands
COMMAND_EXIT                     = "exit"
COMMAND_HELP                     = "help"
COMMAND_CHANGE_DIRECTORY         = "cd"
COMMAND_REV2SELF                 = "rev2self"
COMMAND_CLOSE_TOKEN              = "close_token"
COMMAND_RECOMPILE                = "recompile"

# Exclusive C2 Commands
C2_COMMAND_LIST_MODULES          = "list_modules"
C2_COMMAND_LOAD_MODULE           = "load_module"
C2_COMMAND_UNLOAD_MODULE         = "unload_module"
C2_COMMAND_REFRESH_MODULES       = "refresh_modules"
C2_COMMAND_CLEAN_MODULES         = "clean_modules"

# Configuration values for the HTTP client
HTTP_RESPONSE_SUCC               = 200
HTTP_MAX_HTTP_PARAM_LEN          = 8192
HTTP_MAX_HTTP_HEADER_LEN         = 8192
SUPPORTED_HTTP_METHODS           = ["GET", "POST"]
SUPPORTED_HTTP_ENCAPSULATE_TYPES = ["HEADER", "COOKIE", "FIELD"]
HTTP_AGENT_INVALID_METHOD        = 400
HTTP_AGENT_INVALID_AUTH          = 500

# Separators availables
FIELD_SEPARATOR                  = ","
VALUE_SEPARATOR                  = "="
CUSTOM_SEPARATOR                 = "|"

# Configuration values for paths
CLIENTS_PATH                     = "clients"
HISTORY_PATH                     = "logs"
MODULES_PATH                     = "modules"
TEMPORAL_PATH                    = "temp"
COMPILERS_PATH                   = "compilers"
DISPATCHERS_PATH                 = "dispatchers"
FORMATERS_PATH                   = "formaters"
AGENTS_PATH                      = "agents"
ENVS_PATH                        = "envs"
UTILS_PATH                       = "utils"

# Other configuration values
DEFAULT_EMPTY_EXECUTOR           = "-"
DEFAULT_TOKEN_VALUE              = "0"
RE_IMPERSONATE_TOKEN             = r"Impersonated\suser:\s'(.*?)'\swith\stoken:\s'(\d+)'"
DATETIME_FORMAT                  = "%Y/%m/%d %H:%M:%S"
MODULE_CLASS_NAME                = "Module"
ALL_MODULES                      = "all"
AVAILABLE_SO_AGENTS              = ["Linux", "Windows"]
AVAILABLE_TYPE_AGENTS            = ["php", "java", "cs"]
AVAILABLE_COMPILERS              = ["raw", "container", "precompiled", "csc"]

# Containers Configuration
CONTAINERS = {
    "java" : [
        {
            "version" : "1.6",
            "image" : "openjdk:6"
        },
        {
            "version" : "1.7",
            "image" : "openjdk:7"
        },
        {
            "version" : "1.8",
            "image" : "openjdk:8"
        },
        {
            "version" : "9",
            "image" : "openjdk:9"
        },
        {
            "version" : "10",
            "image" : "openjdk:10"
        },
        {
            "version" : "11",
            "image" : "openjdk:11"
        },
        {
            "version" : "12",
            "image" : "openjdk:12"
        },
        {
            "version" : "13",
            "image" : "openjdk:13"
        },
        {
            "version" : "14",
            "image" : "openjdk:14"
        },
        {
            "version" : "15",
            "image" : "openjdk:15"
        },
        {
            "version" : "16",
            "image" : "openjdk:16"
        },
        {
            "version" : "17",
            "image" : "openjdk:17"
        }
    ],
    "php" : [],
    "cs" : []
}

# JSON Schema for connection profile
PROFILE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "client": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string"
                },
                "method": {
                    "type": "string"
                },
                "headers": {
                    "type": "object"
                },
                "cookies": {
                    "type": "object"
                },
                "fields": {
                    "type": "object"
                },
                "message": {
                    "type": "object",
                    "properties": {
                        "secret": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "string"
                                },
                                "key": {
                                    "type": "string"
                                },
                                "value": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "type",
                                "key",
                                "value"
                            ]
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "string"
                                },
                                "key": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "type",
                                "key"
                            ]
                        }
                    },
                    "required": [
                        "secret",
                        "data"
                    ]
                }
            },
            "required": [
                "url",
                "method",
                "headers",
                "cookies",
                "fields",
                "message"
            ]
        },
        "server": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string"
                },
                "key": {
                    "type": "string"
                }
            },
            "required": [
                "type",
                "key"
            ]
        }
    },
    "required": [
        "client",
        "server"
    ]
}

# Core Commands Configuration
CORE_COMMANDS = [
    {
        "name" : "exit",
        "description" : "Ends the session with the agent",
        "author" : "@secu_x11",
        "examples" : [
            "exit"
        ],
        "so" : [
            {
                "name" : "Linux",
                "agents" : ["php","java"]
            },
            {
                "name" : "Windows",
                "agents" : ["php","java","cs"]
            }
        ],
        "args" : []
    },
    {
        "name" : "help",
        "description" : "Displays the available commands or information of a command passed as an argument",
        "author" : "@secu_x11",
        "examples" : [
            "help",
            "help ls"
        ],
        "so" : [
            {
                "name" : "Linux",
                "agents" : ["php","java"]
            },
            {
                "name" : "Windows",
                "agents" : ["php","java","cs"]
            }
        ],
        "args" : [
            {
                "module": {
                    "help": "Module to show helper",
                    "nargs" : 1,
                    "type":  str
                }
            }
        ]
    },
    {
        "name" : "rev2self",
        "description" : f"Revert back to the original security context (sets the token to {DEFAULT_TOKEN_VALUE})",
        "author" : "@secu_x11",
        "examples" : [
            "rev2self"
        ],
        "so" : [
            {
                "name" : "Windows",
                "agents" : ["cs"]
            }
        ],
        "args" : []
    },
    {
        "name" : "recompile",
        "description" : "Recompile one or multiple modules (use 'all' to recompile all modules)",
        "author" : "@secu_x11",
        "examples" : [
            "recompile ls",
            "recompile ls cat id ps",
            "recompile all"
        ],
        "so" : [
            {
                "name" : "Linux",
                "agents" : ["java"]
            },
            {
                "name" : "Windows",
                "agents" : ["java"]
            }
        ],
        "args" : [
            {
                "module": {
                    "help": "Module/s to recompile",
                    "nargs" : "*",
                    "type":  str
                }
            }
        ]
    }
]

# C2 Command configuration
C2_COMMANDS = [
    {
        "name" : "list_modules",
        "description" : "List modules loaded in the agent",
        "author" : "@secu_x11",
        "examples" : [
            "list_modules"
        ],
        "so" : [
            {
                "name" : "Linux",
                "agents" : ["php"]
            },
            {
                "name" : "Windows",
                "agents" : ["php"]
            }
        ],
        "args" : []
    },
    {
        "name" : "load_module",
        "description" : "Load a new agent module/s (use 'all' to load all available modules)",
        "author" : "@secu_x11",
        "examples" : [
            "load_module ls",
            "load_module ls cd cat id",
            "load_module all"
        ],
        "so" : [
            {
                "name" : "Linux",
                "agents" : ["php"]
            },
            {
                "name" : "Windows",
                "agents" : ["php"]
            }
        ],
        "args" : [
            {
                "module": {
                    "help": "Module/s to load",
                    "nargs" : "*",
                    "type":  str
                }
            }
        ]
    },
    {
        "name" : "unload_module",
        "description" : "Unload an existing agent module/s (use 'all' to unload all loaded modules)",
        "author" : "@secu_x11",
        "examples" : [
            "unload_module ls",
            "unload_module ls cd cat id",
            "unload_module all"
        ],
        "so" : [
            {
                "name" : "Linux",
                "agents" : ["php"]
            },
            {
                "name" : "Windows",
                "agents" : ["php"]
            }
        ],
        "args" : [
            {
                "module": {
                    "help": "Module/s to unload",
                    "nargs" : "*",
                    "type":  str
                }
            }
        ]
    },
    {
        "name" : "refresh_modules",
        "description" : "Refresh module status from agent (update agent's memory in use)",
        "author" : "@secu_x11",
        "examples" : [
            "refresh_modules"
        ],
        "so" : [
            {
                "name" : "Linux",
                "agents" : ["php"]
            },
            {
                "name" : "Windows",
                "agents" : ["php"]
            }
        ],
        "args" : []
    },
    {
        "name" : "clean_modules",
        "description" : "Unload all agent modules",
        "author" : "@secu_x11",
        "examples" : [
            "clean_modules"
        ],
        "so" : [
            {
                "name" : "Linux",
                "agents" : ["php"]
            },
            {
                "name" : "Windows",
                "agents" : ["php"]
            }
        ],
        "args" : []
    }
]

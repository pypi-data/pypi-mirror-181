# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from phishing_hunter.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    SCANNER = "/scanner"
    SCANNER_ADD = "/scanner/add"
    SCANNER_REMOVE = "/scanner/remove"
    HUNTING = "/hunting"
    OBSERVATION = "/observation"
    OBSERVATION_ADD = "/observation/add"
    OBSERVATION_REMOVE = "/observation/remove"
    NOTIFY = "/notify"
    APIKEYS = "/apikeys"
    USERS_INFO = "/users/info"
    APIKEY = "/apikey"
    APIKEY_CREATE = "/apikey/create"
    APIKEY_DELETE = "/apikey/delete"

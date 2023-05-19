CONFIGURATION_FILE = "conf/application.yaml"

license_definition_list = []


class Api:
    login = "/login"
    viewNetworkSettings = "/view-network-settings"
    editNetworkSettings = "/edit-network-settings"
    viewProxySettings = "/view-proxy-settings"
    editProxySettings = "/edit-proxy-settings"
    getInterface = "/get-interface"
    viewHostName = "/view-hostname"
    editHostName = "/edit-hostname"


class FlaskService:
    GET = "GET"
    POST = "POST"
    method_not_supported = "Method not supported!"
    service_api = "service_api"
    config_section = "FLASK"
    port = "port"
    enable_security = "enable_security"
    enable_cookie = "enable_cookie"


class Log:
    config_section = "LOG"


class SQLITE:
    port = "port"
    host = "host"
    config_section = "SQLITE"
    db = "db"
    username = "username"
    password = "password"


class PROXY:
    path = "path"
    config_section = "PROXY"


class ErrorMessages:
    failed = "failed"
    df_formation_error = "Failed to create DataFrame"
    FAILED_TO_LOAD_DATA = "Failed to Load Data"
    USER_NOT_FOUND = "User not found."
    INVALID_CRED = "Invalid Credentials"
    UNAUTHORIZED_USER = "Sorry you are Unauthorized"
    FAILED_TO_REGISTER = "Failed to Register"
    No_DATA = "Data Not Available"
    USER_NAME_EXISTS = "Username already exists, Please try with a different username"


class CommonKeys:
    KEY_STATUS = "status"
    KEY_MESSAGE = "message"
    KEY_FILENAME = "fileName"


class CommonValues:
    VALUE_SUCCESS = "success"
    VALUE_FAILED = "failed"
    VALUE_UNDEFINED = "undefined"
    VALUE_LOGIN_SUCCESS = "You are logged in successfully"
    VALUE_LOGIN_FAILED = "Email not configured. Please contact administrator"
    VALUE_TRUE = "True"
    VALUE_FALSE = "False"
    VALUE_NO_FILE_PRESENT = ""
    HEADER_CONTENT = "header_content"
    BODY_CONTENT = "body_content"
    HEADERS = "headers"
    LABEL = "label"
    KEY = "key"


class CommonStatusCodes:
    SUCCESS = 200
    NOT_FOUND = 404

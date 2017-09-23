import sys
from . import fx_file_utils

JAVAC_EXEC = fx_file_utils.get_javac_path()
JAVA_EXEC = fx_file_utils.get_java_path()

PYTHON_EXEC = sys.executable

LANGUAGE_JAVA = 'java'
LANGUAGE_PYTHON = 'python'
LANGUAGE_JAVASCRIPT = 'javascript'
LANGUAGE_PHP = 'php'
LANGUAGE_C_CPP = 'c_cpp'

SUPPORT_LANGUAGES = [
    LANGUAGE_JAVA,
    LANGUAGE_PYTHON,
    LANGUAGE_JAVASCRIPT,
    LANGUAGE_PHP,
    LANGUAGE_C_CPP
]

KEY_CODE = 'code'
KEY_OUTPUT = 'output'

KEY_CODE_ERROR = 'Error'
KEY_CODE_SUCCESS = 'Success'

# DEFAULT_PER_PAGE = 25

# set to 2 for testing now
DEFAULT_PER_PAGE = 2

import sys
from . import fx_file_utils

JAVAC_EXEC = fx_file_utils.get_javac_path()
JAVA_EXEC = fx_file_utils.get_java_path()

PYTHON_EXEC = sys.executable

LANGUAGE_JAVA = 'java'
LANGUAGE_PYTHON = 'python'
LANGUAGE_JAVASCRIPT = 'javascript'

SUPPORT_LANGUAGES = [
    LANGUAGE_JAVA,
    LANGUAGE_PYTHON,
    LANGUAGE_JAVASCRIPT
]


from . import fx_java_executor, fx_python_executor, fx_js_executor, fx_php_executor
from main.utils import fx_constants
from enum import Enum


class ExecutorLanguage(Enum):

    python = fx_constants.LANGUAGE_PYTHON
    java = fx_constants.LANGUAGE_JAVA
    java_script = fx_constants.LANGUAGE_JAVASCRIPT
    php = fx_constants.LANGUAGE_PHP


class FXExecutorFactory():

    @staticmethod
    def get_executor(language):
        executor = None
        if language:
            language = ExecutorLanguage(language)
            if language is ExecutorLanguage.python:
                executor = fx_python_executor.FXPythonExecutor()
            elif language is ExecutorLanguage.java:
                executor = fx_java_executor.FXJavaExecutor()
            elif language is ExecutorLanguage.java_script:
                executor = fx_js_executor.FXJSExecutor()
            elif language is ExecutorLanguage.php:
                executor = fx_php_executor.FXPHPExecutor()
        return executor
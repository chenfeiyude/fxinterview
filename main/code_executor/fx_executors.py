from . import fx_java_executor, fx_python_executor, fx_js_executor, fx_php_executor
from ..utils import fx_constants

FX_COMPILER = {
    fx_constants.LANGUAGE_PYTHON: fx_python_executor,
    fx_constants.LANGUAGE_JAVA: fx_java_executor,
    fx_constants.LANGUAGE_JAVASCRIPT: fx_js_executor,
    fx_constants.LANGUAGE_PHP: fx_php_executor
}

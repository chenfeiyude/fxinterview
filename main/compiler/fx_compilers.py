from . import fx_java_compiler, fx_python_compiler
from ..utils import fx_constants

FX_COMPILER = {
    fx_constants.LANGUAGE_PYTHON: fx_python_compiler,
    fx_constants.LANGUAGE_JAVA: fx_java_compiler
}

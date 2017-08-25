import js2py, logging
from ..utils import fx_constants

def run_code(code):
    result = dict()

    try:
        code.replace("document.write", "return ")
        out_data = js2py.eval_js(code)
    except Exception as e:
        # return error data
        result[fx_constants.KEY_CODE] = fx_constants.KEY_CODE_ERROR
        result[fx_constants.KEY_OUTPUT] = e
        return result
    else:
        # return success data
        result[fx_constants.KEY_OUTPUT] = out_data
        result[fx_constants.KEY_CODE] = fx_constants.KEY_CODE_SUCCESS
        return result
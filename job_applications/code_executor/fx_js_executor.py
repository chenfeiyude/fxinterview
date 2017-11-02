import js2py, logging
from main.utils import fx_constants
from .fx_common_executor import CommonExecutor


class FXJSExecutor(CommonExecutor):

    def run_code(self, code):
        result = dict()

        try:
            code.replace("document.write", "return ")
            out_data = js2py.eval_js(code)
            # return success data
            result[fx_constants.KEY_OUTPUT] = out_data
            result[fx_constants.KEY_CODE] = fx_constants.KEY_CODE_SUCCESS
            return result
        except Exception as e:
            # return error data
            result[fx_constants.KEY_CODE] = fx_constants.KEY_CODE_ERROR
            result[fx_constants.KEY_OUTPUT] = e
            return result

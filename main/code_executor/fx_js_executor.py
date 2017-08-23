import js2py, logging


def run_code(code):
    result = dict()

    try:
        code.replace("document.write", "return ")
        out_data = js2py.eval_js(code)
    except Exception as e:
        # return error data
        result["code"] = 'Error'
        result["output"] = e
        return result
    else:
        # return success data
        result['output'] = out_data
        result["code"] = "Success"
        return result
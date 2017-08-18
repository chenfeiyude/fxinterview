import os, sys, subprocess, tempfile, time
import logging
from ..utils import fx_file_utils, fx_string_utils

# file name
file_num = int(time.time() * 1000)

# python compiler
py_exec = sys.executable


# python version
def get_version():
    v = sys.version_info
    version = "python %s.%s" % (v.major, v.minor)
    return version


# python file name
def get_py_name():
    global file_num
    return 'test_%d' % file_num


def run_code(code):
    result = dict()
    result["version"] = get_version()
    py_name = get_py_name()
    file_path = fx_file_utils.write_py_file(fx_file_utils.make_temp_dir(), py_name, code)
    try:
        # subprocess.check_output waiting sub process, and return output results
        # stderr is type of standard output
        out_data = fx_string_utils.decode_utf_8(subprocess.check_output([py_exec, file_path], stderr=subprocess.STDOUT, timeout=5))
    except subprocess.CalledProcessError as e:
        # return error data
        result["code"] = 'Error'
        result["output"] = fx_string_utils.decode_utf_8(e.output)
        return result
    else:
        # return success data
        result['output'] = out_data
        result["code"] = "Success"
        return result
    finally:
        # delete temp file
        try:
            os.remove(file_path)
        except Exception as e:
            logging.error('Remove file failed: %s' % e)
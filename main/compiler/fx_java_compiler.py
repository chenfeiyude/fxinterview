import os, sys, subprocess, time
import logging
from ..utils import fx_file_utils, fx_string_utils, fx_constants

# file name
file_num = int(time.time() * 1000)
bash_file = '%s/main/compiler/test.sh'% os.getcwd()

# java file name
def get_file_name():
    global file_num
    return 'test_%d.java' % file_num


def run_code(code):
    result = dict()
    file_name = get_file_name()
    file_dir = fx_file_utils.make_temp_dir()
    file_path = fx_file_utils.write_file(file_dir, file_name, code)
    try:
        # subprocess.check_output waiting sub process, and return output results
        # stderr is type of standard output
        out_data = fx_string_utils.decode_utf_8(subprocess.check_output([fx_constants.JAVAC_EXEC, file_path], stderr=subprocess.STDOUT, timeout=5))
    except subprocess.CalledProcessError as e:
        # return error data
        result["code"] = 'Error'
        result["output"] = fx_string_utils.decode_utf_8(e.output)
        return result
    else:
        # out_data = fx_string_utils.decode_utf_8(subprocess.check_output([bash_file, file_dir, fx_constants.JAVA_EXEC, file_name],stderr=subprocess.STDOUT, timeout=5))
        out_data = fx_string_utils.decode_utf_8(subprocess.check_output([fx_constants.JAVA_EXEC, file_path], stderr=subprocess.STDOUT, timeout=5))

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
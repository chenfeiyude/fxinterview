import logging
import os
import subprocess
import sys
import time

from fx_tools.utils import fx_constants, fx_file_utils, fx_string_utils
from .fx_common_executor import CommonExecutor

# file name
file_num = int(time.time() * 1000)

class FXPythonExecutor(CommonExecutor):

    # python version
    @staticmethod
    def get_version():
        v = sys.version_info
        version = "python %s.%s" % (v.major, v.minor)
        return version


    # python file name
    @staticmethod
    def get_file_name():
        global file_num
        return 'test_%d.py' % file_num

    def run_code(self, code):
        result = dict()
        result["version"] = self.get_version()
        file_path = fx_file_utils.write_file(fx_file_utils.make_temp_dir(), self.get_file_name(), code)
        try:
            # subprocess.check_output waiting sub process, and return output results
            # stderr is type of standard output
            out_data = fx_string_utils.decode_utf_8(subprocess.check_output([fx_constants.PYTHON_EXEC, file_path], stderr=subprocess.STDOUT, timeout=5))
            # return success data
            result[fx_constants.KEY_OUTPUT] = out_data
            result[fx_constants.KEY_CODE] = fx_constants.KEY_CODE_SUCCESS
            return result
        except subprocess.CalledProcessError as e:
            # return error data
            logging.error(e.output)
            result[fx_constants.KEY_CODE] = fx_constants.KEY_CODE_ERROR
            result[fx_constants.KEY_OUTPUT] = fx_string_utils.decode_utf_8(e.output).split('py",')[1]
            return result
        finally:
            # delete temp file
            try:
                os.remove(file_path)
            except Exception as e:
                logging.error('Remove file failed: %s' % e)
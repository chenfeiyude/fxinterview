import os, sys, subprocess, time
import logging
from .fx_common_executor import CommonExecutor
from ..utils import fx_file_utils, fx_string_utils, fx_constants


class FXJavaExecutor(CommonExecutor):

    bash_file = '%s/main/code_executor/run_java.sh'% os.getcwd()

    # java file name
    @staticmethod
    def get_file_name(code):
        if code:
            if 'public class' in code and '{' in code:
                file_name = code.split('public class ')[1].split('{')[0].strip()
            else:
                file_name = "test"
            return '%s.java' % file_name

    def run_code(self, code):
        result = dict()
        file_name = self.get_file_name(code)
        file_dir = fx_file_utils.make_temp_dir()
        file_path = fx_file_utils.write_file(file_dir, file_name, code)
        try:
            # subprocess.check_output waiting sub process, and return output results
            # stderr is type of standard output
            out_data = fx_string_utils.decode_utf_8(subprocess.check_output([fx_constants.JAVAC_EXEC, file_path], stderr=subprocess.STDOUT, timeout=5))
            java_name = file_name.replace('.java', '')
            out_data = fx_string_utils.decode_utf_8(subprocess.check_output([self.bash_file, file_dir, fx_constants.JAVA_EXEC, java_name], stderr=subprocess.STDOUT,
                                        timeout=5))

            # return success data
            result[fx_constants.KEY_OUTPUT] = out_data
            result[fx_constants.KEY_CODE] = fx_constants.KEY_CODE_SUCCESS
            return result
        except subprocess.CalledProcessError as e:
            # return error data
            logging.error(e.output)
            result[fx_constants.KEY_CODE] = fx_constants.KEY_CODE_ERROR
            error_output = fx_string_utils.decode_utf_8(e.output)
            if '.java' in error_output:
                error_output = 'Line' + error_output.split('.java')[1]
            result[fx_constants.KEY_OUTPUT] = error_output
            return result
        finally:
            # delete temp file
            try:
                os.remove(file_path)
            except Exception as e:
                logging.error('Remove file failed: %s' % e)
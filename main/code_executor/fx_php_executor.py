import os, subprocess, time, logging
from ..utils import fx_file_utils, fx_string_utils, fx_constants

# file name
file_num = int(time.time() * 1000)


# python file name
def get_file_name():
    global file_num
    return 'test_%d.php' % file_num


def run_code(code):
    result = dict()
    file_path = fx_file_utils.write_file(fx_file_utils.make_temp_dir(), get_file_name(), code)
    try:
        # subprocess.check_output waiting sub process, and return output results
        # stderr is type of standard output
        out_data = fx_string_utils.decode_utf_8(subprocess.check_output(['php', file_path], stderr=subprocess.STDOUT, timeout=5))
    except subprocess.CalledProcessError as e:
        # return error data
        result[fx_constants.KEY_CODE] = fx_constants.KEY_CODE_ERROR
        result[fx_constants.KEY_OUTPUT] = fx_string_utils.decode_utf_8(e.output)
        return result
    else:
        # return success data
        result[fx_constants.KEY_OUTPUT] = out_data
        result[fx_constants.KEY_CODE] = fx_constants.KEY_CODE_SUCCESS
        return result
    finally:
        # delete temp file
        try:
            os.remove(file_path)
        except Exception as e:
            logging.error('Remove file failed: %s' % e)
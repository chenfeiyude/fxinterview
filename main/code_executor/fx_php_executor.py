import os, subprocess, time, logging
from ..utils import fx_file_utils, fx_string_utils

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
        # out_data = fx_string_utils.decode_utf_8(subprocess.check_output(['php', file_path], stderr=subprocess.STDOUT, timeout=5))

        proc = subprocess.Popen("php %s" % file_path, shell=True, stdout=subprocess.PIPE)
        out_data = proc.stdout.read()

        logging.info(out_data)
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
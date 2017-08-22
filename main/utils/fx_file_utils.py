import logging, os, tempfile, subprocess
from . import fx_string_utils


def make_temp_dir():
    temp_dir = tempfile.mkdtemp(suffix='_test', prefix='fx_interview_')
    return temp_dir


# get code and write into file
def write_file(file_dir, py_name, code):
    file_path = os.path.join(file_dir, py_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    logging.info('file path: %s' % file_path)
    return file_path


def get_java_path():
    java_path = fx_string_utils.decode_utf_8(subprocess.check_output(['whereis', 'java'])).replace('\n', '')
    return java_path


def get_javac_path():
    javac_path = fx_string_utils.decode_utf_8(subprocess.check_output(['whereis','javac'])).replace('\n', '')
    return javac_path
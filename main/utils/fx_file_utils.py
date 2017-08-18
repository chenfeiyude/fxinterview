import logging, os, tempfile


def make_temp_dir():
    temp_dir = tempfile.mkdtemp(suffix='_test', prefix='fx_python_')
    return temp_dir


# get code and write into file
def write_py_file(file_dir, py_name, code):
    file_path = os.path.join(file_dir, '%s.py' % py_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    logging.info('file path: %s' % file_path)
    return file_path
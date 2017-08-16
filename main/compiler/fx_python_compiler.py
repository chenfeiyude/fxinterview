import os, sys, subprocess, tempfile, time

# create temp file
TempFile = tempfile.mkdtemp(suffix='_test', prefix='python_')
# file name
FileNum = int(time.time() * 1000)
# python compiler
EXEC = sys.executable


# python version
def get_version():
    v = sys.version_info
    version = "python %s.%s" % (v.major, v.minor)
    return version


# python file name
def get_pyname():
    global FileNum
    return 'test_%d' % FileNum


# get code and write into file
def write_file(pyname, code):
    fpath = os.path.join(TempFile, '%s.py' % pyname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(code)
    print('file path: %s' % fpath)
    return fpath


# decode file
def decode(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return s.decode('gbk')


def main(code):
    r = dict()
    r["version"] = get_version()
    pyname = get_pyname()
    fpath = write_file(pyname, code)
    try:
        # subprocess.check_output waiting sub process, and return output results
        # stderr is type of standard output
        outdata = decode(subprocess.check_output([EXEC, fpath], stderr=subprocess.STDOUT, timeout=5))
    except subprocess.CalledProcessError as e:
        # return error data
        r["code"] = 'Error'
        r["output"] = decode(e.output)
        return r
    else:
        # return success data
        r['output'] = outdata
        r["code"] = "Success"
        return r
    finally:
        # delete temp file
        try:
            os.remove(fpath)
        except Exception as e:
            exit(1)
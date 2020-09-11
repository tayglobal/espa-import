import epimport as epi
from subprocess import Popen, PIPE
import pytest
import json


SRCDB = 'files://tmp/unittests/test_main'


@pytest.fixture
def remote_importer():
    ri = epi.RemoteImporter(SRCDB)
    return ri


def _run_test(args):
    command = ["python", "-m", "epimport.main", "--srcdb=" + SRCDB] + args
    with Popen(command, stdout=PIPE) as proc:
        output = proc.stdout.read()
    assert proc.returncode == 0
    return output


def test_main(remote_importer):
    remote_importer.add_script("unittest/main_module.py", '''
def main():
    print("Hello World")
''')
    assert _run_test(["unittest.main_module"]) == b'Hello World\n'


def test_entry(remote_importer):
    remote_importer.add_script("unittest/test_entry.py", '''
def test_entry():
    print("Welcome")
''')
    assert _run_test(
        ["unittest.test_entry", "--entry=test_entry"]) == b'Welcome\n'


def test_args(remote_importer):
    remote_importer.add_script("unittest/test_args.py", '''
def main(a, b, c=3):
    assert a == 1
    assert b == 2
    assert c == 3
''')

    args = {'a': 1, 'b': 2}
    _run_test(["unittest.test_args", '--args=' + json.dumps(args)])

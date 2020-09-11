import sys
import types
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec
import kydb


class RemoteFinder(MetaPathFinder):
    def __init__(self, db):
        self.db = db

    def find_spec(self, fullname, path, target=None):
        key = fullname.replace('.', '/') + '.py'
        if self.db.exists(key):
            return ModuleSpec(fullname, self, origin=key)

        key = fullname.replace('.', '/') + '/__init__.py'

        if self.db.exists(key):
            return ModuleSpec(fullname, self, origin=key)

    def create_module(self, spec):
        """
        Module creator.

        Returning None causes Python to use the default module creator.
        """
        name_parts = spec.name.split('.')
        module = types.ModuleType('.'.join(name_parts))
        module.__path__ = name_parts[:-1]
        module.__file__ = spec.origin
        return module

    def exec_module(self, module):
        code = self.db[module.__file__]['code']
        exec(code, module.__dict__)
        return module


class RemoteImporter:
    def __init__(self, url: str):
        self.url = url
        self.db = kydb.connect(url)

    def install(self):
        finder = RemoteFinder(self.db)
        sys.meta_path.append(finder)

    def add_script(self, key: str, script: str):
        self.db[key] = {
            'code': script
        }

    def add_script_from_file(self, key: str, filename: str):
        with open(filename, 'r') as f:
            self.add_script(key, f.read())


_remote_importer: RemoteImporter = None

def get_importer():
    global _remote_importer
    return _remote_importer
    
def set_srcdb(url: str):
    global _remote_importer
    _remote_importer = RemoteImporter(url)
    _remote_importer.install()


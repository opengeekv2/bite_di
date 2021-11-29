# content of conftest.py
import platform

collect_ignore = ["setup.py"]
if float('.'.join(platform.python_version_tuple[0:2])) >= 2.8:
    collect_ignore_glob = ["*_py2.8.py"]

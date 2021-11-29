# content of conftest.py
import platform

collect_ignore = ["setup.py"]
if float('.'.join(platform.python_version_tuple()[0:2])) < 3.8:
    collect_ignore_glob = ["*_py3.8.py"]

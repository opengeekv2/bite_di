# content of conftest.py
import platform

collect_ignore = ["setup.py"]
if (int(platform.python_version_tuple()[0]) >= 3 and
        int(platform.python_version_tuple()[1]) >= 8):
    collect_ignore_glob = ["*_py3.8.py"]

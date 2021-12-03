# content of conftest.py
import platform

collect_ignore = ["setup.py"]
if (int(platform.python_version_tuple()[0]) < 3 or
        int(platform.python_version_tuple()[1]) < 8):
    collect_ignore_glob = ["*_py38.py"]

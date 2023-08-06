# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dirlib']
setup_kwargs = {
    'name': 'dirlib',
    'version': '1.2.0',
    'description': '',
    'long_description': '# dirlib\n\n`dirlib` is a minimum library for getting a directory that is used by putting on configuration files. This is inspired by Golang standard library function called `os.UserConfigDir()`. Currently, Windows, Unix and macOS are supported.\n\n## Installation\n\n```\npip install dirlib\n```\n\n## How to use\n\n```python\nimport dirlib\n\n# On Windows\nprint(dirlib.user_config_dir()) #=> %AppData% or %UserProfile%\n\n# On Unix\nprint(dirlib.user_config_dir()) #=> $XDG_CONFIG_HOME or $HOME/.config\n\n# On macOS\nprint(dirlib.user_config_dir()) #=> $HOME/Libary/Application Support\n```\n\n`user_config_dir()` can pass the two arguments. The first one is an application name. Here is an example on Windows.\n\n```python\nimport dirlib\napp_name = "mysupercooltool"\nprint(dirlib.user_config_dir(app_name)) #=> C:\\Users\\chihiro\\AppData\\Roaming\\mysupercooltool\n```',
    'author': 'owlinux1000',
    'author_email': 'encry1024@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/owlinux1000/dirlib',
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

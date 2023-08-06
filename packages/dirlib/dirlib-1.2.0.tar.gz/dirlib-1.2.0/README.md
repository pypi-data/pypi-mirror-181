# dirlib

`dirlib` is a minimum library for getting a directory that is used by putting on configuration files. This is inspired by Golang standard library function called `os.UserConfigDir()`. Currently, Windows, Unix and macOS are supported.

## Installation

```
pip install dirlib
```

## How to use

```python
import dirlib

# On Windows
print(dirlib.user_config_dir()) #=> %AppData% or %UserProfile%

# On Unix
print(dirlib.user_config_dir()) #=> $XDG_CONFIG_HOME or $HOME/.config

# On macOS
print(dirlib.user_config_dir()) #=> $HOME/Libary/Application Support
```

`user_config_dir()` can pass the two arguments. The first one is an application name. Here is an example on Windows.

```python
import dirlib
app_name = "mysupercooltool"
print(dirlib.user_config_dir(app_name)) #=> C:\Users\chihiro\AppData\Roaming\mysupercooltool
```
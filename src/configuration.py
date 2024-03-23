"""
Parses configuration values from `assets/`.
"""

from printing import *

class Config:

    def __init__(self, config_path: str):
        self._mapping = dict()
        self._used = set()
        with open(config_path, 'r') as fin:
            print_log(__name__, f"Opened configuration file {config_path}.")
            lines = fin.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith('#'):
                    continue
                if ':' not in line:
                    print_error(__name__, f"Configuration syntax error in \"{line}\".")
                key, value = line.split(':')
                if key in self._mapping:
                    print_warning(__name__, f"Key \"{key}\" is already present in {config_path}.")
                self._mapping[key.strip()] = value.strip()
                print_log(__name__, f"Set key-value pair ({key.strip()}, {value.strip()}).")
    
    def get_str(self, key: str) -> str:
        if key not in self._mapping:
            print_error(__name__, f"Key \"{key}\" not found.")
        self._used.add(key)
        return self._mapping[key]
    
    def get_num(self, key: str) -> float:
        if key not in self._mapping:
            print_error(__name__, f"Key \"{key}\" not found.")
        else:
            value = self._mapping[key]
            if not value.isnumeric():
                print_error(__name__, f"Value \"{value}\" from key \"{key}\" is not numeric.")
        self._used.add(key)
        return float(self._mapping[key])

    def redundant(self) -> bool:
        return len(self._used) != len(self._mapping)

def is_enabled(s: str) -> bool:
    if s != "enabled" and s != "disabled":
        print_warning(__name__, f"Invalid boolean value \"{s}\". Falling back to disabled.")
    return s == "enabled"

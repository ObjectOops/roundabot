"""
Parses configuration values and paths from `assets/`.
"""

from printing import *

class Config:

    def __init__(self, config_path: str):
        self._mapping = dict()
        with open(config_path, 'r') as fin:
            print_log(__file__, f"Opened configuration file {config_path}.")
            lines = fin.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith("#"):
                    continue
                if ':' not in line:
                    print_error(__file__, f"Configuration syntax error in \"{line}\".")
                key, value = line.split(':')
                if key in self._mapping:
                    print_warning(__file__, f"Key \"{key}\" is already present in {config_path}.")
                self._mapping[key.strip()] = value.strip()
                print_log(__file__, f"Set key-value pair ({key.strip()}, {value.strip()}).")
    
    def get_str(self, key: str) -> str:
        if key not in self._mapping:
            print_error(__file__, f"Key \"{key}\" not found.")
        return self._mapping[key]
    
    def get_num(self, key: str) -> float:
        if key not in self._mapping:
            print_error(__file__, f"Key \"{key}\" not found.")
        else:
            value = self._mapping[key]
            if not value.isnumeric():
                print_error(__file__, f"Value \"{value}\" from key \"{key}\" is not numeric.")
        return float(self._mapping[key])

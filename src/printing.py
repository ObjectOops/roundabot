"""
Print logging utilities.
"""

def print_log(file_name: str, msg: str):
    print(f"[LOG] ({file_name}) {msg}")

def print_warning(file_name: str, msg: str):
    print(f"\033[38;5;214m[WARNING] ({file_name}) {msg}\033[m")

def print_error(file_name: str, msg: str):
    print(f"\033[38;5;196m[ERROR] ({file_name}) {msg}\033[m")

### utils/terminal.py
import os
from colorama import init

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def initialize_terminal():
    init(autoreset=True)

def restore_terminal():
    pass  # Placeholder for future enhancements
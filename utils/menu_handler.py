import re
import sys
import select
from colorama import Fore, Style

def display_menu():
    print(Fore.CYAN + "Select a category:")
    print(Fore.YELLOW + "1. OSINT")
    print(Fore.YELLOW + "2. Credentials")
    print(Fore.YELLOW + "3. Network")
    print(Fore.YELLOW + "4. Web")
    print(Fore.YELLOW + "5. Active Directory")
    print(Fore.YELLOW + "6. Cloud")
    print(Fore.YELLOW + "7. Databases")
    print(Fore.YELLOW + "8. Exploitation")
    print(Fore.YELLOW + "0. Automatic (Run all categories)")

    print(Fore.GREEN + "Select category (You have 10 seconds): " + Style.RESET_ALL, end="", flush=True)

    # Use select() to add a timeout
    ready, _, _ = select.select([sys.stdin], [], [], 10)  # 10-second timeout

    if ready:
        choice = sys.stdin.readline().strip()
        choice = re.sub(r'[\r\n\x00-\x1F\x7F]', '', choice)  # Remove control characters
        return int(choice) if choice.isdigit() else 1  # Default to 1 if invalid
    else:
        print("\nNo input detected. Defaulting to category 0 (Automatic).")
        return 0  # Default category if no input is given

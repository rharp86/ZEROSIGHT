import os
import re
import sys
import time
import logging
import csv
import queue
import random
import json
import subprocess
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style
import toml
from utils.dependency_checker import check_dependencies
from utils.matrix_rain import MatrixRain

# Initialize colorama for colored terminal text
init(autoreset=True)

# -------------------------------------------------------------------
# LOGGER CONFIGURATION
# -------------------------------------------------------------------
def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger

logger = setup_logger("ZeroSight")

# -------------------------------------------------------------------
# CONFIGURATION LOADER
# -------------------------------------------------------------------
def load_config(config_path: Path) -> Dict:
    if not config_path.exists():
        logger.error("Configuration file not found.")
        sys.exit(1)
    try:
        return toml.load(config_path)
    except Exception as e:
        logger.error(f"Failed to parse configuration: {e}")
        sys.exit(1)

# -------------------------------------------------------------------
# BANNER
# -------------------------------------------------------------------
def display_banner():
    os.system('clear')  # Clear the terminal screen
    banner = """\
███████╗███████╗██████╗  ██████╗ ███████╗██╗ ██████╗ ██╗  ██╗████████╗
╚══███╔╝██╔════╝██╔══██╗██╔═══██╗██╔════╝██║██╔════╝ ██║  ██║╚══██╔══╝
  ███╔╝ █████╗  ██████╔╝██║   ██║███████╗██║██║  ███╗███████║   ██║   
 ███╔╝  ██╔══╝  ██╔══██╗██║   ██║╚════██║██║██║   ██║██╔══██║   ██║   
███████╗███████╗██║  ██║╚██████╔╝███████║██║╚██████╔╝██║  ██║   ██║   
╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
    """
    print(Fore.CYAN + banner)
    print(Fore.WHITE + "Created By: Robert Harp")
    print(Fore.WHITE + "Version: 1.0.0")
    print(Fore.CYAN + "=" * 80)

def display_starting_banner():
    print()
    print(Fore.GREEN + "\n+" + "-" * 78 + "+")
    print(Fore.GREEN + "| Starting ZeroSight" + " " * 59 + "|")
    print(Fore.GREEN + "+" + "-" * 78 + "+")

# -------------------------------------------------------------------
# UTILITY FUNCTIONS
# -------------------------------------------------------------------
def validate_target(target: str) -> bool:
    if not target:
        return False
    ip_regex = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    domain_regex = r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
    return re.match(ip_regex, target) or re.match(domain_regex, target)

def ensure_directories(base_dir: Path, target: str) -> Path:
    target_dir = base_dir / target
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir

def get_next_run_directory(base_dir: Path, target: str) -> str:
    target_dir = base_dir / target
    target_dir.mkdir(parents=True, exist_ok=True)
    run_dirs = [d for d in target_dir.iterdir() if d.is_dir() and d.name.startswith("Run")]
    if run_dirs:
        run_numbers = [int(d.name[3:]) for d in run_dirs if d.name[3:].isdigit()]
        next_run_number = max(run_numbers) + 1 if run_numbers else 1
    else:
        next_run_number = 1
    next_run_dir = target_dir / f"Run{next_run_number}"
    next_run_dir.mkdir(parents=True, exist_ok=True)
    return f"Run{next_run_number}"

def display_menu(categories: list) -> List[int]:
    while True:
        print(Fore.CYAN + "+" + "-" * 78 + "+")
        print(Fore.CYAN + "| ZeroSight Automated Enumeration Tool" + " " * 41 + "|")
        print(Fore.CYAN + "+" + "-" * 78 + "+")
        print(Fore.CYAN + "| Select categories (comma-separated for multiple, or '0' for Automatic):" + " " * 6 + "|")
        for idx, category in enumerate(categories, start=1):
            print(Fore.CYAN + f"| {idx}. {category}" + " " * (75 - len(category) - len(str(idx))) + "|")
        print(Fore.CYAN + "| 0. Automatic" + " " * 65 + "|")
        print(Fore.CYAN + "+" + "-" * 78 + "+")
        choice = input(Fore.GREEN + "Enter your choice: " + Style.RESET_ALL)
        return choice

def execute_tools(tools: list, target: str, run_dir: str, base_dir: Path):
    for tool in tools:
        command = tool['command'].replace("{target}", target).replace("{base_dir}", str(base_dir)).replace("{run_dir}", run_dir)
        log_file_path = Path(command.split()[-1])
        log_file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        print(Fore.GREEN + f"\nExecuting: {command}" + Style.RESET_ALL)
        
        try:
            result = subprocess.run(command, shell=True, timeout=300, capture_output=True, text=True)
            print(result.stdout)  # Print the standard output
            print(result.stderr)  # Print the standard error
            with open(log_file_path, 'w') as log_file:
                log_file.write(result.stdout)
                log_file.write(result.stderr)
            if result.returncode != 0:
                logger.error(f"Error executing {tool['name']}: {result.stderr}")
                print(Fore.RED + f"Error executing {tool['name']}: {result.stderr}" + Style.RESET_ALL)
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout expired for {tool['name']} on {target}")
            print(Fore.RED + f"Timeout expired for {tool['name']} on {target}" + Style.RESET_ALL)
            
# -------------------------------------------------------------------
# REPORT GENERATOR
# -------------------------------------------------------------------
class ReportGenerator:
    def __init__(self, base_dir: Path, target: str, run_dir: str):
        self.base_dir = base_dir
        self.target = target
        self.run_dir = run_dir
        self.report_dir = base_dir / f"reports/{target}/{run_dir}"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def generate_reports(self):
        logs_dir = self.base_dir / f"logs/{self.target}/{self.run_dir}"
        logs = [log for log in logs_dir.glob("*.txt")]

        self.generate_text_report(logs)
        self.generate_json_report(logs)
        self.generate_csv_report(logs)
        self.generate_html_report(logs)

    def generate_text_report(self, logs):
        with open(self.report_dir / "report.txt", "w") as report_file:
            report_file.write(f"Zerosight Security Assessment Report\n")
            report_file.write(f"Target: {self.target}\n")
            report_file.write(f"Run ID: {self.run_dir}\n")
            report_file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for log in logs:
                with open(log, "r") as log_file:
                    report_file.write(f"--- {log.name} ---\n")
                    report_file.write(log_file.read())
                    report_file.write("\n\n")

    def generate_json_report(self, logs):
        report_data = {
            "target": self.target,
            "run_id": self.run_dir,
            "generated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "logs": {}
        }
        for log in logs:
            with open(log, "r") as log_file:
                report_data["logs"][log.name] = log_file.read()
        with open(self.report_dir / "report.json", "w") as report_file:
            json.dump(report_data, report_file, indent=4)

    def generate_csv_report(self, logs):
        with open(self.report_dir / "report.csv", "w", newline='') as report_file:
            csv_writer = csv.writer(report_file)
            csv_writer.writerow(["Zerosight Security Assessment Report"])
            csv_writer.writerow([f"Target: {self.target}"])
            csv_writer.writerow([f"Run ID: {self.run_dir}"])
            csv_writer.writerow([f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
            csv_writer.writerow([])
            csv_writer.writerow(["Log File", "Content"])
            for log in logs:
                with open(log, "r") as log_file:
                    csv_writer.writerow([log.name, log_file.read()])

    def generate_html_report(self, logs):
        with open(self.report_dir / "report.html", "w") as report_file:
            report_file.write("<html><body>\n")
            report_file.write(f"<h1>Zerosight Security Assessment Report</h1>\n")
            report_file.write(f"<p>Target: {self.target}</p>\n")
            report_file.write(f"<p>Run ID: {self.run_dir}</p>\n")
            report_file.write(f"<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>\n")
            report_file.write("<h2>Assessment Summary</h2>\n")
            for log in logs:
                with open(log, "r") as log_file:
                    report_file.write(f"<h3>{log.name}</h3>\n")
                    report_file.write("<pre>\n")
                    report_file.write(log_file.read())
                    report_file.write("</pre>\n")
            report_file.write("</body></html>\n")

# -------------------------------------------------------------------
# MAIN ZEROSIGHT CLASS
# -------------------------------------------------------------------
class ZeroSight:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = setup_logger("ZeroSight")
        self.report_generator = ReportGenerator(Path("reports"))

    def execute_tool(self, tool: Dict, target: str) -> Dict:
        command = tool["command"].replace("{target}", target)
        result = {"tool": tool["name"], "status": "failed", "output": "", "error": ""}
        try:
            proc = subprocess.run(command.split(), capture_output=True, text=True, timeout=tool.get("timeout", 300))
            result["status"] = "success" if proc.returncode == 0 else "failed"
            result["output"] = proc.stdout
            result["error"] = proc.stderr
        except subprocess.TimeoutExpired:
            result["status"] = "timeout"
            result["error"] = "Execution timed out."
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        return result

    def process_target(self, target: str, category: Dict) -> List[Dict]:
        results = []
        tools = category.get("tools", [])
        for tool in tools:
            self.logger.info(f"Executing {tool['name']} on {target}")
            result = self.execute_tool(tool, target)
            results.append(result)
        return results

    def process_targets(self, targets: List[str], category_id: int):
        category = self.config["categories"].get(str(category_id))
        if not category:
            self.logger.error(f"Invalid category ID: {category_id}")
            return

        for target in targets:
            if not validate_target(target):
                self.logger.error(f"Invalid target format: {target}")
                continue

            self.logger.info(f"Processing target: {target}")
            results = self.process_target(target, category)
            self.report_generator.save({"target": target, "results": results})

    def get_targets(self) -> List[str]:
        print(Fore.CYAN + "\nTarget Input Options:")
        print(Fore.WHITE + "1. Enter single domain/IP")
        print(Fore.WHITE + "2. Provide file with targets")

        while True:
            try:
                choice = input(Fore.GREEN + "\nSelect option (1-2): " + Style.RESET_ALL).strip()
                if choice == "1":
                    target = input(Fore.GREEN + "Enter domain/IP: " + Style.RESET_ALL).strip()
                    if validate_target(target):
                        return [target]
                    print(Fore.RED + "Invalid target. Please try again." + Style.RESET_ALL)
                elif choice == "2":
                    file_path = input(Fore.GREEN + "Enter path to targets file: " + Style.RESET_ALL).strip()
                    if os.path.exists(file_path):
                        with open(file_path, "r") as f:
                            targets = [line.strip() for line in f if validate_target(line.strip())]
                        if targets:
                            return targets
                        print(Fore.RED + "No valid targets found in file." + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "File not found." + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Invalid option. Please enter 1 or 2." + Style.RESET_ALL)
            except Exception as e:
                self.logger.error(f"Error reading target input: {str(e)}")

    def display_menu(self) -> int:
        categories = self.config["categories"]

        print(Fore.CYAN + "\nAvailable Categories:")
        for idx, cat in categories.items():
            print(Fore.WHITE + f"{idx}. {cat['name']}")
        print(Fore.WHITE + "0. Automatic (Run all categories)")

        while True:
            try:
                selection = input(Fore.GREEN + "\nSelect category (0 to list all): " + Style.RESET_ALL).strip()
                if selection.isdigit() and int(selection) in range(len(categories) + 1):
                    return int(selection)
                print(Fore.RED + "Invalid selection. Please try again." + Style.RESET_ALL)
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                sys.exit(0)

    def run(self):
        display_banner()
        matrix_rain = MatrixRain()
        matrix_rain.animate()

        targets = self.get_targets()
        if not targets:
            self.logger.error("No valid targets provided.")
            print(Fore.RED + "No valid targets provided. Exiting." + Style.RESET_ALL)
            return

        category_id = self.display_menu()
        self.process_targets(targets, category_id)

# -------------------------------------------------------------------
# MAIN SCRIPT ENTRY
# -------------------------------------------------------------------
def main():
    try:
        matrix_rain = MatrixRain()
        matrix_rain.animate(duration=5)
        display_banner()
        target = input("Enter target: ")
        if not validate_target(target):
            print(Fore.RED + "Invalid target format." + Style.RESET_ALL)
            sys.exit(1)
        print("Target entered:", target)

        # Dynamically determine the base directory
        base_dir = Path(__file__).resolve().parent

        config = load_config(base_dir / "tools.toml")
        categories = [cat['name'] for cat in config['categories'].values()]
        choices = display_menu(categories)

        display_starting_banner()

        run_dir = get_next_run_directory(base_dir / "logs", target)

        if choices == '0':
            # Automatically select all categories
            for idx, category in enumerate(categories, start=1):
                selected_category = list(config['categories'].values())[idx - 1]
                tools = selected_category['tools']
                execute_tools(tools, target, run_dir, base_dir)
        else:
            for choice in choices.split(','):
                if choice.isdigit() and 1 <= int(choice) <= len(categories):
                    selected_category = list(config['categories'].values())[int(choice) - 1]
                    tools = selected_category['tools']
                    execute_tools(tools, target, run_dir, base_dir)
                else:
                    print(Fore.RED + "Invalid selection. Please enter valid numbers corresponding to the categories." + Style.RESET_ALL)

        # Generate reports after executing all tools
        report_generator = ReportGenerator(base_dir, target, run_dir)
        report_generator.generate_reports()

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()

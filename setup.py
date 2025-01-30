#!/usr/bin/env python3
# ZeroSight Setup Script
# Created: 2025-01-12 21:55:08 UTC
# Author: Robert Harp
import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path
from typing import List, Dict

class ZeroSightSetup:
    def __init__(self):
        self.base_dir = Path(__file__).parent.absolute()
        self.required_dirs = [
            'logs',
            'results',
            'templates',
            'wordlists',
            'tool_cache',
            'nuclei-templates',
            'offline_tools'
        ]
        self.python_version = (3, 8)
        self.wordlist_files = ['directories.txt', 'subdomains.txt', 'users.txt']
        self.dependencies = [
            'requests>=2.26.0',
            'toml>=0.10.0',
            'rich>=10.0.0',
            'jinja2>=3.0.0'
        ]

    def check_python_version(self) -> bool:
        """Verify Python version meets requirements"""
        current = sys.version_info[:2]
        if current < self.python_version:
            print(f"Error: Python {self.python_version[0]}.{self.python_version[1]} or higher required")
            return False
        return True

    def create_directories(self):
        """Create required directories"""
        print("Creating required directories...")
        for directory in self.required_dirs:
            dir_path = self.base_dir / directory
            dir_path.mkdir(exist_ok=True)
            print(f"Created directory: {directory}")

    def install_dependencies(self):
        """Install Python package dependencies"""
        print("Installing Python dependencies...")
        try:
            for dependency in self.dependencies:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dependency])
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            return False
        return True

    def setup_wordlists(self):
        """Setup basic wordlists"""
        wordlists_dir = self.base_dir / 'wordlists'
        
        basic_lists = {
            'directories.txt': ['admin', 'api', 'login', 'wp-admin', 'dashboard'],
            'subdomains.txt': ['www', 'mail', 'remote', 'blog', 'dev'],
            'users.txt': ['admin', 'user', 'test', 'guest', 'system']
        }

        print("Setting up basic wordlists...")
        for filename, words in basic_lists.items():
            file_path = wordlists_dir / filename
            with open(file_path, 'w') as f:
                f.write('\n'.join(words))
            print(f"Created wordlist: {filename}")

    def setup_templates(self):
        """Setup report templates"""
        templates_dir = self.base_dir / 'templates'
        
        # HTML Report Template
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>ZeroSight Scan Report</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f0f0f0; padding: 20px; }
        .results { margin-top: 20px; }
        .tool-result { border: 1px solid #ddd; margin: 10px 0; padding: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>ZeroSight Scan Report</h1>
        <p>Generated: {{timestamp}}</p>
        <p>Target: {{target}}</p>
    </div>
    <div class="results">
        {{content}}
    </div>
</body>
</html>
        """
        
        with open(templates_dir / 'report.html', 'w') as f:
            f.write(html_template)

    def verify_installation(self) -> bool:
        """Verify the installation was successful"""
        checks = {
            'Directories': all((self.base_dir / dir).exists() for dir in self.required_dirs),
            'Python Packages': self.verify_python_packages(),
            'Templates': (self.base_dir / 'templates' / 'report.html').exists(),
            'Wordlists': self.verify_wordlists()
        }
        
        for check, status in checks.items():
            print(f"{check}: {'✓' if status else '✗'}")
        
        return all(checks.values())

    def verify_python_packages(self) -> bool:
        """Verify Python packages are installed"""
        try:
            subprocess.run([sys.executable, "-m", "pip", "freeze"], 
                         capture_output=True, 
                         check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def verify_wordlists(self) -> bool:
        """Verify wordlists exist"""
        wordlist_files = ['directories.txt', 'subdomains.txt', 'users.txt']
        return all((self.base_dir / 'wordlists' / f).exists() for f in wordlist_files)

    def run(self):
        """Run the setup process"""
        print("Starting ZeroSight setup...")
        print(f"Setup initiated by: rharp86")
        print(f"Timestamp: 2025-01-12 21:55:08 UTC")
        
        if not self.check_python_version():
            sys.exit(1)
            
        try:
            self.create_directories()
            self.install_dependencies()
            self.setup_wordlists()
            self.setup_templates()
            
            if self.verify_installation():
                print("\nZeroSight setup completed successfully!")
            else:
                print("\nZeroSight setup completed with errors.")
                
        except Exception as e:
            print(f"Error during setup: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    setup = ZeroSightSetup()
    setup.run()

# ZeroSight - Advanced Automated Enumeration Tool
**Created By:** Robert Harp   
**Version:** 1.0.0

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Standard Installation](#standard-installation)
  - [Offline Installation](#offline-installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Offline Mode](#offline-mode)
- [Categories](#categories)
- [Configuration](#configuration)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview
ZeroSight is a comprehensive automated enumeration tool designed to streamline security assessments and penetration testing workflows. It integrates multiple security tools and provides a unified interface for reconnaissance, vulnerability assessment, and security testing.

## Features
- 🚀 Full integration with Nuclei and templates
- 🎯 Eight specialized scanning categories
- 📊 Detailed logging and reporting
- ⚡ Multi-threading with smart timeout management
- 🌐 Offline mode support
- 🎨 Matrix-style visualization
- 📝 Comprehensive HTML and JSON reports
- ⚙️ Configurable tool parameters via TOML
- 🔄 Automatic dependency management

## Requirements
- Python 3.8 or higher
- Git (for initial setup)
- 4GB RAM minimum (8GB recommended)
- Internet connection (for initial setup)

### Core Dependencies
```text
requests>=2.26.0
toml>=0.10.0
rich>=10.0.0
jinja2>=3.0.0

Installation
Standard Installation

    Clone the repository:

bash

git clone https://github.com/rharp86/zerosight.git
cd zerosight

    Run the setup script:

bash

python3 setup.py

    Verify installation:

bash

python3 zerosight.py --check

Offline Installation

    Download the offline package:

bash

# While online
python3 setup.py --download-offline

    Transfer the generated zerosight_offline.tar.gz to the target system

    Extract and install offline:

bash

tar -xzf zerosight_offline.tar.gz
cd zerosight
python3 setup.py --offline

Offline Package Contents

    Python wheel files for all dependencies
    Basic wordlists
    Nuclei templates
    Tool binaries (where applicable)

Usage
Basic Usage
bash

python3 zerosight.py

Follow the interactive prompts to:

    Enter target domain/IP or file
    Select scanning category
    View real-time results

Offline Mode
bash

python3 zerosight.py --offline

Categories

    Automatic - Full automated scanning
        Nuclei
        Nmap
        Gobuster
        Subfinder
            3 more tools

    OSINT - Intelligence gathering
        theHarvester
        Spiderfoot
        Whois
            5 more tools

    Credentials - Password security
        Hydra
        Medusa
        Crowbar
            4 more tools

    Network - Network analysis
        Nmap
        Masscan
        Unicornscan
            5 more tools

    Web - Web application testing
        WPScan
        Nikto
        SQLMap
            6 more tools

    Active Directory - AD assessment
        Bloodhound
        Kerbrute
        CrackMapExec
            4 more tools

    Cloud - Cloud infrastructure
        CloudFail
        S3Scanner
        CloudMapper
            5 more tools

    Databases - Database security
        MongoDB tools
        MySQL tools
        PostgreSQL tools
            5 more tools

Configuration

The tools.toml file contains all tool configurations:
bash

vim tools.toml

Key Configuration Sections:

    General settings
    Category-specific tools
    Threading options
    Rate limiting
    Proxy settings
    Offline mode settings

Logging

Logs are stored in logs/ directory:

    Activity logs: zerosight_YYYYMMDD_HHMMSS.log
    Tool output: results_YYYYMMDD_HHMMSS/
    Error logs: error_YYYYMMDD_HHMMSS.log

Log Rotation

    Logs are automatically rotated after 7 days
    Compressed archives are maintained for 30 days

Troubleshooting
Common Issues

    Tool Not Found
    bash

# Reinstall tool
python3 setup.py --reinstall-tools

Dependency Errors
bash

# Rebuild dependencies
python3 setup.py --rebuild-deps

Offline Mode Issues
bash

    # Verify offline package
    python3 setup.py --verify-offline

Debug Mode
bash

python3 zerosight.py --debug

Contributing

    Fork the repository
    Create feature branch
    Commit changes
    Push to branch
    Create Pull Request

License

MIT License - See LICENSE file for details

Created By: Robert Harp (rharp86)
Last Updated: 2025-01-12 23:03:33 UTC
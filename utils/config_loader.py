### utils/config_loader.py
import toml
from pathlib import Path

def load_config():
    config_path = Path("tools.toml")
    if not config_path.exists():
        raise FileNotFoundError("Configuration file tools.toml not found.")
    return toml.load(config_path)

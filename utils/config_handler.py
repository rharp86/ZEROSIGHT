import toml
from pathlib import Path

from utils.config_loader import load_config

class ConfigHandler:
    def __init__(self, config_path: str = "tools.toml"):
        self.config_path = Path(config_path)
        self.config = self.load_config()

    def load_config(self) -> dict:
        """Load the configuration file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as config_file:
            config = toml.load(config_file)
        
        self.validate_config(config)
        return config

    def validate_config(self, config: dict):
        """Validate the loaded configuration."""
        required_sections = ["general", "categories"]
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required configuration section: {section}")
        
        # Validate categories and tools
        for category_id, details in config["categories"].items():
            if "name" not in details or "tools" not in details:
                raise KeyError(f"Category '{category_id}' is missing required 'name' or 'tools' field")

            for tool in details["tools"]:
                if "name" not in tool or "command" not in tool:
                    raise KeyError(f"Tool in category '{category_id}' is missing required 'name' or 'command' field")

    def get_config(self) -> dict:
        """Return the loaded configuration."""
        return self.config

    def load_config(config_path: str = "tools.toml") -> dict:
        """Convenience function to load the configuration."""
        handler = ConfigHandler(config_path)
        return handler.get_config()

# Example usage:
if __name__ == "__main__":
    try:
        config = load_config("tools.toml")
        print("Configuration loaded successfully:")
        print(config)
    except RuntimeError as e:
        print(e)
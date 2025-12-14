"""Configuration Management"""
import yaml
from typing import Dict, Any, Optional
from dataclasses import dataclass
import os

@dataclass
class Config:
    """Configuration container."""
    data: Dict[str, Any]

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value with dot notation support."""
        keys = key.split(".")
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

def load_config(path: str) -> Config:
    """Load configuration from YAML file."""
    with open(path) as f:
        data = yaml.safe_load(f)
    return Config(data or {})

def save_config(config: Config, path: str) -> None:
    """Save configuration to YAML file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(config.data, f, default_flow_style=False)

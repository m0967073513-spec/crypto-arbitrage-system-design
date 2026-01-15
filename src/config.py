import yaml
from pathlib import Path

def load_config():
    path = Path("config/config.yaml")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

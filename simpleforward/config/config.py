from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, SecretStr

from .models import *


class Config(BaseModel):
    bot: Bot = Bot()
    forwarding: Forwarding = Forwarding()
    logging: Logging = Logging()

    @classmethod
    def load(cls, cfg_path: Optional[Path] = None):
        filepath = Path(cfg_path)
        filepath.parent.mkdir(parents = True, exist_ok = True)

        if not filepath.exists():
            config = cls()
        else:
            with filepath.open(encoding = "utf-8") as config_file:
                config = cls(**yaml.safe_load(config_file))

        object.__setattr__(config, "filepath", filepath)

        if not filepath.exists():
            config.save()

        return config

    def save(self, cfg_path: Optional[Path] = None):
        if not getattr(self, "filepath") and not cfg_path:
            raise FileNotFoundError(f"Cannot find config file: {getattr(self.filepath) or cfg_path}")

        if not getattr(self, "filepath") or (not isinstance(cfg_path, Path) and cfg_path is not None):
            self.filepath = Path(cfg_path)

        self.filepath.parent.mkdir(parents = True, exist_ok = True)

        with open(self.filepath, "w", encoding = "utf-8") as config_file:
            yaml.dump(self._serialize(self.model_dump()), config_file, width = float("inf"), sort_keys = False)

    @classmethod
    def _serialize(cls, obj):
        if isinstance(obj, SecretStr):
            return obj.get_secret_value()
        elif isinstance(obj, dict):
            return {key: cls._serialize(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [cls._serialize(value) for value in obj]

        return obj
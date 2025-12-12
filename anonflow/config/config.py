from pathlib import Path

import yaml
from pydantic import BaseModel, SecretStr

from .models import Config as MainConfig


class Config(BaseModel):
    config: MainConfig = MainConfig()

    def __getattr__(self, name: str, /):
        config = object.__getattribute__(self, "config")

        if name in config.model_fields:
            return object.__getattribute__(config, name)

        return object.__getattribute__(self, name)

    @classmethod
    def _serialize(cls, obj):
        if isinstance(obj, SecretStr):
            return obj.get_secret_value()
        elif isinstance(obj, dict):
            return {key: cls._serialize(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [cls._serialize(value) for value in obj]

        return obj

    @classmethod
    def load(cls, filepath: Path):
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if filepath.exists():
            with filepath.open(encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            return cls(config=MainConfig(**data))

        return cls(config=MainConfig())

    def save(self, filepath: Path):
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with filepath.open("w", encoding="utf-8") as config_file:
            yaml.dump(
                self._serialize(self.config.model_dump()),
                config_file,
                width=float("inf"),
                sort_keys=False,
                default_flow_style=False
            )

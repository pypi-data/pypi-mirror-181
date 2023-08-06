from pydantic import BaseModel, Field, AnyUrl
import yaml
from typing import Literal, Optional
from pathlib import Path
from metagen.helpers import make_hash
from metagen.base import singleton

BASE_CONFIG_FILE = Path(__file__).parent / 'config.yaml'


class HashableBaseModel(BaseModel):
    """Helper class implementing hash into the base model"""

    def __hash__(self) -> int:
        return make_hash({k: v for k, v in self.__dict__.items()})


class RegisterConfig(HashableBaseModel):
    registerName: Literal['pandas', 'dict']

    def __str__(self):
        items = [f"\t- {k} : {v}\n" for k, v in self.__dict__.items()]
        return ''.join(items)


class ImporterConfig(HashableBaseModel):
    path: Optional[str]
    instance_url: Optional[str]
    host: Optional[str]
    token: str
    method: str

    def __str__(self):
        items = [f"\t- {k} : {v}\n" for k, v in self.__dict__.items()]
        return ''.join(items)


@singleton
class Config(HashableBaseModel):
    register_setting: Optional[RegisterConfig] = Field(default_factory=RegisterConfig)
    importer_setting: Optional[ImporterConfig] = Field(default_factory=ImporterConfig)

    def __init__(self):
        super().__init__(**load_yaml(BASE_CONFIG_FILE))

    def __setattr__(self, name, value):
        """Called when attribute is set. Automatically save the setting"""
        setattr(self, name, value)
        dump_yaml(Path(BASE_CONFIG_FILE), self.dict())

    def __str__(self):
        items = [f"{k} : {str(v)}" for k, v in self.__dict__.items()]
        return ''.join([f"{k} : \n {str(v)}" for k, v in self.__dict__.items()])


def load_yaml(path: str) -> dict:
    with open(path, 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def dump_yaml(path: Path, data: dict) -> None:
    with open(path, 'w') as file:
        file.write(yaml.dump(data, Dumper=yaml.Dumper))


CONFIG = Config()



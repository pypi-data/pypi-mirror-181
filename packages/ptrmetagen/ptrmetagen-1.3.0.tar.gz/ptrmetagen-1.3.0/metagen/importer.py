from typing import Dict, Type

from pydantic import BaseModel, validator, AnyUrl, Field
from pathlib import Path
import subprocess
from requests import post
from abc import ABC, abstractmethod

from metagen.pipes import path_check
from metagen.gui import ConfirmUrl


class ImportError(Exception):
    pass


class ImporterABC(BaseModel, ABC):

    @abstractmethod
    def import_fixtures(self, fixtures: dict) -> None:
        pass


class ImporterBase(ImporterABC):
    """base class for all importers"""
    instance_url: AnyUrl

    @validator('instance_url')
    def confirm_instance(cls, value):
        alert = ConfirmUrl(instance_url=value)
        if alert.confirm:
            return value
        else:
            quit()


class NodeImporter(ImporterBase):
    path: Path
    host: AnyUrl

    @validator('path', pre=True)
    def set_pat(cls, value):
        return path_check(value)

    def run(self, fixtutres: dict) -> dict:
        self.server_start()
        report = self.import_fixtures(fixtutres)
        self.server_stop()
        return report

    def server_start(self):
        """Start importer node server"""
        subprocess.run(f'node {self.path / "server"} start')

    def server_stop(self):
        """Start importer node server"""
        subprocess.run(f'node {self.path / "server"} stop')

    def import_fixtures(self, fixtures: dict):
        response = post(url=f'{self.host}/metadata', data=fixtures)
        if response.status_code == 200:
            return response.json()
        else:
            raise ImportError(f'Import of fixtures failed '
                              f'\n status: {response.status_code} '
                              f'\n message: {response.content}')


class UrlImporter(ImporterBase):
    token: str

    def import_fixtures(self, fixtures: dict) -> None:
        headers = {"import-token": self.token}
        response = post(url=f'{self.instance_url}/fixtures/import', files=fixtures, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise ImportError(f'Import of fixtures failed '
                              f'\n status: {response.status_code} '
                              f'\n message: {response.content}')


class ImporterFactory(BaseModel):
    importers: Dict[str, Type[ImporterABC]] = Field(default_factory=dict)

    def add(self, name: str, importer: Type[ImporterABC]) -> None:
        self.importers.update({name: importer})

    def get(self, name: str) -> Type[ImporterABC]:
        return self.importers.get(name)


importer_factory = ImporterFactory()
importer_factory.add(name='node', importer=NodeImporter)
importer_factory.add(name='endpoint', importer=UrlImporter)
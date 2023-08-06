from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, List, Type, Optional, Literal
import json
from uuid import UUID

from metagen.base import LeafABC, UUIDEncoder, FactoryABC
from metagen.helpers import create_file, load_json
from metagen.config.config import CONFIG
from metagen.pipes import path_check
from metagen.register import RegisterABC
from metagen.importer import ImporterFactory



# serialization & deserialization
class SerializerABC(BaseModel, ABC):

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def to_json(self, path: Union[Path, str]) -> None:
        pass


class JSONSerializer(SerializerABC):
    reg: RegisterABC
    structure: dict = Field(default={})

    def to_dict(self) -> dict:
        for element in self.reg.get_elements():
            nodes = element.__nodes__().split('.')
            self.set_node(self.structure, nodes, element)
        return self.structure

    def set_node(self, structure: dict, nodes: list, element: Type[LeafABC]):
        node = nodes.pop(0)
        if len(nodes) > 0:
            if not structure.get(node):
                structure[node] = {}
            self.set_node(structure[node], nodes, element)
        else:
            if not structure.get(node):
                structure[node] = []
            structure[node].append(element.to_dict())

    def to_json(self, path: Union[Path, str]) -> None:
        structure = self.to_dict()

        path = path_check(path)

        if not path.parent:
            create_file(path.parent)

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(structure, file, indent=6, cls=UUIDEncoder, ensure_ascii=False)


class DeSerializerABC(BaseModel, ABC):
    factory: FactoryABC

    @abstractmethod
    def load(self, path: Union[Path, str], **kwargs) -> None:
        pass


class JSONDeserializer(DeSerializerABC):

    def load(self, path: Union[Path, str], encoding='utf8') -> None:

        path = path_check(path)
        obj = load_json(path, encoding)
        for node, structure in obj.items():
            print(f'Loading: {node}')
            self._parse(node, structure)

    def _parse(self, nodes: str, obj: Union[dict, list]) -> None:

        if isinstance(obj, dict):
            for node, structure in obj.items():
                self._parse(f'{nodes}.{node}', structure)
        elif isinstance(obj, list):
            for data in obj:
                self.factory.create(nodes, data)


# generator
class PTRMetagenABC(BaseModel, ABC):
    serializer: SerializerABC
    deserializer: DeSerializerABC
    importer_factory: ImporterFactory
    reg: RegisterABC

    @abstractmethod
    def import_fixtures(self) -> dict:
        pass

    class Config:
        arbitrary_types_allowed = True


class _PTRMetagen(PTRMetagenABC):
    serializer: SerializerABC
    deserializer: DeSerializerABC
    reg: RegisterABC
    importer_factory: ImporterFactory

    def import_fixtures(self, instance_url: Optional[str] = None, method: Optional[Literal['node', 'endpoint']] = None):
        """
        Method imports fixtures into the instance.
        instance_url: str - url of instance in form foo.bar/backend/rest - Parameter optional, if None, instance_url is
        taken from configuration
        method: str: - parameter select method of import. "node" for Node.js importer, "endpoint" for url endpoint -
        Parameter optional, if None, method is taken from configuration
        """
        Importer = self.importer_factory.get(method or CONFIG.importer_setting.method)
        importer = Importer(instance_url=instance_url or CONFIG.importer_setting.instance_url,
                            **CONFIG.importer_setting.dict(exclude={'instance_url'}))
        importer.import_fixtures(fixtures=self.to_dict())

    def load_fixtures(self, path: Union[Path, str], encoding='utf8') -> None:
        """Load fixtures into the register"""
        self.deserializer.load(path, encoding=encoding)

    def to_dict(self) -> dict:
        """Generate dict representation of fixtures from register"""
        return self.serializer.to_dict()

    def to_json(self, path: Union[str, Path]) -> None:
        """Generate json representation of fixtures from register"""
        self.serializer.to_json(path)

    def get_element_by_uuid(self, uuid: str) -> Type[LeafABC]:
        """Return element of given uuid"""
        if self.reg.get_by_uuid(uuid):
            return self.reg.get_by_uuid(uuid)
        else:
            raise ValueError(f'Element with uuid {uuid} did not find')

    def get_elements_by_type(self, element: Type[LeafABC]) -> List[Type[LeafABC]]:
        """Return list of all elements of given element type"""
        return [v for k, v in self.reg.uuid.items() if isinstance(v, element.__wrapped__)]

    def get_element_by_name_internal(self, name_internal: str) -> Type[LeafABC]:
        return self.reg.get_element_by_name_internal(name_internal)

    def find_elements_by_name_internal(self, name_internal: str) -> List[Type[LeafABC]]:
        return self.reg.find_elements_by_name_internal(name_internal)

    def check_missing_keys(self) -> List[str]:
        missing = []
        for element in self.reg.uuid.values():
            for attrName, value in element.__dict__.items():
                if attrName.__contains__('Key') and value:
                    if isinstance(value, (UUID, str)):
                        if not str(value) in self.reg.uuid:
                            missing.append(value)
                    elif isinstance(value, list):
                        for uuid in value:
                            if not str(uuid) in self.reg.uuid:
                                missing.append(uuid)
        return missing




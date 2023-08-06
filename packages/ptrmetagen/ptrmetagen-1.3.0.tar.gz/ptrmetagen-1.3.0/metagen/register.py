from abc import ABC, abstractmethod
from uuid import UUID
from typing import Type, Any, List, Dict
from pydantic import BaseModel, Field

from metagen.base import LeafABC, BaseModelArbitrary
from metagen.helpers import Singleton


class RegisterABC(BaseModelArbitrary, ABC):

    @abstractmethod
    def get_elements(self) -> List[Type[LeafABC]]:
        pass

    @abstractmethod
    def add(self, element: Type[LeafABC]) -> None:
        pass

    @abstractmethod
    def check_register(self, element: Type[LeafABC]) -> bool:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: UUID) -> Type[LeafABC]:
        pass


# register
class DictRegister(RegisterABC, Singleton):
    uuid: dict = Field(default_factory=dict)

    @property
    def hashes(self):
        return {hash(element): element for element in self.uuid.values()}

    @property
    def name_internals(self):
        return {element.nameInternal : element for element in self.uuid.values()}

    def get_elements(self) -> List[Type[LeafABC]]:
        return [element for element in self.uuid.values()]

    def add(self, element: Type[LeafABC]) -> None:
        # TODO resolve hash and uuid check
        if not self.check_register(element):
            if element.key not in self.uuid:
                self.uuid.update({str(element.key): element})
            else:
                raise KeyError(f'UUID duplicity conflict: element {element} with UUID {element.key} exist in register')
        else:
            raise ValueError(f'Hash duplicity conflict: "{element.__class__.__name__}" with '
                             f'key: {element.key} and hash: {hash(element)} already exist')

    def check_register(self, element: Type[LeafABC]) -> bool:
        return hash(element) in self.hashes

    def get_by_uuid(self, uuid: str) -> Type[LeafABC]:
        if UUID(uuid):
            return self.uuid.get(uuid)

    def get_by_hash(self, hash: int) -> Type[LeafABC]:
        return self.hashes.get(hash)

    def get_element_by_name_internal(self, name_internal: str) -> Type[LeafABC]:
        return self.name_internals.get(name_internal)

    def find_elements_by_name_internal(self, name_internal: str) -> List[Type[LeafABC]]:
        return [element for name, element in self.name_internals.items() if name.__contains__(name_internal)]


class RegisterFactory(BaseModel):
    registers: Dict[str, Type[RegisterABC]] = Field(default_factory=dict)

    def add(self, registerName: str, registerType: Type[RegisterABC]) -> None:
        self.registers.update({registerName: registerType})

    def get(self, registerName: str, **ignore) -> Type[RegisterABC]:
        return self.registers[registerName]


register_factory = RegisterFactory()
register_factory.add(registerName='dict', registerType=DictRegister)

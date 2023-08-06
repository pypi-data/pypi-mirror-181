from pydantic import BaseModel
from metagen.components._base import Component


class ViewComponent(Component):
    longDescription: str



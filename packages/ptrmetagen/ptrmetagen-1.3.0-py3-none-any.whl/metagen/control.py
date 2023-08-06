from typing import Type

from metagen.main import register
from metagen.base import LeafABC


def find_ureferenced_key(keyName: str)-> list[LeafABC]:
    uuids = register.table['key'].unique()

    try:
        keys = register.table[keyName].unique()
    except KeyError:
        raise KeyError(f'{keyName} did not find among the element attributes in the register')

    for key in keys:
        pass


if  __name__  == '__main__':
    from pathlib import Path
    from metagen import PTRMetagen

    path = Path('C:\\Users\\micha\\PycharmProjects\\app-esaWorldWater\\fixtures.json')

    gen = PTRMetagen()
    gen.load_fixtures(path)

    pass

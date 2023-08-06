from pathlib import Path
from pydantic import AnyUrl

from metagen.importer import importer_factory

from metagen.config.config import Config

CONFIG = Config()



def test_importer_init_method():
    method = 'node'
    try:
        Importer = importer_factory.get(method or CONFIG.importer_setting.method)
        importer = Importer(**CONFIG.importer_setting.dict())
    except Exception as e:
        assert False

    assert isinstance(importer.path, Path)
    assert isinstance(importer.instance_url, AnyUrl)


def test_importer_init_method_none():
    method = None
    try:
        Importer = importer_factory.get(method or CONFIG.importer_setting.method)
        importer = Importer(**CONFIG.importer_setting.dict())
    except Exception as e:
        assert False

    assert isinstance(importer.token, str)
    assert isinstance(importer.instance_url, AnyUrl)
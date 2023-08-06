import pytest
from metagen import PTRMetagen
from metagen import LayerTemplate


def test_generator_import_none():
    gen = PTRMetagen()
    lt1 = LayerTemplate(applicationKey='app', nameInternal=f'lt', nameDisplay='lt')
    gen.import_fixtures(instance_url='https://foo.bar', method='endpoint')



def test_generator_get_name_internal():
    gen = PTRMetagen()
    lt1 = LayerTemplate(applicationKey='app', nameInternal=f'lt', nameDisplay='lt')
    lt = gen.get_element_by_name_internal('lt')
    assert lt1 == lt


def test_generator_find_name_internal():
    gen = PTRMetagen()
    lt2 = LayerTemplate(applicationKey='app', nameInternal=f'lt_part_1', nameDisplay='lt')
    lt2 = LayerTemplate(applicationKey='app', nameInternal=f'lt_part_2', nameDisplay='lt')
    lt3 = LayerTemplate(applicationKey='app', nameInternal=f'lt_3', nameDisplay='lt')
    lts = gen.find_elements_by_name_internal('part')
    assert len(lts) == 2

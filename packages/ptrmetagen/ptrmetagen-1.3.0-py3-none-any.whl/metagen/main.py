from warnings import warn
from functools import wraps

from metagen.config.config import CONFIG
from metagen.register import register_factory
from metagen.generator import JSONSerializer, JSONDeserializer, _PTRMetagen
from metagen.importer import importer_factory



# register
register = register_factory.get(CONFIG.register_setting.registerName)()


# helpers dacoratoes
def exist_in_register(element):
    @wraps(element)
    def checking_register(*args, **kwargs):
        instance = element(*args, **kwargs)
        if register.check_register(instance):
            registered_element = register.get_by_hash(hash(instance))
            warn(str(f'Element duplication: Element {instance.__class__.__name__} with parameters: '
                 f'{"; ".join([f"{k}: {v}" for k, v in kwargs.items()])} found in register. Element '
                 f'{registered_element.__repr__()} returned instead'))
            return registered_element
        else:
            register.add(instance)
            return instance
    return checking_register


serializer = JSONSerializer(reg=register)

from metagen.metadata import element_factory
deserializer = JSONDeserializer(factory=element_factory)



def PTRMetagen(register=register) -> _PTRMetagen:
    return _PTRMetagen(serializer=serializer, deserializer=deserializer, importer_factory=importer_factory, reg=register)


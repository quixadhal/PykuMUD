# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

import re
from collections import OrderedDict, namedtuple
import copy
import json
import log_system

logger = log_system.init_logging()


def isnamedtuple(obj):
    """
    Named Tuples look, to python, like a normal tuple, so we have to poke around
    their innards a bit to see if they're actually the fancy version.
    -Updated by Syn,
    we need to account for namedtuples that are created without using anamedtuple._make()
    The check can now handle both scenarios, and will NOT hit positive on tuples or other types.

    :param obj: potential namedtuple container
    :type obj:
    :return: True if obj is a namedtuple
    :rtype: bool
    """
    b = type(obj).__bases__
    if len(b) != 1:
        return False
    f = getattr(obj, '_fields', None)
    if not isinstance(f, tuple):
        return False
    elif not hasattr(obj, '_asdict'):
        return False
    elif not callable(obj._asdict):
        return False
    else:
        return True


def to_json(data):
    """
    This function takes an arbitrary data object and attempts to return a JSON
    compatible dict-based structure, which from_json() can use to recreate the
    original object.

    :param data: data object to be serialized
    :type data:
    :return: JSON compatible data element
    :rtype:
    """

    # Order matters here.  It's important to immediately return a base type.
    if data is None or isinstance(data, (bool, int, float, str)):
        return data

    if isinstance(data, OrderedDict):
        return {
            "__type__/OrderedDict": [[to_json(k), to_json(v)] for k, v in data.items()]
        }

    # We MUST check for namedtuple() before ordinary tuples.
    # Python's normal checks can't tell the difference.
    if isnamedtuple(data):
        return {
            "__type__/namedtuple": {
                "type": type(data).__name__,
                "fields": list(data._fields),
                "values": [to_json(getattr(data, f)) for f in data._fields]
            }
        }

    if isinstance(data, set):
        return {
            "__type__/set": [to_json(val) for val in data]
        }

    if isinstance(data, tuple):
        return {
            "__type__/tuple": [to_json(val) for val in data]
        }

    if isinstance(data, list):
        return [to_json(val) for val in data]

    # Here, we return a plain dict if, and ONLY if, every key is a string.
    # JSON dicts require string keys... so otherwise, we have to manipulate.
    if isinstance(data, dict):
        if all(isinstance(k, str) for k in data):
            return {k: to_json(v) for k, v in data.items()}
        return {
            "__type__/dict": [[to_json(k), to_json(v)] for k, v in data.items()]
        }

    # Finally, the magic part.... if it wasn't a "normal" thing, check to see
    # if it has a to_json method.  If so, use it!
    if hasattr(data, 'to_json'):
        return data.to_json(to_json)

    # And if we still get nothing useful, PUNT!
    raise TypeError('Type %r not data-serializable' % type(data))


def from_json(data):
    """
    This function takes a JSON-encoded string and returns the original object
    it represents.

    :param data: JSON data chunks, passed in by json.loads()
    :type data:
    :return: An object
    :rtype:
    """

    # Order matters here.  It's important to immediately return a base type.
    if data is None or isinstance(data, (bool, int, float, str)):
        return data

    # Basic types we've labeled are easy to reconstruct.
    if "__type__/tuple" in data:
        return tuple(data["__type__/tuple"])

    if "__type__/set" in data:
        return set(data["__type__/set"])

    if "__type__/dict" in data:
        return dict(data["__type__/dict"])

    # In the case of an OrderedDict(), we just pass the data to the class.
    if "__type__/OrderedDict" in data:
        return OrderedDict(data["__type__/OrderedDict"])

    # For a namedtuple, we have to rebuild it as a class and then make an instance.
    if "__type__/namedtuple" in data:
        tmp = data["__type__/namedtuple"]
        return namedtuple(tmp["type"], tmp["fields"])(*tmp["values"])

    # If we're a dict, we can check to see if we're a custom class.
    # If we are, we need to find out class definition and make sure
    # there's a from_json() method to call.  If so, let it handle things.
    if hasattr(data, 'keys'):
        for k in data.keys():
            found = re.findall('__class__/((?:\w+)\.)*(\w+)', k)
            if found:
                import importlib
                module_name = found[0][0].rstrip('.')
                class_name = found[0][1]

                if module_name != '' and class_name != '':
                    if data[k].get('import_module', None):
                        module_ref = importlib.import_module(data[k]['import_module'])
                    else:
                        module_ref = importlib.import_module(module_name)
                    class_ref = getattr(module_ref, class_name)
                    if hasattr(class_ref, 'from_json'):
                        return class_ref.from_json(data, from_json)

    # If we have no idea, return whatever we are and hope someone else
    # will handle it up (or down) stream.
    return data


def pack(data):
    """
    A convenience method to avoid having to remember all the arguments.
    :param data: Thing to be serialized
    :return: String representation of thing
    """
    js = json.dumps(data, default=to_json, sort_keys=True)
    return js


def unpack(jso):
    """
    A convenience method to avoid having to remember all the arguments.
    :param jso: Thing to be deserialized
    :return: Thing
    """
    obj = json.loads(jso, object_hook=from_json)
    return obj


class ExampleThing(object):
    template_count = 0
    instance_count = 0

    def __init__(self, template=None, **kwargs):
        super().__init__()
        self.foo = True
        if kwargs:
            [setattr(self, k, copy.deepcopy(v)) for k, v in kwargs.items()]
        if template:
            [setattr(self, k, copy.deepcopy(v)) for k, v in template.__dict__.items()]
        if hasattr(self, 'instance_id'):
            if self.instance_id:
                self.instance_init()
                ExampleThing.instance_count += 1
            else:
                self.instance_id = None
        else:
            ExampleThing.template_count += 1
        self._last_saved = None

    def __del__(self):
        try:
            # logger.trace("Freeing %s" % str(self))
            if self.instance_id:
                ExampleThing.instance_count -= 1
                # if instance.items.get(self.instance_id, None):
                #     self.instance_destructor()
            else:
                ExampleThing.template_count -= 1
        except:
            return

    def to_json(self, outer_encoder=None):
        """
        Example usage:  js = json.dumps(self, default=serialization.to_json, sort_keys=True)
        :param outer_encoder: The top level custom JSON encoder which figures out which encodings to use
        :return: A dict with the JSON encoding of the object as a value, and the type name as a key
        """
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
            elif str(k) in ('_last_saved', '_md5'):
                continue
            else:
                tmp_dict[k] = v

        cls_name = '__class__/' + __name__ + '.' + self.__class__.__name__
        return {cls_name: outer_encoder(tmp_dict)}

    @classmethod
    def from_json(cls, data, outer_decoder=None):
        """
        Example usage: obj = json.loads(jso, object_hook=serialization.from_json)
        :param data:  A dict with the JSON encoding of the object as a value, and the type name as a key
        :param outer_decoder: The top level JSON decoder which creates objects or base types, as needed
        :return: An object or value
        """
        if outer_decoder is None:
            outer_decoder = json.JSONDecoder.decode

        cls_name = '__class__/' + __name__ + '.' + cls.__name__
        if cls_name in data:
            tmp_data = outer_decoder(data[cls_name])
            return cls(**tmp_data)
        return data

    def instance_init(self):
        pass

    def instance_destructor(self):
        pass

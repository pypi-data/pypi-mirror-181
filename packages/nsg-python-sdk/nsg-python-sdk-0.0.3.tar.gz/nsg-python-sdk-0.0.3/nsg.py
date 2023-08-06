import json
import logging
import sys

from net.happygears.nw2.py.monitoring_data_type import MonitoringDataType
from net.happygears.proto.NSG_pb2 import DataSource
# Python class that describes map view, used by views_app.py and customer's scripts views.py
from net.happygears.proto.NSG_pb2 import Device
from serialization import Serialization
from view import View


# from net.happygears.nsgpython.serdes import Serialization
# from net.happygears.nw2.py import MonitoringDataType
# from net.happygears.proto.nsg.NSG import DataSource

def get_log():
    return logging.getLogger()


def deserialize_device(file_name):
    """
    deserialize NetworkNode device object stored in given file.
    Format is deduced based on the file extension: supported extensions
    are .json and .pb

    :param file_name: file name
    :return deserialized device object (PyDevice)
    """
    with open(file_name, 'r') as fr:
        input_device = fr.read()
        if file_name.endswith('.json'):
            return Serialization.deserialize_device_json(input_device)
        elif file_name.endswith('.pb'):
            return Serialization.deserialize_device_pb(input_device)
        else:
            raise Exception('unsupported file extension {0}'.format(file_name))


def serialize_device(device: Device, file_name, fmt):
    """
    serialize device object and write to the file.
    If file_name is "-", write output to stdout.

    :param device: device object (PyDeivce)
    :param file_name: file name
    :param fmt: 'json' or 'pb' (string)
    """
    if fmt == 'json':
        s = Serialization.serialize_device_json(device)
    elif fmt == 'pb':
        s = Serialization.serialize_device_pb(device)
    else:
        raise Exception('unsupported file extension {0}'.format(file_name))
    if file_name == '-':
        sys.stdout.write(s)
    else:
        with open(file_name, 'w') as fw:
            fw.write(s)


def deserialize_device_json(serialized):
    """
    deserialize NetworkNode device object stored in json format and return PyDevice

    :param serialized:  serialized object
    :return: PyDevice object
    """
    return Serialization.deserialize_device_json(serialized)


def deserialize_device_pb(serialized):
    """
    deserialize device object stored in text protocol buffer format and return PyDevice

    :param serialized:  serialized object
    :return: PyDevice object
    """
    return Serialization.deserialize_device_pb(serialized)


def serialize_device_json(device):
    """
    serialize device object to json

    :param device:
    :return:  serialized object in json format
    """
    return Serialization.serialize_device_json(device)


def serialize_device_pb(device):
    """
    serialize device object to text protocol buffer

    :param device:
    :return:  serialized object in text protocol buffer format
    """
    return Serialization.serialize_device_pb(device)


def get_tag_word(nsg_object, facet, default=''):
    """
    Helper function to make extracting facet values from NSG objects
    little cleaner/simpler. Returns the value of the first tag of the object `nsg_object`
    in the given facet. Missing tags will be represented as an empty string or provided default.
    If multiple values exist, only the first will be used.

    :param nsg_object:  an object to extract tags from
    :param facet: tag facet
    :param default: default value used when the object has no tags in the facet
    :return: (string) a word of the first tag in given facet
    """
    tags_set = [t for t in nsg_object.tags if t.startswith(facet + '.')]
    if not tags_set:
        return default
    first = next(iter(tags_set))
    return first.replace(facet + '.', '')


def get_first_tag(tags, facet):
    """

    :param tags:  list of tag
    :param facet: tag facet
    :return: The first tag in given facet. Returns None if the object has no tags in given facet.
    """
    for tag in tags:
        if tag.startswith(facet + '.'):
            dot_index = tag.index('.')
            return tag[dot_index+1:]
    return None


def get_all_tags_in_facet(nsg_object, facet, with_facet=False):
    """
    Helper function that returns all tags in given tag facet.

    :param nsg_object:  an object to extract tags from
    :param facet: tag facet
    :param with_facet if True, returns tags including facet, otherwise returns just words.
    :return: (list) a list of all tags in given facet. Returns empty list if the object has
            no tags in given facet
    """
    tags_set = [t for t in nsg_object.tags if t.startswith(facet + '.')]
    if with_facet:
        return tags_set
    return [x.replace(facet + '.', '') for x in tags_set]


class ExtendedTypeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, View):
            return {
                'name': obj.name,
                'parent': obj.parent,
                'hidden': obj.hidden,
                'connecting_devices': obj.connecting_devices,
                'adjacent_devices': obj.adjacent_devices,
                'device_ids': obj.device_ids,
                'device_names': obj.device_names,
            }
        if isinstance(obj, MonitoringDataType):
            return obj.name
        if isinstance(obj, DataSource):
            return obj.name
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

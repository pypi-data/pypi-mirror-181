import argparse
import inspect
import sys

import nsg
from scripts import tags

FORMATS = ['json', 'pb']


def find_class():
    """
    inspect imported module `tags` to find and return class that has method `assign_device_tags`
    """
    klasses = [x[1] for x in inspect.getmembers(tags, inspect.isclass) if hasattr(x[1], 'assign_device_tags')]
    if not klasses:
        return None
    return klasses[0]


def init():
    """
    entry point for initialization. Find class defined in user's script tags.py,
    then create and return an instance. Note that if the class reads some files
    in its constructor, this will happen here.

    :return instance of the class defined in tags.py
    """
    klass = find_class()
    if klass is None:
        raise RuntimeError(
            'Can not find suitable class in module "tags": expected to find class with method "assign_device_tags()"')
    # NET-6822
    # second parameter "graph" has been deprecated, but existing customer's scripts tags.py still have it
    # I can not just drop it from the call because that causes an error. However, our goal is to drop it
    # in the future. Try to call the script with one parameter, but if it fails, call again with two.
    # Scripts in all customer's clusters do not use second parameter so it is safe to pass just None.
    try:
        return klass(nsg.get_log())
    except TypeError as e:
        return klass(nsg.get_log(), None)


def run(user_class_object, device):
    """
    entry point for script tags.py. NSG servers and tests call this function to run this script

    :param user_class_object    instance of the class defined in user's module tags.py
    :param device   input device
    :type device PyDevice
    :return the same device object with updated tags
    """
    if user_class_object is None:
        print('Parameter user_class_object can not be None', file=sys.stderr)
        return None
    if hasattr(user_class_object, 'assign_device_tags'):
        user_class_object.assign_device_tags(device)
    if hasattr(user_class_object, 'assign_interface_tags'):
        user_class_object.assign_interface_tags(device, device.getPyInterfaces())
    if hasattr(user_class_object, 'assign_hw_component_tags'):
        user_class_object.assign_hw_component_tags(device, device.getPyHardwareComponents())
    if hasattr(user_class_object, 'assign_protocol_descriptor_tags'):
        user_class_object.assign_protocol_descriptor_tags(device, device.getPyProtocolDescriptors())
    return device


def script_run(infile, outfile, format):
    input_device = nsg.deserialize_device(infile)
    user_class_object = init()
    updated_device = run(user_class_object, input_device)
    if outfile is None:
        outfile = '-'
    nsg.serialize_device(updated_device, outfile, format)


def main(argv=None):
    # parse cli arguments and deserialize device.
    # when there are no cli parameters, assume the script is loaded by nsg-python-gw which is
    # going to call run() directly
    if not argv or len(argv) <= 1:
        return
    parser = argparse.ArgumentParser(description='NetSpyGlass tags assignment Python application')
    parser.add_argument('-i', '--input_device',
                        help='the file name where input device is stored in json or protobuffer format')
    parser.add_argument('-f', '--format', choices=FORMATS, default='json',
                        help='use this format to generate output (default: json)')
    parser.add_argument('-o', '--output',
                        help='the file name where the result should be stored in json format; '
                             'if missing or equal to "-", use stdout')
    args = parser.parse_args()

    infile = args.input_device
    outfile = args.output

    if infile == outfile:
        print('Output file can not be the same as input file', file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    input_device = nsg.deserialize_device(infile)
    user_class_object = init()
    updated_device = run(user_class_object, input_device)
    if outfile is None:
        outfile = '-'
    nsg.serialize_device(updated_device, outfile, args.format)


if __name__ == "__main__":
    main(sys.argv)

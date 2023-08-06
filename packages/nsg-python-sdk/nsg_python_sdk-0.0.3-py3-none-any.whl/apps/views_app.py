import argparse
import inspect
import json
import sys

import nsg
# import customer's views app. This is supposed to be their "old" script with no changes
from scripts import views

def find_class():
    """
    inspect imported module `tags` to find and return class that has method `execute`
    """
    klasses = [x[1] for x in inspect.getmembers(views, inspect.isclass) if hasattr(x[1], 'execute')]
    if not klasses:
        return None
    return klasses[0]


def init():
    """
    entry point for initialization. Find class defined in user's script views.py,
    then create and return an instance. Note that if the class reads some files
    in its constructor, it happens here.

    This does not call execute() on user's class, it only creates an instance.
    grpc server calls this once and then holds on to the returned object until
    it gets signal to reload Python scripts.

    :return instance of the class defined in views.py
    """
    klass = find_class()
    if klass is None:
        raise RuntimeError(
            'Can not find suitable class in module "views": expected to find class with method "execute()"')
    return klass(nsg.get_log())


def on_next(view_definitions, device):
    # print('<---- device={} views_count={}'.format(device.name, len(view_definitions)))
    for v1 in view_definitions:
        if v1.match_function(device):
            v1.device_ids.append(device.id)
            v1.device_names.append(device.name)


def run(user_class_object, input_devices):
    """
    entry point. NSG servers and tests call this function to run this script

    :param user_class_object instance of user's class defined in their module views.py
    :param input_devices     input devices (iterable of PyDevice)
    :return list of view definitions, including lists of ids of devices that are members of each view
    """
    view_definitions = user_class_object.execute()
    for device in input_devices:
        on_next(view_definitions, device)
    # we have copied device ids into View objects, now we can erase references to matching functions because
    # they are not accessible from outside anyway
    return view_definitions


def script_run(infile, outfile):
    devices = []
    input_device = nsg.deserialize_device(infile)
    devices.append(input_device)
    user_class_object = init()
    generated_views = run(user_class_object, devices)
    output = json.dumps(generated_views, cls=nsg.ExtendedTypeEncoder, sort_keys=True, indent=2, separators=(',', ': '))
    if outfile is None or outfile == '-':
        sys.stdout.write(output)
    else:
        with open(outfile, 'w') as fw:
            fw.write(output)


def main(argv=None):
    # parse cli arguments and deserialize device.
    # when there are no cli parameters, assume the script is loaded by nsg-python-gw which is
    # going to call run() directly
    if not argv or len(argv) <= 1:
        return
    parser = argparse.ArgumentParser(description='NetSpyGlass views assignment Python application')
    parser.add_argument('input_devices', nargs='+',
                        help='file names of input devices in json format')
    parser.add_argument('-o', '--output',
                        help='the file name where the result should be stored in json format; '
                             'if missing or equal to "-", use stdout')

    args = parser.parse_args()

    infiles = args.input_devices
    outfile = args.output
    if not infiles:
        print('Missing input file', file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    devices = []
    for infile in infiles:
        if not infile:
            continue
        if infile == outfile:
            print('Output file can not be the same as input file', file=sys.stderr)
            parser.print_help()
            sys.exit(1)
        input_device = nsg.deserialize_device(infile)
        devices.append(input_device)
    user_class_object = init()
    generated_views = run(user_class_object, devices)
    output = json.dumps(generated_views, cls=nsg.ExtendedTypeEncoder, sort_keys=True, indent=2, separators=(',', ': '))
    if outfile is None or outfile == '-':
        sys.stdout.write(output)
    else:
        with open(outfile, 'w') as fw:
            fw.write(output)


if __name__ == "__main__":
    main(sys.argv)



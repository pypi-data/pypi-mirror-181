from net.happygears.nw2.py.py_wrappers.py_device import PyDevice


class TagSelector(object):
    """
    Tag selector Python hook. This class is provided for backward compatibility with
    Python scripts `tags.py` that assume there is base class TagSelector even though
    this class does not really do anything.

    This class defines expected set of functions in the customer's tag selector class.
    """

    def __init__(self, log, _=None):
        """
        # NET-6822
        # second parameter "graph" has been deprecated, but existing customer's scripts tags.py still have it
        # and use this class as their base class so they call super() with two parameters.
        """
        self.log = log

    def assign_device_tags(self, device):
        """
        Analyze the device and add or remove tags. Device passed as argument
        already has implicit (automatic) tags set by the system. This function
        can modify them or add new ones by adding strings to the attribute
        'tags' (a set of strings). Each added tag must conform to the format
        "TagFacet.word". For example, to add a new tag to the device, just
        add string to `device.tags`::

            device.tags.add('MyTagFacet.Word')

        Default implementation of this function does nothing. To add
        user-defined tags, create your own class derived from :class:`TagSelector`
        and override this function.

        :param device:  an :class:`net.happygears.nw2.py.py_wrappers.PyDevice` object
        """
        assert isinstance(device, PyDevice)
        pass

    def assign_interface_tags(self, device, interfaces):
        """

        Analyze interface objects in list "interfaces" (parent device object
        is also provided as argument "device") and add or remove tags. Both
        device and interfaces already have implicit (automatic) tags added
        by the system when they are passed to this function. Function
        "assign_device_tags()" has already been called on the device, too.
        Tags are copied to monitoring variables later when the server creates
        them.

        This function can add, remove or modify tags using attribute "tags"
        (a set of strings). Each added tag must conform to the format
        "TagFacet.word"

        Default implementation of this function does nothing. To add
        user-defined tags, create your own class derived from :class:`TagSelector`
        and override this function.

        One of the intended purposes of this function is to parse interface
        description and generate tags.

        :param device:   instance of class `PyDevice`
        :param interfaces:  list of :class:`net.happygears.nw2.py.py_wrappers.PyNetworkInterface` objects
        """
        pass

    def assign_hw_component_tags(self, device, components):
        """

        Analyze objects in the list "components" (parent device object
        is also provided as argument "device") and add or remove tags. Both
        device and components already have implicit (automatic) tags added
        by the system when they are passed to this function. Function
        "assign_device_tags()" has already been called on the device, too.
        Tags are copied to monitoring variables later when the server creates
        them.

        This function can add, remove or modify tags using attribute "tags"
        (a set of strings). Each added tag must conform to the format
        "TagFacet.word"

        Default implementation of this function does nothing. To add
        user-defined tags, create your own class derived from :class:`TagSelector`
        and override this function.

        :param device:   instance of class `PyDevice`
        :param components:  list of :class:`net.happygears.nw2.py.py_wrappers.PyHardwareComponent` objects
        """
        pass

    def assign_protocol_descriptor_tags(self, device, components):
        """
        Analyze and manipulate tags on objects in the list "components" where
        each item is an object of class :class:`net.happygears.nw2.py.py_wrappers.PyProtocolDescriptor`.
        This class is an abstraction that is used to describe a parameter or a counter
        of a protocol. NetSpyGlass automatically adds tags to these objects when
        they are created; this function can analyse and manipulate those tags.

        Both device and components already have implicit (automatic) tags added
        by the system when they are passed to this function. Function
        "assign_device_tags()" has already been called on the device, too.
        Tags are copied to monitoring variables later when the server creates
        them.

        This function can add, remove or modify tags using attribute "tags"
        (a set of strings). Each added tag must conform to the format
        "TagFacet.word".

        Default implementation of this function does nothing. To add
        user-defined tags, create your own class derived from :class:`TagSelector`
        and override this function.

        :param device:   instance of class `PyDevice`
        :param components:  list of :class:`net.happygears.nw2.py.py_wrappers.PyProtocolDescriptor` objects
        """
        pass

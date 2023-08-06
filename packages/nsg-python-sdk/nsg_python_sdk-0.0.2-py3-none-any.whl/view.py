"""
 Copyright (C) 2022 HappyGears - All Rights Reserved

 Unauthorized copying of this file, via any medium is strictly prohibited.
 Proprietary and confidential

 DO NOT MODIFY ! This file is part of the distribution and may change in the future versions.

"""


class View(object):
    """
    This class describes a view.

    :param view_dict:  a dictionary that describes the view. Allowed keys are: 'name',
                       'parent', 'match_function', 'connecting_devices', 'adjacent_devices'

    Alternatively, all parameters that describe the view can be provided as arguments:

    :param name: view name
    :param parent: the name of the parent view
    :param match_function: python function that will be called with one parameter (:class:`PyDevice` object)
                            to determine if a device should be a member of the view. The function should return
                            True or False
    :param intf_match_function: python function that will be called with two parameters: :class:`PyDevice` object
                            and :class:`PyNetworkInterface` object. It should decide if the interface should be
                            a member of the view. The function should return True or False
    :param connecting_devices:  (boolean) if True, the view will also include devices that
                   connect devices that match this view. Default value is False.
    :param adjacent_devices: (boolean) if True, the view will also include devices one hop away
                   from the devices that match this view. If this parameter is missing,
                   its value is set to False

    Examples::

        v = View({
            'name': 'view_name',
            'matching_function': lambda host: host in ['host_foo', 'host_bar']
        })

        v = View(name='view_name', matching_function=lambda host: host in ['host_foo', 'host_bar'])

    """

    def __init__(self, *args, **kwargs):
        view_dict = {}
        if args:
            view_dict = args[0]
        if kwargs:
            view_dict = kwargs
        self.name = view_dict.get('name', 'no_name')
        self.parent = view_dict.get('parent', '')
        self.rule = None
        self.match_function = view_dict.get('match_function', lambda x: True)
        self.intf_match_function = view_dict.get('intf_match_function', lambda x, y: True)
        self.last_updated = 0
        self.parameters = {}
        self.hidden = view_dict.get('hidden', False)
        self.connecting_devices = view_dict.get('connecting_devices', False)
        self.adjacent_devices = view_dict.get('adjacent_devices', False)
        # dictionary <parameters> is essentially a copy of the original dict the view object has been built from
        for item in list(view_dict.keys()):
            self.parameters[item] = view_dict.get(item)
        # list of ids of devices that are members of this view
        self.device_ids = []
        # list of names of devices that are members of this view (used mostly for tests)
        self.device_names = []

    def match(self, host):
        """
        This function calls `match_function` to determine if given host should belong to this view

        :param host:  an instance of class Host (see above)
        :return:  True if the host belongs here
        """
        return self.match_function(host)

    def __str__(self):
        return str(self.__dict__)

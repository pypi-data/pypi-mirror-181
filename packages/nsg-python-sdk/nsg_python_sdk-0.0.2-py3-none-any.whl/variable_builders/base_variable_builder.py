"""
Copyright (C) 2022 HappyGears - All Rights Reserved

Unauthorized copying of this file, via any medium
is strictly prohibited. Proprietary and confidential

DO NOT MODIFY ! This file is part of the distribution
and may change in the future versions.

"""


class BaseVariableBuilder(object):
    """
    This class is used to build monitoring variables
    """
    def __init__(self, log):
        self.log = log

    def make_variables(self, device, component):
        return {}

#!/usr/bin/python

from ansible.errors import (
    AnsibleFilterTypeError
)
import re


def convert_mac(var_a):
    '''
        convert mac string
    '''
    if not isinstance(var_a, str):
        raise AnsibleFilterTypeError("String type is expected, "
                                     "got type %s instead" % type(var_a))
    if not re.search('^[0-9A-Fa-f]{12}$', var_a):
        raise AnsibleFilterTypeError("Wrong format")


    return (re.sub(r'(.{2})', r'\1:', var_a)[:-1]).upper()


class FilterModule(object):
    def filters(self):
        return {
            'convert_mac': convert_mac
        }

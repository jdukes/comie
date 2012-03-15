#!/usr/bin/env python
"""This is an *actually* pythonic way to access (read from, add write
functionality later) the registry
"""

from _winreg import *
from os.path import join as pjoin

class _base:

    def __init__(self):
        pass

    def get_subkey(self, path):
        return Key(path, self)

class Value:

    def __init__(self, name, content, vtype):
        self.name = name.strip() or "@" 
        self.content = content
        self.vtype = vtype

    def __repr__(self):
        return "<key value of %s is %s of type %s>" % (self.name,
                                                       self.content,
                                                       self.vtype)
        
class Key(_base):
    """ Keys don't exist without a parent registry connection. 
    """

    def __init__(self, path, _parent):
        self._parent = _parent
        self.con = OpenKey(self._parent.con, path)
        if "path" in _parent.__dict__:
            self.path = pjoin(self._parent.path, path)
        else:
            self.path = path
        self.name = path.split('\\')[-1]
        self.num_keys, self.num_values, self.last_mod = \
                       QueryInfoKey(self.con)
        
    def get_values(self):
        for i in range(self.num_values):
            yield Value(*EnumValue(self.con,i))

    def get_subkeys(self):
        for i in range(self.num_keys):
            subkey = EnumKey(self.con,i)
            yield Key(subkey, self)

    def create_subkey(self, subkey):
        path = self.path + subkey
        return CreateKey(self.con, path)

    def set_value(self, subkey, vtype, value):
        SetValue(self.con, subkey, vtype, value)

    def delete_subkey(self, subkey):
        DeleteKey(self.con, subkey)

    def delete_value(self, value):
        DeleteValue(self.con, value)

    def flush(self):
        FlushKey(self.con)

    def close(self):
        self.flush()
        CloseKey(self.con)

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def __repr__(self):
        return "<Registry Key %s>" % self.path

    

class Registry(_base):
    """ Connection to the registry.
    """
    def __init__(self, root):
        self.root = root
        self.con = ConnectRegistry(None,root)
        
    
    def __repr__(self):
        return "<Registry connection to %s>" % self.root

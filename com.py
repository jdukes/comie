#!/usr/bin/env python

from comtypes.client import GetModule, CreateObject

from registry import Registry, HKEY_CLASSES_ROOT

reg = Registry(HKEY_CLASSES_ROOT)

class Com:

    def __init__(self, clsid):
        self.clsid = clsid
        self.clsid_key = reg.get_subkey("CLSID\\" + clsid)
        for value in self.clsid_key.get_values():
            if value.name == "@":
                self.name = value.content
            if value.name.lower() == "appid":
                self.AppID = value.content
                map( lambda v: self._setattr_(v.name, v.content),
                     ( val for val in
                       reg.get_subkey("AppID\\" + self.AppID).get_subkeys()))
        for key in self.clsid_key.get_subkeys():
            if key.name.lower() == "interface":
                self.interface = key.values()
            if key.name.lower() == "control":
                self.is_control = True
            if key.name.lower() == "programmable":
                self.is_activex = True
            if key.name.lower() == "implemented categories":
                self.implemented_categories = [ k.name for k in key.get_subkeys()]
                
            if key.name.lower() == "typelib":
                self.typelib_guid = key.get_value().content
                self.typelib_key = reg.get_subkey("TypeLib\\" +
                                                  self.typelib_guid)
                self.typelib_files = []
                for ver in self.typelib_key.get_subkeys():
                    for sv in ver.get_subkeys():
                        if sv.num_keys:
                            for arch in sv.get_subkeys():
                                v = arch.get_value().content #fix this awefulness
                                self.typelib_files.append(v)
                                GetModule(v)
                try:
                    self.obj = CreateObject(self.clsid)
                    self.methods = [ (name,args) for r,name,args,arg_names,n,n2
                                     in self.obj._methods_ ]
                except WindowsError:
                    self.obj = "could not be instantiated"

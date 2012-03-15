#!/usr/bin/env python

from comtypes.client import GetModule, CreateObject

from registry import Registry, HKEY_CLASSES_ROOT

reg = Registry(HKEY_CLASSES_ROOT)

#{03837511-098B-11D8-9414-505054503030}

class Com:

    def __init__(self, clsid):
        self.clsid = clsid
        clsid_key = reg.get_subkey("CLSID\\" + clsid)
        for value in clsid_key.get_values():
            if value.name == "@":
                self.name = value.content
            if value.name.lower() == "appid":
                self.AppID = value.content
                map( lambda k, v: self._setattr_(k, v),
                     (val.name, val.value) for val in
                     reg.get_subkey("AppID\\" + self.AppID))

        for key in clsid_key.get_subkeys():
            if key.name.lower() == "interface":
                self.interface = key.values()
            if key.name.lower() == "control":
                self.is_control = True
            if key.name.lower() == "programmable":
                self.is_activex = True
            if key.name.lower() == "typelib":
                self.typelib_guid = key.get_value()
                typelib_key = reg.get_subkey("TypeLib\\" +
                                             self.typelib_guid)
                for ver in typelib_key.get_subkeys():
                    GetModule(ver.get_subkey('0'))
                        
                        
                        


            
        
        #[k for k in get_subkeys("CLSID\\%s\InprocServer32" % z) ]
    #get_values("CLSID\\%s\\TypeLib" % clsid)

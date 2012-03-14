#!/usr/bin/env python

import comtypes.client 
from registry import Registry


reg = Registry(HKEY_CLASSES_ROOT)

class Com:

    def __init__(self, clsid):
        self.clsid = clsid
        clsid_key = reg.get_subkey("CLSID\\" + clsid)
        for value in clsid_key.get_values():
            if value.name == "@":
                self.name = value.content
            if value.name.lower() == "appid":
                self.AppID = value.content
        for key in clsid_key.subkeys():
            pass
            
        
        #[k for k in get_subkeys("CLSID\\%s\InprocServer32" % z) ]
    #get_values("CLSID\\%s\\TypeLib" % clsid)

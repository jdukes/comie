#!/usr/bin/env python

from comtypes.client import GetModule, CreateObject

from registry import Registry, HKEY_CLASSES_ROOT

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
        for key in clsid_key.get_subkeys():
                    if key.name == "Interface":
                        print "Interface", key.values()
                        print '#'*80
                    if key.name == "AppID":
                        app_id = key.values()
                        print "AppID", app_id
                        print "human readable AppID", reg.get_subkey("CLSID\\" + clsid
                                                                 + '\\AppID\\' )
                        print '#'*80
                    if key.name == "Control":
                        print "is Control"
                        print '#'*80
                    if key.name == "Programmable":
                        print "is ActiveX"
                        print '#'*80

            
        
        #[k for k in get_subkeys("CLSID\\%s\InprocServer32" % z) ]
    #get_values("CLSID\\%s\\TypeLib" % clsid)

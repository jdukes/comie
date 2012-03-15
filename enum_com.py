#!/usr/bin/env python

import os
import sys

import com
from registry import Registry, HKEY_CLASSES_ROOT


OUTPUT_DIR = "c:\\com_enum\\"
CLSID_LOG = OUTPUT_DIR + 'clsid_snap.log'
APPID_LOG = OUTPUT_DIR + 'appid_snap.log' 

reg = Registry(HKEY_CLASSES_ROOT)

def snapshot():
    if not os.path.exists(OUTPUT_DIR) or \
           not os.path.exists(CLSID_LOG) or \
           not os.path.exists(APPID_LOG):
        try:
            os.mkdir(OUTPUT_DIR)
        except Exception, e:
            print "Failed attempting to create output directory."
            print "If this path already exists it could be overwritten."
            print "If this is expected please remove the path and run again"
        clsid_snap = open(CLSID_LOG,'w')
        appid_snap = open(APPID_LOG,'w')
        [clsid_snap.write(k.name.lower() +'\n') for k in reg.get_subkey('CLSID').get_subkeys()]
        clsid_snap.close()
        [appid_snap.write(k.name.lower()+'\n') for k in reg.get_subkey('APPID').get_subkeys()]
        appid_snap.close()
        print "initial snapshot taken. Install, reboot, and run again."
        sys.exit(0)
    else:
        clsid_snap = open(CLSID_LOG,'r+')
        appid_snap = open(APPID_LOG,'r+')
        new_clsids = set(k.name.lower() for k in reg.get_subkey('CLSID').get_subkeys()).difference(
            k.strip() for k in open(CLSID_LOG))
        new_appids = set(k.name.lower() for k in reg.get_subkey('APPID').get_subkeys()).difference(
            k.strip() for k in open(APPID_LOG))
        for f,l in ((clsid_snap,new_clsids),(appid_snap,new_appids)):
            f.seek(0)
            f.truncate()
            [ f.write(k +'\n') for k in l ]
        stat_file = open(OUTPUT_DIR + 'stat','w')
        stat_file.write('snapshot_finished')
        stat_file.close()
        
#clsid_snap.next().strip()



def main():
    if not os.path.exists(OUTPUT_DIR) or \
       not os.path.exists(OUTPUT_DIR + 'stat'):
        print "snapshotting"
        snapshot() #quits if first run, runs through if second
        print "complete"
    
        

if __name__ == "__main__":
    main()

#GetModule(tlib)

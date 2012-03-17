#!/usr/bin/env python

import sys
import os
from time import sleep
from subprocess import Popen,PIPE

accesschk = 'C:\\SysinternalsSuite\\accesschk.exe'
if not os.path.exists(accesschk):
    print "get accesschk from sysinternals and place in %s" % accesschk
    exit(1)

def access_check(name, flags=[]):
    args = [accesschk,'-q']
    args.extend(flags)
    args.append(name)
    proc = Popen(args, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = proc.communicate()
    log.write(stdout + "\n")
    # log.write('"%s","%s","%s"\r\n' %
    #           (name,
    #            ":".join( stdout.replace('"','\\"').split('\r\n')[1:]),
    #            stderr.replace('\r\n',':')))


#log = open('dacl_check.csv', 'w')
log = open('dacl_check.log', 'w')

#log.write('"File","stdout","stderr"\r\n')

if len(sys.argv) < 2:
    print "usage: %s name_of_regshot_file" % sys.argv[0]
    sys.exit(1)

fd = open(sys.argv[1])
buff = fd.read(1024) # fd.read() works on Linux, seems to be buggy
                         # on this python on Windows
diff = ""
while buff:
    diff += buff
    buff = fd.read(1024)
    
diff = diff.split('----------------------------------')
diff = dict( (diff[x].strip().split(':')[0],
              diff[x+1].strip().split('\n'))
             for x in xrange(1,len(diff), 2)
             if diff[x+1].strip() )

if 'Keys added' in diff:
    keys_to_check = diff['Keys added']

for k in ['Values added','Values Added', 'Values modified']:
    if k in diff:
        keys_to_check.extend(okv[0]
                             for okv in ( kv.split(':') for kv in diff[k] )
                             if len(okv) > 1)

files_to_check = []
for k in ['Files added', 'Files [attributes?] modified', 'Folders added']:
    if k in diff:
        files_to_check.extend(diff[k])


for f in files_to_check:
    access_check(f)

for k in keys_to_check:
    access_check(k, ['-k'])

log.flush()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Module containing the procedures to handle server management
    with ssh on the commandline. 
"""   
##### Avoid pydoc errors
import sys
try:
  from __main__ import prgdir,prgname
  import os.path
  exec(open(os.path.join(prgdir,prgname+"_imp.py")).read())
except:
  if sys.argv[0].find('pydoc'):
    pass # we are running from pydoc3

##### Module Start
### -------------------------------------------------------------------
def check_conn(hosts,user,kwdict):
  from __main__ import dbg,prgargs,cfg
  """ Executes a simple testprogramm on all hosts in parallel with 
  minimal timeout values. In case of errors shows the same messages
  the usual run would show.
  """    
  dbg.entersub()
  hosts_avail = []
  now = datetime.datetime.now().time()
  dbg.dprint(1,"start =", now)
  ### strange thing: if the first host of the list is unknown, the program runs, 
  ### completes with no error, but python throws a SIGSEGV double_free() 
  ### after successful exit.
  ### added 127.0.0.1 as the first host and objectcounter to work around that     
  testhosts = ['127.0.0.1'] + hosts 
  objc = 0   
  client = ParallelSSHClient(testhosts,user=user,allow_agent=False,**kwdict,
           num_retries=0, timeout=cfg.data.chktimeout)
  output = client.run_command(cfg.argdefaults.cmd,
           timeout=int(cfg.data.chktimeout),
           stop_on_errors=False, return_list=True)
  for obj in output:
    testout = ""
    host = obj.host
    # dbg.dprint(0,host) 
    if obj.channel is None:
      if not ( host == '127.0.0.1' and objc == 0 ):
        rxe2_mod_general.print_hostline(client.user,host,'conncheck','')
        if obj.exception is not None:
          rxe2_mod_parallel.handle_pssh_errors(obj.exception, host)
      continue
    try:
      testout = list(obj.stdout)
    except Exception as e:  
      if not ( host == '127.0.0.1' and objc == 0):
        rxe2_mod_general.print_hostline(client.user,host,'conncheck','')
        rxe2_mod_parallel.handle_pssh_errors(e, host)
      continue

    if not ( host == '127.0.0.1' and objc == 0 ):
      hosts_avail.append(host) 
    objc += 1
  
  client = None
  del client
  now = datetime.datetime.now().time()
  dbg.dprint(1,"end =", now)
  dbg.leavesub()
  return(hosts_avail)

### -------------------------------------------------------------------

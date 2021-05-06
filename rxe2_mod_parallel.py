#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Module containing the procedures to handle ssh runs for rxe.
    all pssh stuff is in here
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
def copy_cmd(client,copy,cmd,timeout):
  from __main__ import dbg,cfg
  """ Copy the local commandfile to remote:/tmp 
      no error handling is done here, instead a conncheck is done
      before copy. See also: rxe2_conncheck 
  """    
  dbg.entersub()
  now = datetime.datetime.now().time()
  dbg.dprint(1,"start =", now)
  greenlets = client.scp_send(copy,cmd)
#    for g in greenlets:
#      if not g.successful():
#        dbg.dprint(256, g.name, "failed" )
#      print("Parent:",g.parent)
#      print("get   : ", g.get())
#      print("name  : ", g.name) 
#      print("succ  : ", g.successful()) 
#      print("dir   :" ,dir(g),"\n")
  joinall(greenlets, raise_error=True,timeout=cfg.data.cptimeout)
#  except Exception as e:
#    dbg.dprint(256, "Fail on copy", e)
  now = datetime.datetime.now().time()
  dbg.dprint(1,"end =", now)
  dbg.leavesub()

### -------------------------------------------------------------------
def handle_pssh_errors(error,host):
  """ Try to handle errors from pssh, error messages can be extended
  by using any number >0 for  -d 
  """
  from __main__ import dbg,loguru,cfg,prgargs
  hlen = cfg.data.hlen
  dbg.entersub()
  errormsg = f"ERROR: {error}"
  #dbg.dprint(2, type(error))
  if type(error) is pssh.exceptions.ConnectionErrorException:
    line = "--- NO CONNECTION, HOST DOWN? ---" 
  elif type(error) is pssh.exceptions.UnknownHostException:
    line = "--- NO CONNECTION, unknown HOST ---"
  elif type(error) is pssh.exceptions.Timeout:
    line = "--- TIMEOUT after " + str(prgargs.tmout) + " seconds --- "
  elif type(error) is pssh.exceptions.AuthenticationException:
    line = "--- AUTH ERROR ---"
  elif type(error) is ssh2.exceptions.SocketRecvError:
    line = "--- SSH RECV ERROR ---"
  else:
    line = f"Unknown error of type: {type(error)}" 

  if (dbg.lvl) > 0:
    line += "\n" + errormsg

  dbg.dprint(256,line)
  loguru.logger.info(f"{host:{hlen}} | {line}")
  dbg.leavesub()

### -------------------------------------------------------------------
def show_output(client,output,cmd,opts):
  """ Show the commands output and print exceptions
  """
  from __main__ import dbg,cfg
  hlen = cfg.data.hlen
  dbg.entersub()
  #dbg.dprint(0,type(output),"output[0]",output[0])
  for obj in output:
    #dbg.dprint(0, obj,"\nType:",type(obj))
#    testout = ""
    host = obj.host
    rxe2_mod_general.print_hostline(client.user,host,cmd,opts)
    ### In case there is no channel, continue  
    if obj.channel is None:
      dbg.dprint(0,"No Channel set up")
      if obj.exception is not None:
        dbg.dprint(0,"But got exception")
        handle_pssh_errors(obj.exception, host) 
      continue
    #dbg.dprint(0,"obj.stdout", obj.stdout,"\nType:",type(obj.stdout))
    #dbg.dprint(0,"obj.client", type(obj.client))
    #testout = None
    read = []
    try:
      for line in obj.stdout:
        read.append(line)
    except Exception as e:  
      handle_pssh_errors(e, host)
      dbg.dprint(0,"exit_code was",obj.exit_code)
      obj.client.close_channel(obj.channel)
      #client.host_clients[host].close_channel(obj.channel)
#    else:
    loguru.logger.info(f"{client.user}@{host:25} P {cmd} {opts}")
    exitline = f"  -- Exit Code: {obj.exit_code:3}, Exception: '{obj.exception}'"
    loguru.logger.info(exitline)
    if obj.exit_code is not None and obj.exit_code != 0 :
      dbg.dprint(256,exitline)
    if len(read):
      for line in read:
        print(f"{line}") 
        loguru.logger.info(f"  -- OUT: {line.rstrip()}")
    else:  
      line = "  -- NO OUTPUT --"
      dbg.dprint(0,line)
      loguru.logger.info(f"{line}")

  dbg.leavesub()  
### -------------------------------------------------------------------

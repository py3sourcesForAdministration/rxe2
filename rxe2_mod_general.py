#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Module containing the procedures to run prgname.py
"""   
##### Avoid pydoc errors
import os, os.path, sys
try:
  from __main__ import prgdir,prgname
  import os.path
  exec(open(os.path.join(prgdir,prgname+"_imp.py")).read())
except:
  if sys.argv[0].find('pydoc'):
    pass # we are running from pydoc3
##### Module Start
###-------------------------------------------------------------------------
def get_files(path):
  """ return list of files found in path """
  from __main__ import dbg 
  dbg.entersub()
  knownfiles = {}
  for top, dirs, files in os.walk(path):
    for nm in files:
      path = os.path.join(top, nm)
      name = os.path.basename(path)
      knownfiles[name] = path

  dbg.leavesub()
  return knownfiles    

###-------------------------------------------------------------------------
def handle_fdict(namelist,filedict,type=None):
  """ compare a list of names to a dictionary with teh available names
  as keys. a type for the comparison must be given: 1by1, single or items.
  Returns a list of matching items.
  """
  from __main__ import dbg 
  dbg.entersub()
  result = []
  dbg.dprint(2,"type",type, namelist)
  for n in namelist:
    new = n.split(',')
    for name in new:
      if not name:
        continue
      dbg.dprint(2,name)
      if name in filedict:
        if type == '1by1':
          with open(filedict[name],'r') as f:
            for line in f:
              if line.startswith('#'):
                continue
              else:
                result.append(line.strip())
        elif type == 'single':
          result = filedict[name]
        elif type == 'items':
          result.append(filedict[name])
        else :
          print("not yet done")
      else:
        result.append(name)

  dbg.leavesub()
  return result  

###-------------------------------------------------------------------------
def buildlist(namelist,search,type=None):
  """ take a list of names and search for files with this name 
   if a file exists append content to the returnlist 
  """
  from __main__ import dbg
  dbg.entersub()
  reslist = [] 
  filedict = get_files(search)
  reslist = handle_fdict(namelist,filedict,type=type)

  dbg.leavesub()
  return sorted(set(reslist)) 

###-------------------------------------------------------------------------
def list_cmds(fdict):
  """ prints out the list of found commands "rxe -lc" 
  """
  from __main__ import dbg
  dbg.entersub()
  newdict = {}
#  dbg.dprint(0,fdict)
  for k,v in fdict.items():
    group = os.path.basename(os.path.dirname(v))
    if os.access(v, os.X_OK):
      newdict[group]    = newdict.get(group,{})
      newdict[group][k] = newdict[group].get(k,1)
#  dbg.dprint(0, newdict)
  for g in sorted(newdict.keys()):
    print(f"- {g}")
    for c in sorted(newdict[g].keys()):
      print(f"    ->    {c}")
  dbg.leavesub()  
  sys.exit(0)

###-------------------------------------------------------------------------
def list_hosts():
  """ prints out the list of found hostfiles "rxe -lh" 
  """
  from __main__ import dbg,cfg 
  dbg.entersub()
  fdicth = get_files(cfg.data['nodefiles'])
  for k in sorted(set(fdicth)):
    print(f"--- {k}")
  dbg.leavesub()  
  sys.exit(0)

###-------------------------------------------------------------------------
def setup_logging():
  """ Initialize loguru log
  """
  from __main__ import dbg,prgargs,prgdir
  dbg.entersub()
  loguru.logger.remove()
  if prgargs.log:
    logname = prgargs.cmd.replace(' ','_') 
    loguru.logger.add(os.path.join(prgdir,'logs',logname + ".log"),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:7} | {message}")
  dbg.leavesub()

###-------------------------------------------------------------------------
def print_hostline(user,host,cmd,opts):
  """ Just print user@host and command 
  """
  from __main__ import dbg,cfg
  rst = cfg.data.colors.rst
  fgy = cfg.data.colors.fgy
  fgg = cfg.data.colors.fgg
  print(f"{fgg}--------------- {user}@{host:25} {cmd} {opts}{rst}")

###-------------------------------------------------------------------------
def print_error(host,e):
  """ print error """  
  from __main__ import dbg, cfg
  hlen = cfg.data.hlen
#  line = "--- NO CONNECTION, MAYBE AUTH OR HOSTNAME PROBLEM ---"
  dbg.dprint(256,e)
  loguru.logger.error(f"{host:{hlen}} | {e}")
###-------------------------------------------------------------------------
def print_log(host,e):
  """ print error """  
  from __main__ import dbg,cfg
  hlen = cfg.data.hlen
#  dbg.dprint(0, e)
  loguru.logger.info(f"{host:{hlen}} | {e}")
###-------------------------------------------------------------------------

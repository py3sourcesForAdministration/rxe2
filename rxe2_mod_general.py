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
  from __main__ import dbg,prgargs,prgdir,prgname
  dbg.entersub()
  loguru.logger.remove()
  logfile = os.path.join(prgdir,'logs',prgname + ".log")
  if prgargs.log:
    #logname = prgargs.cmd.replace(' ','_') 
    ### rotate if already to big
    if os.path.isfile(logfile) and os.path.getsize(logfile) > 1000000 :
      from datetime import date
      currdate = date.today().strftime("%Y-%m-%d") 
      move_to = os.path.join(prgdir,'logs',currdate+"_"+prgname+".log")
      os.rename(logfile,move_to)
    ### init log
    loguru.logger.add(logfile,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:7} | {message}")
  dbg.leavesub()
  return(logfile)

###-------------------------------------------------------------------------
def prnout(typ,*args):
  """ print output to stdout and depending on type:
      hostline:                  'h',user,host,cmd
      error   :                  'e',other args  # first one red
      warning :                  'w',all args    # all yellow
      info    :                  'i',all args    # all normal
  """
  from __main__ import dbg,cfg
  rst = cfg.data.colors.rst
  fgy = cfg.data.colors.fgy
  fgg = cfg.data.colors.fgg
  fgr = cfg.data.colors.fgr
  hlen = cfg.data.hlen
  line = f"error in args to print: {' '.join(args)}"  
  if typ.startswith( 'h' ):          
    line = f"{fgg}--------------- {args[0]}@{args[1]:{hlen}} {args[2]}{rst}"
    loguru.logger.info(line)
  elif typ.startswith('e'):
    line = f"{fgr}{args[0]}{rst} | " + " ".join(args[1:])
    loguru.logger.error(line)
  elif typ.startswith('i'):
    line = f"{' '.join(args)}"
    loguru.logger.info(line)
  elif typ.startswith('w'):
    line = f"{fgy}{args[0]}{rst} | " + " ".join(args[1:])
    loguru.logger.warning(line)
  else:
    dbg.dprint(0,line,args)
    return
  print(line)    

###-------------------------------------------------------------------------
def log_and_cleanup(lfile):
  from __main__ import dbg,cfg,prgargs
  import re
  iserr = ''
  if os.path.isfile(lfile):
    if re.search('err',lfile):
      iserr = 'stderr: '
    if prgargs.log:
      with open(lfile) as f:
        for line in f: 
          loguru.logger.info(f"{iserr}{line.rstrip()}")
    os.remove(lfile)
###-------------------------------------------------------------------------

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Docstring: replace
"""
import os, os.path, sys, checkenv
libdir         = checkenv.chk_sufficient()
prgname,prgdir = checkenv.get_names(__file__)

###########   M A I N   #######################################################
def main():
  """ Main part for doing the work
  """
  import os
  from rxe2_mod_general import prnout
  dbg.entersub()
  user    = prgargs.user
  cmd     = prgargs.cmd
  tmout   = prgargs.tmout
  fdict1  = rxe2_mod_general.get_files(os.path.join(prgdir,'cmdfiles.example'))
  fdict   = { **fdict1,  **rxe2_mod_general.get_files(cfg.data['cmdfiles'])}
  ### Stop if only listing is wanted
  if prgargs.listcmds:
    rxe2_mod_general.list_cmds(fdict) 
  if prgargs.listhosts:
    rxe2_mod_general.list_hosts()
  ### otherwise continue with other options  
  logfile = rxe2_mod_general.setup_logging()  
  ### evaluate hosts to hostlist
  hosts     = rxe2_mod_general.buildlist(prgargs.srv,cfg.data['nodefiles'],type='1by1')
  ### password or key ?
  kwdict = { 'username'     : user }
  if prgargs.password:
    kwdict['password'] = prgargs.password 
  if prgargs.identity:
    kwdict['client_keys'] = [prgargs.identity]
  ### prepare command  
  copy = ''

  if prgargs.cmd:
    if prgargs.cmd in fdict:
      copy = fdict[prgargs.cmd]
      cmd  = '/tmp/'+prgargs.cmd
    elif prgargs.cmd.startswith('./'):
      copy = prgargs.cmd
      basename = os.path.basename(copy)
      cmd  = '/tmp/'+basename
  ### prepare commandline opts
  opts = '' 
  if prgargs.opts:
    opts = ' '.join(prgargs.opts)
  ### debug print what is done already
  dbg.dprint(2,"user    =",user)
  dbg.dprint(2,"hosts   =",hosts)
  dbg.dprint(2,"cmd     =", cmd)
  dbg.dprint(2,"copy    =", copy)
  dbg.dprint(2,"opts    =", opts)
  dbg.dprint(2,"timeout =", tmout)
  dbg.dprint(2,"kwdict  =", kwdict)

  start = datetime.datetime.now()
  ### Do connection check if copy i not set
  if not copy:
    availhosts = asyncio.get_event_loop().run_until_complete(
            rxe2_mod_async.run_mcmds(hosts,cfg.data.chkcmd,
                 max(tmout/4,cfg.data.conntm),**kwdict))
  else:
    availhosts = asyncio.get_event_loop().run_until_complete(
            rxe2_mod_async.run_mcopy(hosts,copy,cmd,**kwdict))
  dbg.dprint(1,"Started with number of hosts:",len(hosts))
  dbg.dprint(1,"leftover hosts to execute   :",len(availhosts))
  missing = set(hosts) - set(availhosts)
  ### Start for available hosts
  sys.stdout.flush()
  sys.stderr.flush()
  sys.stdin.flush()
  if len(availhosts) > 0 and len(cmd):
    ##### ----- Start of interactive -------------------------------------------
    if prgargs.interactive :
      for host in hosts:
        prnout('h',user,host,cmd,opts)
        target   = user+ '@' +host
        execcmd = ' '.join(['(','ssh','-tt',target,'"',cmd,opts,'"',cfg.data.redirect])
        res = os.system(execcmd)
        prnout('i','exit_code:',str(res))
        rxe2_mod_general.log_and_cleanup(cfg.data.cap_out) 
        rxe2_mod_general.log_and_cleanup(cfg.data.cap_err) 
    ##### ----- Start of parallel ----------------------------------------------
    else:
      asyncio.get_event_loop().run_until_complete(
          rxe2_mod_async.run_mcmds(availhosts,cmd+" "+opts,tmout,**kwdict))
    ##### ----- End of command execution ---------------------------------------
    ### cleanup
    if copy:
      asyncio.get_event_loop().run_until_complete(
          rxe2_mod_async.run_mcmds(availhosts,"rm "+cmd,tmout,**kwdict))
    ### End of available hosts

  end = datetime.datetime.now()
  dbg.leavesub()
  print()
  dbg.dprint(0,"Took",end -start,"to execute") 
  if (len(missing)): 
    dbg.dprint(0,"Skipped unconnectable Hosts:",missing)
###########   D E F A U L T   I N I T   #######################################
if __name__ == "__main__":
  from mydebug.py3dbg import dbg
  from myconf.py3cfg  import init_cfg
  cfg = init_cfg(prgname,prgdir,libdir,dbg)
  exec(cfg.imports)
  exec(cfg.usage)
  main()

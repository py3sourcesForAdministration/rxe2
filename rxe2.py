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
  dbg.entersub()
  user    = prgargs.user
  cmd     = prgargs.cmd
  timeout = prgargs.tmout
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
  kwdict = { 'pkey'     : prgargs.identity }
  if prgargs.password:
    kwdict = { 'password' : prgargs.password }
  ### prepare command  
  copy = ''
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
  dbg.dprint(2,"user   =",user)
  dbg.dprint(2,"hosts  =",hosts)
  dbg.dprint(2,"cmd    =", cmd)
  dbg.dprint(2,"copy   =", copy)
  dbg.dprint(2,"opts   =", opts)
  dbg.dprint(2,"kwdict =", kwdict)

  start = datetime.datetime.now()
  ### Do connection check always
  hosts = rxe2_conncheck.check_conn(hosts,user,kwdict)
  dbg.dprint(2,"leftover hosts to execute:",hosts)
  
  ### Start for available hosts
  if len(hosts) > 0 :
    client = ParallelSSHClient(hosts,user=user,allow_agent=False,**kwdict)
    if copy: 
      rxe2_mod_parallel.copy_cmd(client,copy,cmd,timeout)
  
    ###-------------------------------------------------------------------------
    ##### Start of interactive
    if prgargs.interactive :
      # import rxe2_mod_interactive
      sys.stdout.flush()
      sys.stderr.flush()
      sys.stdin.flush()
      for host in hosts:
        rxe2_mod_general.print_hostline(user,host,cmd,opts)
        loguru.logger.info(f"{user}@{host:25} {cmd} {opts}")
        target   = user+ '@' +host
        execcmd = ' '.join(['(','ssh','-tt',target,'"',cmd,opts,'"',cfg.data.redirect])
        res = os.system(execcmd)
        loguru.logger.info(f"  -- Exit Code: {res}")
        rxe2_mod_general.log_and_cleanup(cfg.data.cap_out) 
        rxe2_mod_general.log_and_cleanup(cfg.data.cap_err) 
    ###-------------------------------------------------------------------------
    ##### Start of parallel
    else:
      ### with use_pty=True STDOUT and STDERR are always combined
      dbg.dprint(0,"cmd    =", cmd)
      output = client.run_command(cmd+" "+opts,stop_on_errors=False,
               use_pty=True,read_timeout=timeout, return_list=True)
      ### evaluate output
      rxe2_mod_parallel.show_output(client,output,cmd,opts)
      ### End of parallel 
    ###-------------------------------------------------------------------------
    ### cleanup
    if copy:
      client.run_command("rm "+cmd, stop_on_errors=False,
               return_list=True)
    ### End of available hosts
    del client

  end = datetime.datetime.now()
  dbg.leavesub()
  print()
  dbg.dprint(0,"Took",end -start,"to execute")  
###########   D E F A U L T   I N I T   #######################################
if __name__ == "__main__":
  from mydebug.py3dbg import dbg
  from myconf.py3cfg  import init_cfg
  cfg = init_cfg(prgname,prgdir,libdir,dbg)
  exec(cfg.imports)
  exec(cfg.usage)
  main()

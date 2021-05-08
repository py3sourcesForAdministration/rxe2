#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Module containing the procedures to handle ssh runs for rxe.
    all async ssh stuff is in here
"""   
##### Avoid pydoc errors
import asyncio, asyncssh, sys, datetime
try:
  from __main__ import prgdir,prgname
  import os.path
  exec(open(os.path.join(prgdir,prgname+"_imp.py")).read())
except:
  if sys.argv[0].find('pydoc'):
    pass # we are running from pydoc3
##### Module Start
### ----- copy --------------------------------------------------------
async def copy_file(host,src,dst,**kwargs):
    async with asyncssh.connect(host,**kwargs) as conn:
        return await asyncssh.scp(src,(conn,dst))

### -------------------------------------------------------------------
async def run_mcopy(hosts,src,dst,**kwargs):
    from __main__ import dbg
    from rxe2_mod_general import prnout
    dbg.entersub()
    dbg.dprint(2,'src:',src,', dst:',dst,', kwargs:',kwargs)
    availhosts = []
    tasks = (copy_file(host,src,dst,**kwargs) for host in hosts)
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for i, result in enumerate(results, 0):
        if isinstance(result, Exception):
            rxe2_mod_general.prnout('h',kwargs['username'],hosts[i],'Conncheck') 
            prnout('e',"Exception in conntest:", str(result))
        else:
            availhosts.append(hosts[i])
    dbg.leavesub()        
    return availhosts

### ----- run cmd -----------------------------------------------------
async def run_cmd(host,cmd,**kwargs):
    async with asyncssh.connect(host,**kwargs) as conn:
        return await conn.run(cmd,term_type='xterm-256color',check=True)

### -------------------------------------------------------------------
async def run_mcmds(hosts,cmd,tmout,**kwargs):
    from __main__ import dbg
    from rxe2_mod_general import prnout
    dbg.entersub()
    dbg.dprint(2,'cmd:',cmd,', tmout:',tmout,', kwargs:',kwargs)
    #tasks = (run_cmd(host,cmd,**kwargs) for host in hosts)
    tasks = (asyncio.wait_for(run_cmd(host,cmd,**kwargs),timeout=tmout) for host in hosts)
    results = await asyncio.gather(*tasks, return_exceptions=True)
    if cmd.startswith('rm /tmp/') :
        for i, result in enumerate(results, 0):
            if isinstance(result, Exception):
                prnout('w',"Exception in rm cmd:", hosts[i],"remove failed")
    else:          
        for i, result in enumerate(results, 0):
            prnout('h',kwargs['username'],hosts[i],cmd) 
            if isinstance(result, asyncio.TimeoutError):
               prnout('e',"Timeout Exception:",str(result))
               continue
            if isinstance(result, Exception):
                prnout('e',"Execution Exception:", str(result))
                continue
            ### always do  
            if result.exit_status:
                prnout('i','exit_code:',result.exit_status)
            if result.stdout:
                prnout('i',"{}".format(result.stdout.rstrip(),end=''))
            if result.stderr:
                prnout('i',"stderr: {}".format(result.stderr.rstrip(),end=''))
    dbg.leavesub()        


      

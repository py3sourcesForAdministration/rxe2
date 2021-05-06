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
async def create_conn(host,user,**kwargs):
  return await  asyncssh.connect(host,username='root',*kwargs)

async def check_conns(hosts,user,**kwargs):
  newhosts = [] 
  newconns = {} 
  conns = (create_conn(host,user,**kwargs) for host in hosts)
  for i in range(1):
    print(type(conns[i]))  
  connchecks = await asyncio.gather(*conns, return_exceptions=True)
  for i, result in enumerate(conns, 0):
    if isinstance(result, Exception):
      print('Conn to %s failed: %s' % (hosts[i], str(result)))
    else:  
      print(f"{hosts[i]} ok")   
      newhosts.append(hosts[i])
      #newconns[hosts[i]] = conns[i]
  #return  newhosts, newconns  

async def run_client(host, command):
  from __main__ import cfg,dbg
  async with asyncssh.connect(host,username='root',login_timeout=1.4) as conn:
    return await conn.run(command,term_type='xterm-256color')


async def run_multiple_clients(hosts,**kwargs):
    from __main__ import cfg,dbg
    dbg.entersub()
    newargs = {}
    if 'cmd' in kwargs:
      command = kwargs['cmd'] 
    if 'username' in kwargs:
      newargs['username'] = kwargs['username']
    if 'copy' in kwargs:
      newargs['copy'] = kwargs['copy']

    if command == 'Check#Only':
      tasks = (run_client(host, 'pwd') for host in hosts)
      results = await asyncio.gather(*tasks, return_exceptions=True)
      for i, result in enumerate(results, 0):
        if isinstance(result, Exception):
          rxe2_mod_general.print_hostline(newargs['username'],hosts[i],command,'')  
          dbg.dprint(256,f"Exception: {str(result)}")
        elif result.exit_status != 0:
          dbg.dprint(0,f"{hosts[i]} exit_code: {result.exit_status}")
          dbg.dprint(0,f"stdout: {result.stdout}",end='')
          dbg.dprint(0,f"stderr: {result.stderr}",end='')
        else:  
          cfg.data.availhosts.append(hosts[i]) 
    else:
      tasks = (run_client(host, command) for host in hosts)    
      results = await asyncio.gather(*tasks, return_exceptions=True)
      for i, result in enumerate(results, 0):
        if isinstance(result, Exception):
          print('Task %s failed: %s' % (hosts[i], str(result)))
        elif result.exit_status != 0:
          print('Task %s exited with status %s:' % (hosts[i], result.exit_status))
          print(result.stderr, end='')
          print(result.stdout, end='')
        else:
          print('Task %s succeeded:' % hosts[i])
          print(result.stderr, end='')
          print(result.stdout, end='')
      print(75*'-')
    dbg.leavesub()  


      

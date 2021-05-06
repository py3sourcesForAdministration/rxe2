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
async def run_client(host, command):
    async with asyncssh.connect(host,username='root') as conn:
        return await conn.run(command,term_type='xterm-256color')


async def run_multiple_clients(hosts,command):
    # Put your lists of hosts here

    tasks = (run_client(host, cmd) for host in hosts)
    #print(type(tasks))
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results, 0):
        #print(str(result))
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

      

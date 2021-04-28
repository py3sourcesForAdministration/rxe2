#!/usr/bin/env python3 
# -*- coding: utf8 -*-
# test for parallel-ssh v2 timeout handling
import sys,os
from   pssh.clients import ParallelSSHClient, SSHClient
from   pssh.exceptions import Timeout
#------------------------------------------------------
hosts   = [ 'centosap' ]
cmd     = 'yum update'
ruser   = 'root'
timeout = 15
kwdict  = { 'pkey'     : os.path.join(os.environ['HOME'],'.ssh','id_rsa') }
#------------------------------------------------------

client = ParallelSSHClient(hosts,user=ruser,allow_agent=False,**kwdict)
output = client.run_command(cmd,stop_on_errors=False,use_pty=True,read_timeout=timeout)
print("type(output):",type(output))

read = []
for host_out in output:
  print("------------------------- ",host_out.host, host_out.exit_code, host_out.exception )
  #print("type.host_out:", type(host_out)) 
  #print("type.host_out.buffers:", type(host_out.stdout)) 
  try:
    #host_out.channel.flush()
    for line in host_out.stdout:
      read.append(line)
  except Timeout:
    print("Got Timeout")
    host_out.client.close_channel(host_out.channel)

#for host_out in output:  
#  host_out.client.close_channel(host_out.channel)

client.join(output)  
for l in read :
  print(l)

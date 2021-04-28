#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" --- This is only the usage file ---"""
import argparse,sys,os
if sys.argv[0].find('pydoc') > 0 :
  print(__doc__); sys.exit(0)
from __main__ import prgname,dbg,cfg
show_hidden_args = '--help-long' in sys.argv
class myFormatter(argparse.RawTextHelpFormatter,argparse.ArgumentDefaultsHelpFormatter): 
  pass
parser = argparse.ArgumentParser(formatter_class=myFormatter)
### set defaults, makes it possibly to suppress the printing of defaults in help
parser.set_defaults(**cfg.argdefaults)
#all_defaults = {key: parser.get_default(key) for key in cfg.argdefaults}
#print(all_defaults)
parser.add_argument('-d', type=int, metavar="level", dest="debug",        
                        help="set debug level\t")

#############
# group0 = parser.add_mutually_exclusive_group(required=False)
parser.add_argument('-L', action='store_true', dest="log",
                          default=argparse.SUPPRESS,
                        help="write log file")
parser.add_argument('-T', type=int, metavar="sec", dest="tmout",                                                   help="Set Command timeout for parallel execution\n\t\t")
parser.add_argument('-I', action='store_true', dest="interactive",
                        default=argparse.SUPPRESS, 
                        help="instead of parallel executing command\n"+
                             "execute on hosts one by one, but\n" + 
                             "allow interacting with host")
#############
parser.add_argument('-s', nargs='*',  dest="srv", default=[ 'localhost'],
                        help="remote server or hostfile or comma sep. list\n\t\t")
#############
ident = parser.add_argument_group('ssh identity')
ident.add_argument('-u', type=str, dest="user",
                        help="remote user\t")
group1 = ident.add_mutually_exclusive_group(required=False)
group1.add_argument('-i', type=str, dest="identity",
                        help="rsa key to use\t")
group1.add_argument('-p', type=str, dest="password",
                        default=argparse.SUPPRESS,
                        help="pw of remote user")
#############
execution = parser.add_argument_group('execution')
group2 = execution.add_mutually_exclusive_group(required=False)
group2.add_argument('-lc', action='store_true', dest="listcmds",
                          default=argparse.SUPPRESS,
                        help="list available cmdfiles")
group2.add_argument('-lh', action='store_true', dest="listhosts",
                          default=argparse.SUPPRESS,
                        help="list available hostfiles")
group2.add_argument('-c', nargs='?', metavar="cmd", dest="cmd",
                        default=argparse.SUPPRESS,
                        help="cmd or existing cmdfile, if no command is\n" +
                             "given => execute "+ parser.get_default('cmd')+ " only")
execution.add_argument('-o', nargs='*', metavar="carg", dest="opts",
                          default=argparse.SUPPRESS,
                        help="cmd arguments")
args = parser.parse_args()
globals()['prgargs']  = args
dbg._initlvl(prgargs.debug) 
dbg.dprint(2, "prgargs" , prgargs)

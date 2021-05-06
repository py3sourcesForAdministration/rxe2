#!/usr/bin/env python3
# -*- coding: utf8 -*-
""" --- This is only the configuration file ---"""
import sys,os
if sys.argv[0].find('pydoc') > 0 :
  print(__doc__); sys.exit(0)

from datetime import date
from   colorama import init, Fore, Back, Style
from __main__ import prgdir,prgname
capture_out = prgname+'_out.log'
capture_err = prgname+'_err.log'
data = {
  'nodefiles' : os.path.realpath(os.path.join(prgdir,'nodefiles_use')),
  'cmdfiles'  : os.path.realpath(os.path.join(prgdir,'cmdfiles_use')),
  ### define colors
  'colors'    : {
    'rst'  : Style.RESET_ALL,
    'fgg'  : Style.BRIGHT + Fore.GREEN,
    'fgy'  : Style.BRIGHT + Fore.YELLOW,
    'fgr'  : Style.BRIGHT + Fore.RED,
  }, 
  'hlen'      : 13,
  'cptimeout' : 3,
  'chktimeout': 1.5,
  'availhosts': [],
  'cap_out'   : capture_out,
  'cap_err'   : capture_err,
  'redirect'  : " ".join(['|','tee',capture_out,')','3>&1','1>&2','2>&3','|','tee',capture_err]) 
}
argdefaults = { 
  'debug'       : 0,
  'listcmds'    : False,
  'listhosts'   : False,
  'log'         : False,
  'interactive' : False,
  'tmout'       : 3,
  'user'        : 'root',
  'srv'         : 'localhost',
  'cmd'         : 'ConnCheck',
  'identity'    : os.path.join(os.environ['HOME'],'.ssh','id_rsa'),
  'password'    : None,
  'opts'        : '',
} 

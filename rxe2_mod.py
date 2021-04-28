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

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.


import base64
from binascii import hexlify
import getpass
import select
import socket
import sys,os
import time
import traceback
### this part is from paramiko demo files : interactive.py
import socket
import sys
import paramiko
from paramiko.py3compat import u

# windows does not have termios...
try:
  import termios
  import tty
  has_termios = True
except ImportError:
  has_termios = False

#####---------------------------------------------------------------------
def interactive_shell(chan):
  if has_termios:
    posix_shell(chan)
  else:
    windows_shell(chan)

#####---------------------------------------------------------------------
def posix_shell(chan):
  import select
  oldtty = termios.tcgetattr(sys.stdin)
  try:
    tty.setraw(sys.stdin.fileno())
    tty.setcbreak(sys.stdin.fileno())
    chan.settimeout(0.0)
    while True:
      r, w, e = select.select([chan, sys.stdin], [], [])
      if chan in r:
        try:
          x = u(chan.recv(1024))
          if len(x) == 0:
            sys.stdout.write("\r\n*** EOF\r\n")
            break
          sys.stdout.write(x)
          sys.stdout.flush()
        except socket.timeout:
          pass
      if sys.stdin in r:
        x = sys.stdin.read(1)
        if len(x) == 0:
          break
        chan.send(x)
  finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

#####---------------------------------------------------------------------
# thanks to Mike Looijmans for this code
def windows_shell(chan):
  import threading
  sys.stdout.write(
    "Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n"
  )
  def writeall(sock):
    while True:
      data = sock.recv(256)
      if not data:
        sys.stdout.write("\r\n*** EOF ***\r\n\r\n")
        sys.stdout.flush()
        break
      sys.stdout.write(data)
      sys.stdout.flush()

  writer = threading.Thread(target=writeall, args=(chan,))
  writer.start()
  try:
    while True:
      d = sys.stdin.read(1)
      if not d:
        break
      chan.send(d)
  except EOFError:
    # user hit ^Z or F6
    pass

### This part is adapted from paramiko demos : demo.py
#####---------------------------------------------------------------------
def agent_auth(transport, username):
  """
  Attempt to authenticate to the given transport using any of the private
  keys available from an SSH agent.
  """
  agent = paramiko.Agent()
  agent_keys = agent.get_keys()
  if len(agent_keys) == 0:
    return
  for key in agent_keys:
    print("Trying ssh-agent key %s" % hexlify(key.get_fingerprint()))
    try:
      transport.auth_publickey(username, key)
      print("... success!")
      return
    except paramiko.SSHException:
      print("... nope.")

#####---------------------------------------------------------------------
def manual_auth(username, hostname):
    default_auth = "p"
    auth = input(
      "Auth by (p)assword, (r)sa key, or (d)ss key? [%s] " % default_auth
    )
    if len(auth) == 0:
      auth = default_auth

    if auth == "r":
      default_path = os.path.join(os.environ["HOME"], ".ssh", "id_rsa")
      path = input("RSA key [%s]: " % default_path)
      if len(path) == 0:
        path = default_path
      try:
        key = paramiko.RSAKey.from_private_key_file(path)
      except paramiko.PasswordRequiredException:
        password = getpass.getpass("RSA key password: ")
        key = paramiko.RSAKey.from_private_key_file(path, password)
        t.auth_publickey(username, key)
    elif auth == "d":
      default_path = os.path.join(os.environ["HOME"], ".ssh", "id_dsa")
      path = input("DSS key [%s]: " % default_path)
      if len(path) == 0:
        path = default_path
      try:
        key = paramiko.DSSKey.from_private_key_file(path)
      except paramiko.PasswordRequiredException:
        password = getpass.getpass("DSS key password: ")
        key = paramiko.DSSKey.from_private_key_file(path, password)
      t.auth_publickey(username, key)
    else:
      pw = getpass.getpass("Password for %s@%s: " % (username, hostname))
      t.auth_password(username, pw)

#####---------------------------------------------------------------------
##### This part is to interact with rxe
def connect(username,hostname,cmd,opts):
#  import paramiko,os
  port = 22
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
  except Exception as e:
    print("*** Connect failed: " + str(e))
    traceback.print_exc()
    sys.exit(1)
  try:
    t = paramiko.Transport(sock)
    try:
      t.start_client()
    except paramiko.SSHException:
      print("*** SSH negotiation failed.")
      sys.exit(1)

    try:
      keys = paramiko.util.load_host_keys(
        os.path.expanduser("~/.ssh/known_hosts")
      )
    except IOError:
      try:
        keys = paramiko.util.load_host_keys(
                os.path.expanduser("~/ssh/known_hosts"))
      except IOError:
        print("*** Unable to open host keys file")
        keys = {}

    # check server's host key -- this is important.
    key = t.get_remote_server_key()
    print("Got", key.get_name(),"Type",type(key))
    print("Hostname",hostname)
    for k in keys:
      if k == hostname:
        print("K:",k,keys[k]) 
    if hostname not in keys:
      print("*** WARNING1: Unknown host key!")
    elif key.get_name() not in keys[hostname]:
      print("*** WARNING2: Unknown host key!")
    elif keys[hostname][key.get_name()] != key:
      print("*** WARNING: Host key has changed!!!")
      sys.exit(1)
    else:
      print("*** Host key OK.")

    # get username
    if username == "":
      default_username = getpass.getuser()
      username = input("Username [%s]: " % default_username)
      if len(username) == 0:
        username = default_username

    agent_auth(t, username)
    if not t.is_authenticated():
        manual_auth(username, hostname)
    if not t.is_authenticated():
      print("*** Authentication failed. :(")
      t.close()
      sys.exit(1)

    chan = t.open_session()
    chan.get_pty()
    chan.invoke_shell()
    print("*** Here we go!\n")
    interactive_shell(chan)
    chan.close()
    t.close()

  except Exception as e:
    print("*** Caught exception: " + str(e.__class__) + ": " + str(e))
    traceback.print_exc()
    try:
      t.close()
    except:
      pass
    sys.exit(1)

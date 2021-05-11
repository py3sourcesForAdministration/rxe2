# rxe
program to execute remote commands with ssh (usually in parallel, with -I interactive one by one)

To use this program you need a small piece of python code as well (pylibap). Checkout this project first. Best way to use is to checkout both projects in the same subdirectory of your homedir. 
After setup of pylibap you should be able to use this one as well. 
Try rxe --help

Operation Modes:
With option -I a normal ssh connection is spawned for each host. This is slow, but enables you to answer questions from the host if the executed program requires input. Parallel Execution (the default without -I) does not offer this possibility. Executing interactive programs in parallel mode will result in timeouts. Of course the hosts must be enabled to login the executing user (option -u) first, either with password or a public key. 
When using prepared executables/scripts (see For Convenience) from the cmdfiles directory the executable is first copied to the host, then executed and afterwards removed. The copy/remove operations are always executed in parallel. 

Timeouts:
To handle long executing times of executables/scripts you change the execution timeout (-T). The timeout for the copy operation is fixed but can be changed in the rxe_cfg.py file. 
Sometimes, when a host is not available, or the name is not resolvable you will wait a long time until you get the timeout message and the reason for this timeout. DNS errors and Host down problems are handled by the os and take a long time to return. You can do something like "rxe -s <hostfile>" first to check the connection only.
      
For convenience:
There are two example directories provided. 
nodefiles.example contains text files containing hostnames one on each line. These hostfiles are checked and used with option -s first. This helps running commands on lists of hosts.
cmdfiles.example contains subdirs with executable files. This helps when running a complete list of comands on each host. Filenames in these directories can be used as parameter for option -c. You need not specify a path, just the executable's name. 

To use these directories create directories nodefiles_yourname, and cmdfiles_yourname and symbolic links nodefiles_use and cmdfiles_use to these directories.
Check with rxe -lc and rxe -lh whter the files are found.

Terms of use/License:

    rxe.py - program to execute remote commands with ssh

    Copyright © 2020 Armin Poschmann

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


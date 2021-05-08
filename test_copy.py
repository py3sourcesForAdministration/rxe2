import asyncssh,asyncio
########## ----- copy
async def copy_file(host,src,dst,**kwargs):
    async with asyncssh.connect(host) as conn:
        return await asyncssh.scp(src,(conn,dst))

async def run_mcopy(hosts,src,dst,**kwargs):
    availhosts = []
    tasks = (copy_file(host,src,dst,**kwargs) for host in hosts)
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for i, result in enumerate(results, 0):
        if isinstance(result, Exception):
            print(f"------ {hosts[i]} connection failed")  
            print(f"Exception: {str(result)}")
        else:
            availhosts.append(hosts[i])
    return availhosts

########## ----- run
async def run_cmd(host,cmd,**kwargs):
#    async with asyncssh.connect("localhost") as conn:
#        async with conn.create_process(cmd, term_type="xterm-color") as process:
#            while process.exit_status is None:
#                try:
#                    result = await asyncio.wait_for(process.stdout.readline(), timeout=timeout-0.1)
#                    print(result, end="")
#                except asyncio.TimeoutError as exc:
#                    print("Got timeout - retrying")
#            print("Remote process finished with exit status {}".format(process.exit_status))
    async with asyncssh.connect(host) as conn:
        return await conn.run(cmd,term_type='xterm-256color')

async def run_mcmds(hosts,cmd,**kwargs):
    tasks = (asyncio.wait_for(run_cmd(host,cmd,**kwargs),timeout=timeout) for host in hosts)
    results = await asyncio.gather(*tasks, return_exceptions=True)
    if cmd.startswith('rm /tmp') :
        for i, result in enumerate(results, 0):
            if isinstance(result, Exception):
                print(f"remove cmd on {hosts[i]} failed")
    else:          
        for i, result in enumerate(results, 0):
            print(f"------ {hosts[i]} {cmd}")  
            if isinstance(result, asyncio.TimeoutError):
                print("Timeout on",hosts[i],result)
                continue
            if isinstance(result, Exception):
                print(f"Exception: {str(result)}")
                continue
            if result.exit_status:
                print(f"{hosts[i]} exit_code: {result.exit_status}")
            if result.stdout:
                print(f"stdout: {result.stdout}",end='')
            if result.stderr:
                print(f"stderr: {result.stderr}",end='')

#### Start
hosts = ['localhost']
#hosts = ['localhost','foo']
script = '/home/ap/pydev/rxe/cmdfiles.example/system_info/ConnCheck'
copy   = '/tmp/ConnCheck'
#script = '/home/ap/pydev/rxe/cmdfiles_rss/rxe_test/prog_with_input.py'
#copy   = '/tmp/prog_with_input.py'
kwargs = { 'username' : 'root' }
interactive = False
timeout = 2

### Check connection and sort out unavailable hosts
#availhosts = asyncio.get_event_loop().run_until_complete(run_mcopy(hosts,script,copy,**kwargs))
#if len(hosts) != len(availhosts):
#    print(f"only {len(availhosts)} hosts left: {availhosts}")
### run the command, copied script or from commandline  
#if interactive:
#for host in availhosts:
#        pass # do something else
#else:
asyncio.get_event_loop().run_until_complete(run_mcmds(hosts,copy,**kwargs))
### cleanup if needed
#if copy:
#    asyncio.get_event_loop().run_until_complete(run_mcmds(availhosts, f"rm {copy}",**kwargs))

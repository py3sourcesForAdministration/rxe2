import asyncio, asyncssh, sys
cmd = """
echo fast line
echo -n 'slow line'; sleep 1
echo; echo "fast line"
echo -n 'slow line'; sleep 1
echo; echo "fast line"
"""
async def run_client(host,cmd):
    async with asyncssh.connect(host) as conn:
        return await (async with conn.create_process(cmd, term_type="xterm-color") as process:
        #async with conn.create_process(cmd, term_type="xterm-color") as process:
            output = []
            count = 0
            while process.exit_status is None and count < timeout:
                try:
                    result = await asyncio.wait_for(process.stdout.readline(), timeout=1)
                    print(result, end="")
                    output.append(result)
                except asyncio.TimeoutError as exc:
                    count += 1
                    #print("Got timeout - retrying")
            print("Remote process finished with exit status {},{}".format(process.exit_status,output))
        )
async def run_cmd(host,cmd,**kwargs):
    async with asyncssh.connect(host) as conn:
        return await conn.run(cmd,term_type='xterm-256color')  

async def run_mcmds(hosts,cmd,**kwargs):
    tasks = (asyncio.wait_for(run_client(host,cmd,**kwargs),timeout=timeout) for host in hosts)
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for i, result in enumerate(results, 0):
            print(f"------ {hosts[i]} {cmd}")  
            if isinstance(result, asyncio.TimeoutError):
                print("Timeout on",hosts[i],result)
                continue
            if isinstance(result, Exception):
                print(f"Exception: {str(result)}")
                continue
            #print(output)  
#            if result.exit_status:
#                print(f"{hosts[i]} exit_code: {result.exit_status}")
#            if result.stdout:
#                print(f"stdout: {result.stdout}",end='')
#            if result.stderr:
#                print(f"stderr: {result.stderr}",end='')
timeout = 5  
hosts   = ['localhost','centosap' ]
cmd     = '/tmp/ConnCheck'
asyncio.get_event_loop().run_until_complete(run_mcmds(hosts,cmd))

#asyncio.get_event_loop().run_until_complete(run_client())


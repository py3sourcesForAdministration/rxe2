import asyncio
import asyncssh
import uuid

async def run_client(host):
    async with asyncssh.connect(host) as conn:
        script = '/home/ap/pydev/rxe/cmdfiles.example/system_info/ConnCheck'
        copy   = '/tmp/ConnCheck'
        await asyncssh.scp(script,(conn,copy))

        try:
            return await conn.run(copy)
        finally:
            await conn.run(copy)

async def run_multiple_clients():
    # Put your lists of hosts here
    hosts = ['localhost', 'localhost']

    tasks = (run_client(host) for host in hosts)

    for result in await asyncio.gather(*tasks, return_exceptions=True):
        print(result)

asyncio.get_event_loop().run_until_complete(run_multiple_clients())

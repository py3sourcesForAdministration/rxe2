import asyncio, asyncssh, sys
# @asyncio.coroutine
async def run_client():
    with (asyncssh.connect('localhost')) as conn:
        stdin, stdout, stderr = await conn.open_session('echo hello1; sleep 5 ; echo hello2')

        output = await stdout.read()
        print(output, end='')

        await stdout.channel.wait_closed()

        status = stdout.channel.get_exit_status()
        if status:
            print('Program exited with status %d' % status, file=sys.stderr)
        else:
            print('Program exited successfully')

asyncio.get_event_loop().run_until_complete(run_client())


# If you are able to use python3.5, then you can use the async and await keywords. 
# So your function definition becomes async def run_client() and your yield from turns into await. – Opal Feb 12 '16 at 12:52

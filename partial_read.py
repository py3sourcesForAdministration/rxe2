import io
import asyncio

class Foo():

    async def run(self):
        proc = await asyncio.create_subprocess_exec('ping', 'www.google.de', stdout=asyncio.subprocess.PIPE)
        await asyncio.gather(self.run_proc(proc), self.kill_proc(proc))

    async def run_proc(self, proc):
        while True:
            line = await proc.stdout.readline()

            if line == b'':
                break

            print(line)

    async def kill_proc(self, proc):
        await asyncio.sleep(5)
        print("meh")
        proc.kill()


f = Foo()
loop = asyncio.get_event_loop()
loop.run_until_complete(f.run())

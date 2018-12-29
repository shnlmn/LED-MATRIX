import asyncio



loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather())
print("RUNNING")
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

loop.close()


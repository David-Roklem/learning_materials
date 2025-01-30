import asyncio


async def coro(sleep_time):
    print(f"Sleeping for {sleep_time} seconds")
    await asyncio.sleep(sleep_time)
    print(f"Done sleeping for {sleep_time} seconds")


async def main():
    c1 = coro(1)
    c2 = coro(2)
    c3 = coro(3)

    # c1_future, c2_future, c3_future = await asyncio.gather(c1, c2, c3)

    # await c1
    # await c2
    # await c3

    async with asyncio.TaskGroup() as tg:
        c1_task = tg.create_task(c1)
        c2_task = tg.create_task(c2)
        c3_task = tg.create_task(c3)

    return c1_task, c2_task, c3_task


asyncio.run(main())
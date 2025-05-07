"""Демонстрация работы отладочного режима библиотеки asyncio"""


import asyncio
from util import async_timed


@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for _ in range(10000000):
        counter = counter + 1
    return counter


async def main() -> None:
    """По умолчанию, предупреждающее сообщение выводится в консоль если корутина работает дольше 100 мс (0.1 сек).
    Это можно регулировать с помощью закомменченной части"""
    # loop = asyncio.get_event_loop()
    # loop.slow_callback_duration = 0.3
    task_one = asyncio.create_task(cpu_bound_work())
    await task_one


if __name__ == "__main__":
    asyncio.run(main(), debug=True)

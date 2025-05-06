import asyncio
import requests
import httpx
from util.async_timer import async_timed


"""
Пример ниже показывает, что если использовать блокирующую библиотеку для работы с вводом-выводом (requests),
то запросы к серверу будут выполняться последовательно, не давая никакого прироста скорости.
В закомменченной части пример асинхронного вызова посредством библиотеки httpx - время работы кода сокращается!

Если вы все-таки хотите использовать библиотеку requests, то синтаксис async применить можно,
но нужно явно попросить asyncio задействовать многопоточность с помощью исполнителя пула потоков.
"""


@async_timed()
async def get_example_status() -> int:
    # async with httpx.AsyncClient() as client:
    #     return await client.get('http://www.example.com')
    return requests.get('http://www.example.com').status_code


@async_timed()
async def main():
    task_1 = asyncio.create_task(get_example_status())
    task_2 = asyncio.create_task(get_example_status())
    task_3 = asyncio.create_task(get_example_status())
    await task_1
    await task_2
    await task_3


asyncio.run(main())

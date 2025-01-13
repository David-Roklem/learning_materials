"""В связи с тем, что в JN есть сложности с вызовом asyncio.run, все примеры кода приведены в обычном питоновском
файле"""

import asyncio
import logging
from time import sleep

# Блок логирования
logging.basicConfig(
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s",
)

log = logging.getLogger(__name__)
# Блок логирования


# Блок синхронного варианта выполнения
def get_stocks():
    log.info("get stocks")
    sleep(1)
    log.info("stocks ok")


def get_weather():
    log.info("get weather")
    sleep(1)
    log.info("weather ok")


def main():
    get_stocks()
    get_weather()


# main()
"""Вывод main() - время выполнения 2 секунды:
[2025-01-13 13:09:31.349] t:18 INFO - get stocks
[2025-01-13 13:09:32.349] t:20 INFO - stocks ok
[2025-01-13 13:09:32.350] t:24 INFO - get weather
[2025-01-13 13:09:33.350] t:26 INFO - weather ok
"""
# Блок синхронного варианта выполнения


### Блок асинхронного варианта выполнения ###

async def get_stocks():
    log.info("get stocks")
    await asyncio.sleep(1)
    log.info("stocks ok")


async def get_weather():
    log.info("get weather")
    await asyncio.sleep(1)
    log.info("weather ok")


async def main():
    coro = get_stocks() 
    log.info("created coro %s", coro)
    await coro
    await get_weather()


# asyncio.run(main())
"""Вывод asyncio.run(main()) - время выполнения по прежнему 2 секунды:
[2025-01-13 13:11:05.262] t:59 INFO - created coro <coroutine object get_stocks at 0x7f846cf12200>
[2025-01-13 13:11:05.262] t:46 INFO - get stocks
[2025-01-13 13:11:06.264] t:48 INFO - stocks ok
[2025-01-13 13:11:06.264] t:52 INFO - get weather
[2025-01-13 13:11:07.265] t:54 INFO - weather ok

Почему так? Дело в том, что использование asyncio.run(main()) само по себе не влияет на асинхронность
выполнения функций. Важно, как организованы вызовы внутри корутины main(). А вызываются ф-ии get_stocks и get_weather
последовательно, а потому и выполняться будут последовательно,
и общее время выполнения будет равно сумме времени выполнения каждой функции.
"""

"""Существуют несколько способов выполнить данный код по-настоящему асинхронно"""

# ПЕРВЫЙ способ асинхронного выполнения, применяя метод `gather`
async def get_stocks():
    log.info("get stocks")
    await asyncio.sleep(1)
    log.info("stocks ok")


async def get_weather():
    log.info("get weather")
    await asyncio.sleep(1)
    log.info("weather ok")


async def main():
    coro = get_stocks() 
    log.info("created coro %s", coro)
    task1, task2 = await asyncio.gather(coro, get_weather())
    return task1, task2


# asyncio.run(main())
"""[2025-01-13 13:19:49.954] t:96 INFO - created coro <coroutine object get_stocks at 0x7f85ffd16200>
[2025-01-13 13:19:49.954] t:82 INFO - get stocks
[2025-01-13 13:19:49.954] t:88 INFO - get weather
[2025-01-13 13:19:50.955] t:84 INFO - stocks ok
[2025-01-13 13:19:50.956] t:90 INFO - weather ok
Получаем разницу 50.956 - 49.954 ~ 1 секунда"""


# ВТОРОЙ способ асинхронного выполнения, применяя метод `create_task` с асинхронным менеджером контекста
# и asyncio.TaskGroup() - согласно официальной документации считается предпочтительным способом
async def get_stocks():
    log.info("get stocks")
    await asyncio.sleep(1.001)
    log.info("stocks ok")


async def get_weather():
    log.info("get weather")
    await asyncio.sleep(1)
    log.info("weather ok")


async def main():
    coro = get_stocks() 
    log.info("created coro %s", coro)
    # task1, task2 = await asyncio.create_task(coro), await asyncio.create_task(get_weather())
    async with asyncio.TaskGroup() as tg:
        tg.create_task(coro)
        tg.create_task(get_weather())


asyncio.run(main())
"""
[2025-01-13 13:32:37.370] t:127 INFO - created coro <coroutine object get_stocks at 0x7f7c27532380>
[2025-01-13 13:32:37.370] t:114 INFO - get stocks
[2025-01-13 13:32:37.370] t:120 INFO - get weather
[2025-01-13 13:32:38.372] t:116 INFO - stocks ok
[2025-01-13 13:32:38.372] t:122 INFO - weather ok
Получаем разницу 38.372 - 37.370 ~ 1 секунда"""

### Блок асинхронного варианта выполнения ###
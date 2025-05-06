import asyncio
from asyncio import CancelledError
from time import perf_counter
from util.delay_functions import delay

start = perf_counter()


async def main():
    long_task = asyncio.create_task(delay(10))
    seconds_elapsed = 0
    print(f"Время прошедшее с момента запуска программы - {perf_counter() - start}")
    while not long_task.done():
        print("Задача не закончилась, следующая проверка через секунду.")
        await asyncio.sleep(1)
        seconds_elapsed = seconds_elapsed + 1
        print(f"seconds_elapsed - {seconds_elapsed}")
        if seconds_elapsed == 5:
            print(f"seconds_elapsed - {seconds_elapsed} -> Принт после проверки if seconds_elapsed == 5")
            long_task.cancel()
    try:
        await long_task
    except CancelledError:
        print("Наша задача была снята")
    print(f"Время прошедшее с момента запуска программы - {perf_counter() - start}")


# asyncio.run(main())

"""
В коде выше настроена отмена задачи по истечению 5 секунд работы код. Сделано это вручную. Ниже пример установки
тайм-аута для задачи с помощью wait_for
"""


async def main2():
    delay_task = asyncio.create_task(delay(2))
    try:
        result = await asyncio.wait_for(delay_task, timeout=1)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print('Тайм-аут!')
        print(f'Задача была снята? {delay_task.cancelled()}')


# asyncio.run(main2())

"""
Эта программа завершается примерно через 1 с. По истечении 1 с предложение wait_for возбуждает исключение TimeoutError,
которое мы обрабатываем/
"""


"""
Автоматическое снятие задачи, работающей дольше, чем ожидается, обычно является разумной практикой.
В противном случае сопрограмма могла бы ждать неопределенно долго, занимая ресурсы,
которые никогда не будут освобождены. Но в некоторых случаях желательно дать сопрограмме поработать.
Например, по прошествии некоторого времени мы можем проинформировать пользователя
о том, что работа занимает дольше, чем ожидалось, но не снимать ее, когда тайм-аут истечет.

Для этого обернем нашу задачу функцией asyncio.shield. Эта функция предотвращает снятие сопрограммы,
снабжая ее «щитом», позволяющим игнорировать запросы на снятие.
"""


async def main3():
    task = asyncio.create_task(delay(10))
    try:
        result = await asyncio.wait_for(asyncio.shield(task), 5)
        print(result)
    except TimeoutError:
        print("Задача заняла более 5 с, скоро она закончится!")
        result = await task
        print(result)


asyncio.run(main3())

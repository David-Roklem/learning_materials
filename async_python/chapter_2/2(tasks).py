import asyncio
from util.delay_functions import delay


# Создание задачи
async def main():
    sleep_for_three = asyncio.create_task(delay(3))
    print(type(sleep_for_three))
    result = await sleep_for_three
    print(result)


# asyncio.run(main())


# Конкурентное выполнение нескольких задач
async def main2():
    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(3))
    sleep_once_more = asyncio.create_task(delay(3))
    await sleep_for_three
    await sleep_again
    await sleep_once_more


asyncio.run(main2())

"""
РЕЗЮМЕ
Вводим понятие задачи, которая является оберткой вокруг сопрограммы. В данном случае, мы последовательно
запускаем три задачи (sleep_for_three, sleep_again, sleep_once_more), каждая из которых запускает сопрограмму 
`delay`. Посколько задача задержка в 3 сек, то общее время выполнение корутины main2 равно 3 сек + незначительное
время, необходимое event loop`у для переключения контекста между задачами.
"""
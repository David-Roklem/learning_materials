import requests
from time import perf_counter
from functools import wraps
import threading

base_url = "https://reqres.in/"


def calc_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        time_start = perf_counter()
        res = func(*args, **kwargs)
        time_spent = perf_counter() - time_start
        print(wrapper)
        return time_spent, res
    return wrapper


def make_req(method, url, data=None):
    url = f"{base_url}{url}"
    if method == "GET":
        res = requests.get(url)
    elif method == "POST":
        res = requests.post(url)
    return res.json()


@calc_time
def main():
    threads = []

    urls = ["/api/users?delay=2", "/api/users?delay=3", "/api/users?delay=5"]
    for url in urls:
        thread = threading.Thread(target=make_req, args=("GET", url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return threads


print(main())


"""Данный пример показывает, использование многопоточности позволяет отправлять запросы не дожидаясь получения ответа
от сервера. Т.е. первым потоком отправляем первый запрос и пока происходит ожидание, сразу же вторым потоком
отправляем второй запрос. Тоже самое и с третьим. Таким образом, мы программа не простаивает попусту и общее время
работы скрипта примерно равно времени ожидания ответа с самой большой задержкой.
ВАЖНО! Несмотря на то, что мы использовали многопоточность, в действительности одновременно использовался только
1 поток (из-за GIL). Весь выигрыш во времени стал возможен только благодаря тому, что у нас происходил системный вызов,
т.е. ответственность за оповещение интерпретатора о получении ответа ложится на плечи ОС. Многопоточность
бесполезна для распараллеливания процессов интерпретатора, все из-за того же GIL. Т.е. мы не получим никакого
выигрыша при, например, попытке распараллелить 3 независимых цикла for, т.е. в один момент времени GIL не позволит
выполняться более, чем одному циклу (потоку). Иными словами, применять многопоточность в Python имеет смысл только
для input-output задач.
Также стоит отметить, что на сегодняшний день использование многопотчности является плохой практикой из-за
ненулевой вероятности сбоев из-за race conditions. К тому же, переключение контекста между потоками довольно
ресурсоемкая операция. Актуальный тренд - применение асинхронности"""

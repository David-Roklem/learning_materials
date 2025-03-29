import requests
from time import perf_counter
from functools import wraps

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


@calc_time
def make_req(method, url, data=None):
    url = f"{base_url}{url}"
    if method == "GET":
        res = requests.get(url)
    elif method == "POST":
        res = requests.post(url)
    return res.json()


def main():
    urls = ["/api/users?delay=2", "/api/users?delay=3", "/api/users?delay=5"]
    overall_time_spent = 0
    for url in urls:
        res = make_req("GET", url)
        overall_time_spent += res[0]
    print(overall_time_spent)


print(main())


"""Общее затраченное на выполнение скрипта время будет примерно соответствовать совокупному delay, 
заданному в заголовке запроса, поскольку код выполняется последовательно: сначала выполняется первый запрос - 
ожидание... потом второй запрос - ожидание... и, наконец, третий запрос - ожидание...
В файле 'http_requests_multithreading.py' реализована логика отправки запросов в многопоточном режиме.
Смотри вывод и объяснение там"""
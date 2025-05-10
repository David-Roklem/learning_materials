"""
Демонстрация работы сокета с блокировкой и без, в основе которых лежит обычный бесконечный цикл.
В случае с неблокирующейся реализацией сокета, происходит бесконечный опрос на наличие подключений до тех пор,
пока не произойдет подключение. В течение этого времени процесс загружен практически на 100%, что катастрофически
неэффективно и недопустимо в реальном проекте.
"""

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
server_socket.listen()
server_socket.setblocking(False)

connections = []

try:
    while True:
        try:
            connection, client_address = server_socket.accept()
            connection.setblocking(False)
            print(f'Получен запрос на подключение от {client_address}!')
            connections.append(connection)
        except BlockingIOError:
            pass
        print(f"Current number of connections is {len(connections)}")

        for conn in connections:
            buffer = b''
            while buffer[-2:] != b'\r\n':
                data = conn.recv(2)
                if not data:
                    break
                else:
                    print(f'Получены данные: {data}!')
                    buffer = buffer + data
            print(f"Все данные: {buffer}")
            conn.sendall(buffer)

finally:
    server_socket.close()

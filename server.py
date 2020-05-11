import os
import socket
from time import sleep
from threading import Thread
from datetime import datetime

try:
    from signal import pause
except ImportError:
    def pause():
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            pass


def accept_tcp_connections(serversocket):
    while True:
        clientsocket, clientaddress = serversocket.accept()
        Thread(target=handle_request, args=(clientsocket, clientaddress), daemon=True).start()


def handle_request(clientsocket, clientaddress):
    request = b''
    while True:
        request += clientsocket.recv(1024)
        if request.endswith(b'\r\n' * 2):
            break
    print(request.decode())

    headers = [
        b'HTTP/1.1 200 OK',
        b'Content-Type: text/plain',
        b'X-Secret-Message: Hello world!',
    ]
    body = f'Hello world! Current time is {datetime.now()}.'.encode()

    response = b'\r\n'.join(headers) + b'\r\n' * 2 + body
    clientsocket.sendall(response)
    clientsocket.close()


if __name__ == '__main__':
    # ip, port = '0.0.0.0', 80
    # ip, port = '127.0.0.1', 80
    # ip, port = '127.0.0.1', 5000
    ip = '0.0.0.0'
    port = os.environ['PORT']

    print('Python HTTP Server\nPress Ctrl+C to exit')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as serversocket:
        try:
            serversocket.bind((ip, port))
        except OSError:
            raise SystemExit('Address already in use')
        serversocket.listen(5)

        Thread(target=accept_tcp_connections, args=(serversocket,), daemon=True).start()
        print(f'Listening on {ip}:{port}')

        pause()
        print('Goodbye!')

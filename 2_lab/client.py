from socket import socket
from threading import Thread
import http_parser
import json

host = 'localhost'
port = 6666
queue_len = 21
codding = 'utf-8'


def read_from_socket(s: socket):
    data = b''
    while True:
        chunk = s.recv(1024)
        if chunk:
            data += chunk
        if len(chunk) == 0 or chunk[-1:] == b'\n':
            break
    return data


def client(i: int):
    client_connection = socket()
    client_connection.connect((host, port))

    message = json.dumps({'position': i})
    request = http_parser.GET(message)
    client_connection.send(request.encode(codding))
    data = read_from_socket(client_connection).decode(codding)
    request = http_parser.POST_parser(data)
    message = request['message']

    print(f"Receive for {i}: {message['number']}")
    client_connection.close()


def main():
    numbers = []
    for i in range(3):
        numbers.append(int(input("Enter the fib num: ")))

    threads = []
    for i in range(3):
        thread = Thread(target=client, args=(numbers[i],))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()

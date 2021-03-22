from socket import socket, AF_INET, SOCK_STREAM
from select import select
import http_parser
import json

host = 'localhost'
port = 6666
queue_len = 21
codding = 'utf-8'


def fibonacci(n) -> int:
    f_n = f_n_next = 1

    n = int(n) - 2

    while n > 0:
        f_n, f_n_next = f_n_next, f_n + f_n_next
        n -= 1

    return f_n_next


def read_from_socket(s: socket):
    data = b''
    while True:
        chunk = s.recv(1024)
        if chunk:
            data += chunk
        if len(chunk) == 0 or chunk[-1:] == b'\n':
            break
    return data


def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(queue_len)

    print("Server started")

    readable = [server_socket]
    writeable = []
    exceptional = [server_socket]

    messages = {}

    while True:
        read, write, _except = select(readable, writeable, exceptional)

        for s in read:
            if s is server_socket:
                new_client, addr = server_socket.accept()
                readable.append(new_client)
            else:
                data = read_from_socket(s)
                data = http_parser.GET_parser(data.decode(codding))

                for k, v in data.items():
                    print(f"{k}: {v}")
                print("\n")

                message = data['message']
                fib_num = fibonacci(message['position'])
                message = json.dumps({'number': fib_num})
                answer = http_parser.POST(message)
                messages[s] = answer
                writeable.append(s)
                readable.remove(s)

        for s in write:
            data = messages[s]
            s.send(data.encode(codding))
            writeable.remove(s)
            s.close()

        for s in _except:
            if s is server_socket:
                break
            s.close()


if __name__ == '__main__':
    main()

import json
import threading
from socket import socket, AF_INET, SOCK_STREAM, SO_RCVBUF, SOL_SOCKET

HOST = 'localhost'
PORT = 65432
QUEUE_LEN = 10
CODING = "utf-8"


def read_from_socket(s: socket) -> bytearray:
    data = bytearray()
    buff_size = s.getsockopt(SOL_SOCKET, SO_RCVBUF)
    while True:
        chunk = s.recv(buff_size)
        if chunk:
            data += chunk
        if len(chunk) == 0 or chunk[-1:] == b'/n':
            break
        return data


def fibonacci(n) -> int:
    fib1 = fib2 = 1

    n = int(n) - 2

    while n > 0:
        fib1, fib2 = fib2, fib1 + fib2
        n -= 1

    return fib2


def connection_handler(client_socket, client_info):
    raw_request = read_from_socket(client_socket)
    request = raw_request.decode(CODING)
    request_dict = json.loads(request)

    print(f"Receive from {client_info}, payload: {request}")

    result_number = str(fibonacci(request_dict["number"]))
    result_dict = {
        "result": result_number,
    }

    response_json = json.dumps(result_dict)
    response_raw = response_json.encode(CODING)

    client_socket.send(response_raw)

    client_socket.close()


def main() -> None:
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(QUEUE_LEN)
    while True:
        (client_socket, client_info) = sock.accept()

        connection_thread = threading.Thread(target=connection_handler, args=(client_socket, client_info))
        connection_thread.start()


if __name__ == '__main__':
    main()

import json
import threading
from socket import socket, AF_INET, SOCK_STREAM, SO_RCVBUF, SOL_SOCKET

HOST = 'localhost'
PORT = 65432
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


def connection_request(host, port, position, connection_number):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))

    request_dict = {
        "number": position,
    }
    request_json = json.dumps(request_dict)

    request_raw = request_json.encode(CODING)
    sock.send(request_raw)

    response_raw = read_from_socket(sock)
    response = response_raw.decode(CODING)

    result_dict = json.loads(response)

    sock.close()
    print(
        f"Receive for {position}: {result_dict['result']}. Connection number: {connection_number}")


def main() -> None:
    requests = []
    for _ in range(0, 3):
        requests.append(int(input("Enter the number of element: ")))

    thread_pool = []
    for i in range(0, len(requests)):
        thread_pool.append(threading.Thread(target=connection_request, args=(HOST, PORT, requests[i], i)))
        thread_pool[i].start()


if __name__ == '__main__':
    main()

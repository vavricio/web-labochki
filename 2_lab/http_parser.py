import json


def GET(message: str) -> str:
    get = 'GET / HTTP/1.1\nServer: Apache\nContent-Language: uk\nContent-Type: text/html\n'
    get += 'Content-Length: ' + str(len(str(message))) + '\n\n'
    get += str(message) + '\n'

    return get


def POST(message: str) -> str:
    post = 'HTTP/1.1 200 OK\nServer: Apache\nContent-Language: uk\nContent-Type: text/html\n'
    post += 'Content-Length: ' + str(len(str(message))) + '\n\n'
    post += str(message) + '\n'

    return post


def GET_parser(http: str):
    http = http.split('\n')
    get = {}
    first_line = http.pop(0).split()
    request_type = first_line[0]
    protocol, version = first_line[2].split('/')
    get['request_type'] = request_type
    get['protocol'] = protocol
    get['version'] = version

    index = 0
    for i in http:
        index += 1
        if i == '':
            break
        else:
            line = i.split(': ')
            get[line[0]] = line[1]
    get['message'] = json.loads(http[index])
    return get


def POST_parser(http: str) -> dict:
    http = http.split('\n')
    post = {}
    first_line = http.pop(0).split()
    request_type = 'POST'
    protocol, version = first_line[0].split('/')
    status = first_line[1]
    description = first_line[2]
    post['request_type'] = request_type
    post['protocol'] = protocol
    post['version'] = version
    post['status'] = status
    post['description'] = description

    index = 0
    for i in http:
        index += 1
        if i == '':
            break
        else:
            line = i.split(': ')
            post[line[0]] = line[1]
    post['message'] = json.loads(http[index])

    return post

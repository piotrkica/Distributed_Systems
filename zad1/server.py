from threading import Thread
import socket
import time


def init_server():
    server_address = ('127.0.0.1', 9000)

    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_tcp.bind(server_address)
    socket_udp.bind(server_address)

    return socket_tcp, socket_udp


def handle_client_tcp(ip, port, client_conn):
    print('Connection from', (ip, port))
    while True:
        data = client_conn.recv(128)
        data = str(data, 'cp1250')
        if data == 'exit' or not data:
            break
        else:
            print(f'[{port}] {time.strftime("%H:%M:%S")}: {data}')
            for sock in sockets:
                if sock != client_conn:
                    sender_info = str(port)
                    sock.send(bytes(sender_info + " " + data, 'cp1250'))

    sockets.remove(client_conn)
    client_conn.close()


def handle_client_udp():
    while True:
        data, (ip, port) = socket_udp.recvfrom(1024)
        data = str(data, 'cp1250')
        if not data:
            break
        else:
            print(f'[{port}] {time.strftime("%H:%M:%S")}: {data}')
            for sock in sockets:
                if sock.getpeername() != (ip, port):
                    socket_udp.sendto(bytes(str(port) + " " + data, 'cp1250'), sock.getpeername())


if __name__ == "__main__":
    print('PYTHON SERVER START')
    socket_tcp, socket_udp = init_server()
    socket_tcp.listen()
    threads = []
    sockets = []

    client_udp = Thread(target=handle_client_udp)
    client_udp.start()
    threads.append(client_udp)

    while True:
        socket_tcp.listen()
        connection, (ip, port) = socket_tcp.accept()
        sockets.append(connection)

        client_tcp = Thread(target=handle_client_tcp, args=(ip, port, connection))
        client_tcp.start()
        threads.append(client_tcp)

        for t in threads:
            if not t.is_alive():
                t.join()
                threads.remove(t)

    client_udp.join()

    print('PYTHON SERVER SHUTDOWN')

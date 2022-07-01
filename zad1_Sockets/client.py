from threading import Thread
import socket
import struct
import time

serverIP = "127.0.0.1"
serverPort = 9000
MCAST_GRP = '225.1.1.1'
MCAST_PORT = 5007


def init_client():
    client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client_tcp.connect((serverIP, serverPort))
    port = client_tcp.getsockname()[1]
    client_udp.bind(("127.0.0.1", port))

    client_mcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client_mcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)
    client_mcast.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    client_mcast.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    return client_tcp, client_udp, client_mcast


def handle_tcp(sock):
    while True:
        try:
            data = sock.recv(128)
            data = str(data, 'cp1250')
            if data:
                data = data.split(' ', 1)
                sender_info, msg = data[0], data[1]
                print(f'[{sender_info}] {time.strftime("%H:%M:%S")}: {msg}')
        except (ConnectionResetError, ConnectionAbortedError) as ex:
            break


def handle_udp(sock):
    while True:
        try:
            data, address = sock.recvfrom(1024)
            data = str(data, 'cp1250')
            if data:
                data = data.split(' ', 1)
                sender_info, msg = data[0], data[1]
                print(f'[{sender_info}] {time.strftime("%H:%M:%S")}: {msg}')
        except Exception:
            break


def handle_mcast(sock):
    while True:
        try:
            data = sock.recv(128)
            data = str(data, 'cp1250')
            if data:
                data = data.split(' ', 1)
                sender_info, msg = data[0], data[1]
                if sender_info != ID:
                    print(f'[{sender_info}] {time.strftime("%H:%M:%S")}: {msg}')
        except Exception as ex:
            break


if __name__ == "__main__":
    print('PYTHON CLIENT START')
    client_tcp, client_udp, client_mcast = init_client()
    ID = str(client_tcp.getsockname()[1])

    tcp_thread = Thread(target=handle_tcp, args=[client_tcp])
    udp_thread = Thread(target=handle_udp, args=[client_udp])
    mcast_thread = Thread(target=handle_mcast, args=[client_mcast])
    tcp_thread.start()
    udp_thread.start()
    mcast_thread.start()

    while True:
        msg = input()
        if msg == "U":
            msg = input()
            client_udp.sendto(bytes(msg, 'cp1250'), (serverIP, serverPort))
        elif msg == "M":
            msg = input()
            client_mcast.sendto(bytes(ID + " " + msg, 'cp1250'), (MCAST_GRP, MCAST_PORT))
        else:
            client_tcp.send(bytes(msg, 'cp1250'))
        if msg == "exit":
            client_tcp.close()
            client_udp.close()
            client_mcast.close()
            break

    tcp_thread.join()
    udp_thread.join()
    mcast_thread.join()
    print('PYTHON CLIENT SHUTDOWN')

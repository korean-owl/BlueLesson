import socket
import threading
from queue import Queue

def Send(group, send_queue):
    print('Thread Send Start')
    while True:
        try:
            # 새롭게 추가된 클라이언트가 있을 경우 Send 스레드를 새롭게 만들기 위해 루프를 빠져나감
            recv = send_queue.get()
            if recv == 'Group Changed':
                print('Group Changed')
                break

            # for 문을 돌면서 모든 클라이언트에게 동일한 메시지를 보냄
            for conn in group:
                msg = 'Client' + str(recv[2]) + ' >> ' + str(recv[0])
                if recv[1] != conn:  # client 본인이 보낸 메시지는 받을 필요가 없기 때문에 제외시킴
                    conn.send(bytes(msg.encode()))
                else:
                    pass
        except:
            pass


def Recv(conn, count, send_queue):
    print('Thread Recv' + str(count) + ' Start')
    while True:
        data = conn.recv(1024).decode()
        send_queue.put([data, conn, count])  # 각각의 클라이언트의 메시지, 소켓정보, 쓰레드 번호를 send로 보냄


# TCP Echo Server
if __name__ == '__main__':
    send_queue = Queue()
    HOST = '0.0.0.0'  # 수신 받을 모든 IP를 의미
    PORT = 9000  # 수신받을 Port
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP Socket
    server_sock.bind((HOST, PORT))  # 소켓에 수신받을 IP주소와 PORT를 설정
    server_sock.listen(10)  # 소켓 연결, 여기서 파라미터는 접속수를 의미
    count = 0
    group = []  # 연결된 클라이언트의 소켓정보를 리스트로 묶기 위함
    while True:
        count = count + 1
        conn, addr = server_sock.accept()  # 해당 소켓을 열고 대기
        group.append(conn)  # 연결된 클라이언트의 소켓정보
        print('Connected ' + str(addr))

        # 소켓에 연결된 모
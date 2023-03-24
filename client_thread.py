import socket
import threading

def receive_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"[서버] {data.decode()}")

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 8080))

    receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
    receive_thread.start()

    while True:
        msg = input("메시지를 입력하세요: ")
        client_socket.sendall(msg.encode())

if __name__ == "__main__":
    main()

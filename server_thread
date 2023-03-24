import socket
import threading

def handle_client(client_socket, addr):
    print(f"[+] 연결된 클라이언트: {addr}")
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"[{addr}] {data.decode()}")
        client_socket.sendall(data)
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))
    server.listen(5)

    print("[*] 서버 시작됨...")

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    main()

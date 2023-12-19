import socket

def send_create_account_request(host, port, username, password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (host, port)
    client_socket.connect(server_address)

    try:
        request = f"CREATE_ACC {username} {password}"
        client_socket.sendall(request.encode())

        response = client_socket.recv(1024)
        print(f"Server Response: {response.decode()}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    server_host = "localhost"
    server_port = 12345
    new_username = "mina123"
    new_password = "AnaMina123"

    send_create_account_request(server_host, server_port, new_username, new_password)

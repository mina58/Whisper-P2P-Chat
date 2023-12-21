from server.Network.ServerMainThread import ServerMainThread
import socket

ip = socket.gethostbyname(socket.gethostname())
port = 12121

server_thread = ServerMainThread(
    ip=ip,
    port=port
)
server_thread.start()

print(f"Server started on {ip}:{port}")
input("Press Enter to stop the server...\n")

# Stop the server
server_thread.stop()
server_thread.join()

import tkinter as tk
from tkinter import simpledialog
from client.Presentation.WelcomeScreen import WelcomeScreen

def main():
    server_ip = simpledialog.askstring(
        "Welcome to whisper", "Please enter the ip address of the server.")
    if server_ip is None:
        return
    root = tk.Tk()
    app = WelcomeScreen(root, server_ip)
    root.mainloop()


if __name__ == "__main__":
    main()

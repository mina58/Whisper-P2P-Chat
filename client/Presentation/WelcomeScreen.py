import tkinter as tk
from tkinter import simpledialog

from client.Presentation.MainMenu import MainMenu
from client.Service.ServiceOrchestrator import ServiceOrchestrator


class WelcomeScreen:
    def __init__(self, root, server_ip):
        self.root = root
        self.root.title("Whisper Chat")

        self.services = ServiceOrchestrator(server_ip)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Create and position the buttons
        self.create_buttons()

    def create_buttons(self):
        sign_up_button = tk.Button(
            self.root, text="Sign Up", command=self.sign_up)
        login_button = tk.Button(self.root, text="Login", command=self.login)
        sign_up_button.grid(row=0, column=0, padx=100, pady=10)
        login_button.grid(row=1, column=0, padx=100, pady=10)

    def sign_up(self):
        username = simpledialog.askstring("Sign Up", "Enter a new username:")
        password = simpledialog.askstring(
            "Sign Up", "Enter a new password:", show="*")
        if self.services.create_account(username, password):
            tk.messagebox.showinfo("Sign Up", "Sign up successful!")
        else:
            tk.messagebox.showerror("Sign Up", "Sign up failed!")

    def login(self):
        username = simpledialog.askstring("Login", "Enter your username:")
        password = simpledialog.askstring(
            "Login", "Enter your password:", show="*")
        if self.services.login(username, password):
            tk.messagebox.showinfo("Login", "Login successful!")
            MainMenu(self.root, self.services)
        else:
            tk.messagebox.showerror("Login", "Login failed!")

    def on_close(self):
        self.services.close()
        self.root.destroy()

import tkinter as tk
from tkinter import simpledialog

from client.Presentation.ChattingScreen import ChattingScreen

class MainMenu:
    def __init__(self, root, services):
        self.root = root
        self.services = services
        self.root.title("Main Menu")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_buttons()

    def create_buttons(self):
        create_room_button = tk.Button(self.root, text="Create Room",  command=self.create_room)
        join_room_button = tk.Button(self.root, text="Join Room", command=self.join_room)
        list_rooms_button = tk.Button(self.root, text="List Rooms", command=self.list_rooms)
        list_users_button = tk.Button(self.root, text="List Users", command=self.list_users)
        private_chat_button = tk.Button(self.root, text="Private Chat", command=self.private_chat)
        logout_button = tk.Button(self.root, text="Logout", command=self.logout)

        buttons = [create_room_button, join_room_button, list_rooms_button, list_users_button, private_chat_button, logout_button]

        for i, button in enumerate(buttons):
            button.grid(row=i, column=0, padx=100, pady=10)

    def create_room(self):
        room_name = simpledialog.askstring("Room Name",  "Enter a room name:")
        if self.services.create_room(room_name):
            tk.messagebox.showinfo("Room Created", "Room created successfully!")
            self.clear_root()
            ChattingScreen(self.root, self.services)
        else:
            tk.messagebox.showerror("Room unavailable", "Room creation failed!")

    def join_room(self):
        room_name = simpledialog.askstring("Room Name", "Enter a room name:")
        if self.services.join_room(room_name):
            tk.messagebox.showinfo("Room Joined", "Room joined successfully!")
            self.clear_root()
            ChattingScreen(self.root, self.services)
        else:
            tk.messagebox.showerror("Room unavailable", "Room join failed!")

    def list_rooms(self):
        rooms = self.services.list_rooms()
        tk.messagebox.showinfo("Rooms", "\n".join(rooms))

    def list_users(self):
        users = self.services.list_users()
        tk.messagebox.showinfo("Users", "\n".join(users))

    def private_chat(self):
        pass

    def logout(self):
        self.services.close()
        self.root.destroy()

    def on_close(self):
        self.services.close()
        self.root.destroy()

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()
import tkinter as tk


class PrivateChattingScreen:
    def __init__(self, root, services):
        self.root = root
        self.root.title("Chat App")

        # Initialize the service
        self.services = services
        self.is_chatting = True

        # Message display area with scrollbar
        self.message_frame = tk.Frame(root)
        self.message_area = tk.Text(
            self.message_frame, height=15, width=50, state=tk.DISABLED)
        self.scrollbar = tk.Scrollbar(
            self.message_frame, command=self.message_area.yview)
        self.message_area.config(yscrollcommand=self.scrollbar.set)
        self.message_area.grid(row=0, column=0, sticky=tk.NSEW)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.message_frame.grid(padx=10, pady=10)

        # Entry to type messages
        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=5, sticky=tk.EW)

        # Send button
        self.send_button = tk.Button(
            root, text="Send", command=self.send_message)
        self.send_button.grid(row=2, column=0, pady=5)

        # Back button
        self.back_button = tk.Button(root, text="Back", command=self.go_back)
        self.back_button.grid(row=3, column=0, pady=5)

        # Bind the Enter key to send message
        self.message_entry.bind("<Return>", self.send_message_event)

        # Start receiving messages
        self.get_messages()
        self.check_connection()
        self.get_requests()

        # Set the window close sequence for graceful shutdown
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def send_message(self, event=None):
        message = self.message_entry.get()
        self.add_messages([f"{self.services.username}: {message}"])
        if message:
            self.services.send_private_chat_message(message)

    def add_messages(self, messages):
        for message in messages:
            self.message_area.config(state=tk.NORMAL)
            self.message_area.insert(tk.END, f"{message}\n")
            self.message_area.config(state=tk.DISABLED)
            self.message_entry.delete(0, tk.END)

            # Scroll to the end
            self.message_area.see(tk.END)

    def go_back(self):
        from client.Presentation.MainMenu import MainMenu
        self.is_chatting = False
        self.services.end_private_chat()
        self.clear_root()
        MainMenu(self.root, self.services)

    def send_message_event(self, event):
        # Triggered when Enter key is pressed in the entry
        self.send_message()

    def get_messages(self):
        messages = self.services.get_private_chat_messages()
        messages = [
            f"{message['username']}: {message['message']}" for message in messages]
        if len(messages) > 0:
            self.add_messages(messages)

        if self.is_chatting:
            # Schedule the next get_message call in 100ms
            self.root.after(100, self.get_messages)

    def on_close(self):
        self.is_chatting = False
        self.services.close()
        self.root.destroy()

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def check_connection(self):
        status = self.services.get_is_connected_to_private_chat()
        if status:
            self.root.after(100, self.check_connection)
        else:
            tk.messagebox.showinfo("Chat ended", "User left the chat.")
            self.go_back()

    def get_requests(self):
        if self.services.is_chat_requested():
            sender = self.services.get_requested_chat_username()
            response = tk.messagebox.askyesno(
                "Chat Request", f"Do you want to chat with {sender}?")
            if response:
                self.services.end_private_chat()
                self.services.accept_private_chat()
                tk.messagebox.showinfo("Accepted", "Accepted request")
                self.clear_root()
                PrivateChattingScreen(self.root, self.services)
            else:
                self.services.reject_private_chat()
                self.root.after(100, self.get_requests)
        else:
            self.root.after(100, self.get_requests)

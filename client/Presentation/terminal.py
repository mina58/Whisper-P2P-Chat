
import curses
# import asyncio
import threading
import time

from client.Service.ServerAPI import ServerAPI
from client.Service.ChatService import ChatService
from queue import Queue

chat_messages = []
current_room = ""
my_username = ""
to_chat_queue = Queue()
api = None
chat_service = None
udp_port = None


'''
# update the chat screen with messages called from get_messages function , didnt use it 
def show_messages(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 8, f"Room: {current_room}", curses.color_pair(2) | curses.A_BOLD)

    for i, message in enumerate(chat_messages, start=2):
        stdscr.addstr(i, 0, message, curses.color_pair(2))

    stdscr.refresh()

# get messages asynchronously
async def get_messages():
    global chat_messages
    while True:
        if chat_service != None:
            messages = chat_service.get_messages()        # function from ChatService to get msgs from the server
        if messages:
            chat_messages.extend(messages)
            
            # curses.wrapper(show_messages)  # ignore this , no need
        await asyncio.sleep(1)

# user yb3t msg gdeda
def send_message(message):
    chat_service.send_message(message)   # function from ChatService

    
'''

# Welcome screen


def welcome_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 8, "WELCOME TO P2P CHAT APP",
                  curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(2, 0, "1. Sign up", curses.color_pair(3))
    stdscr.addstr(3, 0, "2. Log in", curses.color_pair(3))
    stdscr.addstr(5, 0, "Select an option (1/2): ")
    stdscr.refresh()
    choice = stdscr.getch()
    if choice == ord('1'):
        return "signup"
    elif choice == ord('2'):
        return "login"
    else:
        return "welcome"

# Signup screen


def signup_screen(stdscr):
    stdscr.clear()

    stdscr.addstr(0, 8, "Sign-Up", curses.color_pair(2) | curses.A_BOLD)

    stdscr.addstr(2, 0, "Enter your username: ",
                  curses.color_pair(4) | curses.A_BOLD)
    curses.echo()
    username = stdscr.getstr(3, 0, 30).decode('utf-8')

    stdscr.addstr(5, 0, "Enter your password: ",
                  curses.color_pair(4) | curses.A_BOLD)
    curses.noecho()
    password = stdscr.getstr(6, 0, 30).decode('utf-8')

    stdscr.addstr(7, 0, "Confirm your password: ",
                  curses.color_pair(4) | curses.A_BOLD)
    confirm_password = stdscr.getstr(8, 0, 30).decode('utf-8')

    if password == confirm_password:
        if api.create_account(username, password):
            my_username = username

            stdscr.addstr(
                9, 0, "Account created successfully. Press any button to return.")
            return "welcome"

        else:
            stdscr.addstr(
                9, 0, "Username is taken. Press any button to return.")
        stdscr.getch()
        return "welcome"
    else:
        stdscr.addstr(
            9, 0, "Passwords do not match. Press any key to go back.")
        stdscr.getch()
        return "welcome"

# Login screen


def login_screen(stdscr):
    global my_username

    stdscr.clear()
    stdscr.addstr(0, 8, "Log-In", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(2, 0, "Enter your username: ",
                  curses.color_pair(4) | curses.A_BOLD)
    curses.echo()
    username = stdscr.getstr(3, 0, 30).decode('utf-8')

    stdscr.addstr(5, 0, "Enter your password: ",
                  curses.color_pair(4) | curses.A_BOLD)
    curses.noecho()
    password = stdscr.getstr(6, 0, 30).decode('utf-8')

    if api.login(username, password):
        my_username = username

        return "home"
    stdscr.addstr(
        9, 0, "Login failed. Press any key to go back.")
    stdscr.getch()
    return "welcome"

# Home screen


def home_screen(stdscr):
    stdscr.clear()
    stdscr.clear()

    stdscr.addstr(0, 8, "HOME", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(0, 8, "HOME", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(2, 0, "1. Create Room", curses.color_pair(5))
    stdscr.addstr(3, 0, "2. List Available Rooms", curses.color_pair(5))
    stdscr.addstr(4, 0, "3. Join Room", curses.color_pair(5))
    stdscr.addstr(5, 0, "4. List Users", curses.color_pair(5))
    stdscr.addstr(6, 0, "5. Private Chat", curses.color_pair(5))
    stdscr.addstr(7, 0, "6. Logout", curses.color_pair(5))
    stdscr.addstr(9, 0, "Select an option (1-6): ")
    stdscr.refresh()

    choice = stdscr.getch()
    if choice == ord('1'):
        return "create_room"
    elif choice == ord('2'):
        return "list_rooms"
    elif choice == ord('3'):
        return "join_room"
    elif choice == ord('4'):
        return "list_users"
    elif choice == ord('5'):
        return "private_chat"
    elif choice == ord('6'):
        api.logout()
        return None
    else:
        return "home"

# List rooms screen


def list_rooms_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 8, "List Rooms", curses.color_pair(4) | curses.A_BOLD)

    available_rooms = api.list_rooms()  # ["room_1", "room_2", ...]

    for i, room in enumerate(available_rooms, start=1):
        stdscr.addstr(i, 0, f"{i}. {room}")

    stdscr.refresh()

    choice = stdscr.getch()
    return "home"

# List users screen


def list_users_screen(stdscr):
    stdscr.scrollok(True)
    stdscr.clear()
    stdscr.addstr(0, 8, "List Users", curses.color_pair(4) | curses.A_BOLD)

    online_users = api.list_users()

    for i, user in enumerate(online_users, start=2):
        stdscr.addstr(i, 0, f"{i-1}. {user}", curses.color_pair(2))

    stdscr.addstr(len(online_users) + 5, 0, "Press 0 to go back to home.")
    stdscr.refresh()

    choice = stdscr.getch()
    if choice == ord('0'):
        return "home"
    else:
        return "list_users"

# Create room screen


def create_room_screen(stdscr):
    global chat_service, current_room, to_chat_queue, my_username

    stdscr.clear()
    stdscr.addstr(0, 8, "Create New Room",
                  curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(2, 0, "Enter the room name: ",
                  curses.color_pair(4) | curses.A_BOLD)
    curses.echo()
    room_name = stdscr.getstr(3, 0, 30).decode('utf-8')
    curses.noecho()

    chat_service = ChatService(room_name, my_username, to_chat_queue)

    if api.create_room(room_name):
        current_room = room_name
        stdscr.addstr(
            5, 0, f"Room '{room_name}' created successfully. Press any key to start chatting")
        stdscr.getch()
        return "room_chatting"
    else:
        chat_service.end_chat()
        stdscr.addstr(5, 0, f"Invalid room name. Press any key to go back.")
        stdscr.getch()
        return "create_room"

# Join room screen


def join_room_screen(stdscr):
    global chat_service, current_room, to_chat_queue, my_username, udp_port

    stdscr.clear()
    stdscr.addstr(0, 8, "Join Room", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(2, 0, "Enter the room name: ",
                  curses.color_pair(4) | curses.A_BOLD)
    curses.echo()
    room_name = stdscr.getstr(3, 0, 30).decode('utf-8')
    curses.noecho()

    chat_service = ChatService(room_name, my_username, to_chat_queue)
    udp_port = chat_service.get_address()[1]

    if api.join_room(room_name, udp_port):  # fe salfa hena    udp_port
        current_room = room_name
        stdscr.addstr(5, 0, f"Joining room '{room_name}'...")
        stdscr.addstr(6, 0, "Press any key to start chatting")
        stdscr.getch()
        return "room_chatting"
    else:
        stdscr.addstr(
            5, 0, f"Room '{room_name}' is not available. Press any key to go back.")
        stdscr.getch()
        chat_service.end_chat()
        return "join_room"


def room_chatting_screen(stdscr):
    global chat_service, chat_messages

    is_chatting = True
    stdscr.scrollok(True)
    message = ""

    def get_messages_thread():
        current_line = 0
        while is_chatting:
            chat_messages = chat_service.get_messages()
            for i, msg in enumerate(chat_messages, start=2):
                stdscr.addstr(current_line + i, 0,
                              msg, curses.color_pair(2))
                stdscr.refresh()

            stdscr.move(stdscr.getmaxyx()[0] - 1, len(message) + 1)
            current_line += len(chat_messages)
            stdscr.refresh()

            time.sleep(0.1)

    get_messages_thread = threading.Thread(target=get_messages_thread)

    get_messages_thread.start()

    stdscr.addstr(0, 8, f"Room: {current_room}",
                  curses.color_pair(2) | curses.A_BOLD)

    stdscr.clear()
    curses.curs_set(1)  # Show the cursor
    curses.echo()  # Enable echoing

    input_win_height = 10
    input_win = curses.newwin(
        1, curses.COLS, curses.LINES - input_win_height, 0)

    input_win.refresh()

    rows, cols = stdscr.getmaxyx()
    stdscr.move(rows - 1, 0)

    while True:
        stdscr.refresh()

        char = stdscr.getch()

        if char == curses.KEY_BACKSPACE or char == 127:
            message = message[:-1]
            input_win.clear()
            input_win.addstr(0, 0, message)
            input_win.refresh()
        elif char == curses.KEY_ENTER or char == 10 or char == 13:
            chat_service.send_message(message)
            message = ""
            stdscr.move(rows - 2, 0)
            stdscr.clrtoeol()
            input_win.clear()
            input_win = curses.newwin(1, curses.COLS - 1, curses.LINES - 1, 0)
            input_win.refresh()
        elif char == 27:
            is_chatting = False
            chat_service.end_chat()
            api.leave_room(current_room)
            return "home"
        else:
            message += chr(char)

        rows, cols = stdscr.getmaxyx()
        stdscr.move(rows - 1, len(message))


def main(stdscr):

    # api = ServerAPI(server_ip, server_port,to_chat_queue)

    # chat_service = ChatService(current_room, my_username, to_chat_queue)
    # udp_port = chat_service.get_address()

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.bkgd(curses.color_pair(1))

    current_screen = "welcome"
    is_running = True

    while is_running:
        if current_screen == "welcome":
            current_screen = welcome_screen(stdscr)
        elif current_screen == "signup":
            current_screen = signup_screen(stdscr)
        elif current_screen == "login":
            current_screen = login_screen(stdscr)
        elif current_screen == "home":
            current_screen = home_screen(stdscr)
        elif current_screen == "list_rooms":
            current_screen = list_rooms_screen(stdscr)
        elif current_screen == "list_users":
            current_screen = list_users_screen(stdscr)
        elif current_screen == "create_room":
            current_screen = create_room_screen(stdscr)
        elif current_screen == "join_room":
            current_screen = join_room_screen(stdscr)
       # elif current_screen == "private_chat":
        #    current_screen = private_chat_screen(stdscr)
        elif current_screen == "room_chatting":
            current_screen = room_chatting_screen(stdscr)
        else:
            curses.endwin()
            is_running = False


# if _name_ == "main":
server_ip = input("Enter server ip: ")
server_port = 12121
api = ServerAPI(server_ip, server_port, to_chat_queue)
curses.wrapper(main)

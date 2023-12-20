import curses


def welcome_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 8, "WELCOME TO P2P CHAT APP",  curses.color_pair(2) | curses.A_BOLD )
    stdscr.addstr(2, 0, "1. Sign up" , curses.color_pair(3))
    stdscr.addstr(3, 0, "2. Log in" ,  curses.color_pair(3))
    stdscr.addstr(5, 0, "Select an option (1/2): ")
    stdscr.refresh()
    choice = stdscr.getch()
    if choice == ord('1'):
        return "signup"
    elif choice == ord('2'):
        return "login"
    else:
        return "welcome"

# def get_user_input(stdscr, prompt, is_password=False):
#     stdscr.addstr(0, 0, prompt, curses.color_pair(4) | curses.A_BOLD)
#     curses.echo()
#     if is_password:
#         curses.noecho()
#         user_input = stdscr.getstr(1, 0, 30).decode('utf-8')
#         curses.echo()
#     else:
#         user_input = stdscr.getstr(1, 0, 30).decode('utf-8')
#     curses.noecho()
#     return user_input
    

def signup_screen(stdscr):
    stdscr.clear()
    
    stdscr.addstr(0, 8, "Sing-Up",  curses.color_pair(2) | curses.A_BOLD )

    stdscr.addstr(2, 0, "Enter your username: ", curses.color_pair(4) | curses.A_BOLD)
    curses.echo()
    username = stdscr.getstr(3, 0, 30).decode('utf-8')

    stdscr.addstr(5, 0, "Enter your password: ", curses.color_pair(4) | curses.A_BOLD)
    curses.noecho()
    password = stdscr.getstr(6, 0, 30).decode('utf-8')
    
    
    stdscr.addstr(7, 0, "Confirm your password: ", curses.color_pair(4) | curses.A_BOLD)
    confirm_password = stdscr.getstr(8, 0, 30).decode('utf-8')
    
    if password == confirm_password:
        return "home"
    else:
        stdscr.addstr(4, 0, "Passwords do not match. Press any key to go back.")
        stdscr.getch()
        return "welcome"

def login_screen(stdscr):

    stdscr.clear()
    
    stdscr.addstr(0, 8, "Log-In",  curses.color_pair(2) | curses.A_BOLD )

    stdscr.addstr(2, 0, "Enter your username: ", curses.color_pair(4) | curses.A_BOLD)
    curses.echo()
    username = stdscr.getstr(3, 0, 30).decode('utf-8')

    stdscr.addstr(5, 0, "Enter your password: ", curses.color_pair(4) | curses.A_BOLD)
    curses.noecho()
    password = stdscr.getstr(6, 0, 30).decode('utf-8')
    

    return "home"

def home_screen(stdscr):
    
    stdscr.clear()
    stdscr.clear()
    
    stdscr.addstr(0, 8, "HOME",  curses.color_pair(2) | curses.A_BOLD )
    stdscr.addstr(2, 0, "1. Create Room" , curses.color_pair(5))
    stdscr.addstr(3, 0, "2. List Available Rooms" , curses.color_pair(5))
    stdscr.addstr(4, 0, "3. Join Room" , curses.color_pair(5))
    stdscr.addstr(5, 0, "4. List Users" , curses.color_pair(5))
    stdscr.addstr(6, 0, "5. Private Chat" , curses.color_pair(5))
    stdscr.addstr(7, 0, "6. Logout" , curses.color_pair(5))
    stdscr.addstr(9, 0, "Select an option (1-6): " )
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
        return "welcome"
    
    else:
        return "home"


def list_rooms_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 8, "List Rooms", curses.color_pair(4) | curses.A_BOLD)

    
    available_rooms = ["Gaming Room", "Music Room", "Studying Room", "Wael Ghonim Space"]

    for i, room_name in enumerate(available_rooms, start=2):
        stdscr.addstr(i, 0, f"{i-1}. Room Name: {room_name}", curses.color_pair(2))

    stdscr.addstr(len(available_rooms) + 5, 0, "Press 0 to go back to home.")
    stdscr.refresh()

    choice = stdscr.getch()
    if choice == ord('0'):
        return "home"
    else:
        return "list_rooms"



def list_users_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 8, "List Users", curses.color_pair(4) | curses.A_BOLD)

    
    online_users = ["Mohamed", "Moemen", "Mina", "Donia", "Wael Ghonim"]

    for i, user in enumerate(online_users, start=2):
        stdscr.addstr(i, 0, f"{i-1}. {user}", curses.color_pair(2))

    stdscr.addstr(len(online_users) + 5, 0, "Press 0 to go back to home.")
    stdscr.refresh()

    choice = stdscr.getch()
    if choice == ord('0'):
        return "home"
    else:
        return "list_users"


def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) 
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.bkgd(curses.color_pair(1))

    current_screen = "welcome"

    while True:
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
        

if __name__ == "__main__":
    curses.wrapper(main)






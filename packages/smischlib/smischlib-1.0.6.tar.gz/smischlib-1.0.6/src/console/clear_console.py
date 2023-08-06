from smischlib import running_os
from os import system
def clear_console(type="full"):
    if type == "full":
        if running_os() == "win":
            system("cls")
        else:
            system("clear")
    elif type == "line":
        print("\033[A\033[K", end="") #presunutie o poličko spať "\033[A", zmazanie riadka "\033[K"
    
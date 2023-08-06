from smischlib import running_os
from os import system
def clear_console(type="full"):
    if type == "full":
        if running_os() == "win":
            system("cls")
        else:
            system("clear")
    elif type == "line":
        print(100*" ",end="\r\r")
    
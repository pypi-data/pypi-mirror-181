import sys
from src.utilities.running_os import running_os
from src.print.anim_print import animated_print
from src.input.anim_input import animated_input
from src.console.clear_console import clear_console
from src.input.ask_input import ask_input

def testoro():
    if running_os() == "win":
        print("EZ je to win")
    else:
        print("NEEZ je to linux")

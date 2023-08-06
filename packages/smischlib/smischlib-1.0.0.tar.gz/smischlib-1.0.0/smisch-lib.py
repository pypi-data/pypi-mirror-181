from src.utilities.running_os import *

def testoro():
    if running_os() == "win":
        print("EZ je to win")
    else:
        print("NEEZ je to linux")
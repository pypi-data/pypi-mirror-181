from smischlib import animated_input
def ask_input(text,type="str"):
    while True:
        if type == "str":
            a = animated_input(text,0.01)
            return a
        elif type == "int":
            try:
                a = int(animated_input(text,0.01))
                return a 
            except: pass
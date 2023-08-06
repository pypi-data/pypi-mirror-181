from smischlib import animated_input
def ask_input(prompt="Example prompt for input:",datatype="str",type="animated",delay=0.05):
    while True:
        if datatype == "str":
            if type == "animated":
                a = animated_input(prompt,delay)
                return a
            else:
                a = input(prompt)
                return a
        elif datatype == "int":
            try:
                if type == "animated":
                    a = int(animated_input(prompt,delay))
                    return a
                else:
                    a = int(input(prompt))
                    return a
            except: pass
import os,time,string,random
def clear_console(type="line"):
    if type == "line":
        print(100*" ",end="\r")
    elif type == "console":
        for i in range(100):
            print()
def animate_print(text,delay=0.05):
    custom_text = []
    for i in text:
        custom_text.append(i)
        time.sleep(delay)
        print("".join(custom_text),end="\r")
def animate_input(text,delay=0.05):
    clear_console("console")
    custom_text = []
    for i in text:
        custom_text.append(i)
        time.sleep(delay)
        if len(text) != len(custom_text):
            print("".join(custom_text),end="\r")
        else:
            s = input(f"{text}")
            clear_console("console")
            return s
def ask_input(text,type="str"):
    while True:
        if type == "str":
            a = animate_input(text,0.01)
            return a
        elif type == "int":
            try:
                a = int(animate_input(text,0.01))
                return a 
            except: pass

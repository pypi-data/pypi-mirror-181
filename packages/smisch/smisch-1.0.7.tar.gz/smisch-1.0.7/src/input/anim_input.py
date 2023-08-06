from smisch import clear_console
import time

def animate_input(text,delay=0.05):
    clear_console("full")
    custom_text = []
    for i in text:
        custom_text.append(i)
        time.sleep(delay)
        if len(text) != len(custom_text):
            print("".join(custom_text),end="\r")
        else:
            s = input(f"{text}")
            clear_console("full")
            return s
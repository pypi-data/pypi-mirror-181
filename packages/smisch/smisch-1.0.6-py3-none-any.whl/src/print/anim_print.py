import time

def animate_print(text,delay=0.05):
    custom_text = []
    for i in text:
        custom_text.append(i)
        time.sleep(delay)
        print("".join(custom_text),end="\r")
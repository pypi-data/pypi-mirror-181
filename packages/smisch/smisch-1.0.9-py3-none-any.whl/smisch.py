import os,time,string,random
from src.console.clear_console import *
from src.print.anim_print import *
from src.utilities.running_os import *
from src.input.anim_input import *
from src.input.ask_input import *

def test_smi():
    for i in range(100):
        print(i)
    clear_console("line")
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

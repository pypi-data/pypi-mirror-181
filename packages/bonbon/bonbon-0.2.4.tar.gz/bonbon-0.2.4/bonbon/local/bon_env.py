import os
from time import sleep
from datetime import datetime
from pydirectinput import move
from contextlib import contextmanager

def afk(): 
    cnt, t = 0, 60
    while True:
        if cnt % t == 0:
            print(f"{datetime.now()}: {cnt}")
        move(-1, None)
        sleep(1.0)
        move(1, None)
        sleep(1.0)
        cnt+=1

@contextmanager
def change_dir(destination):
    try:
        cwd = os.getcwd()
        os.chdir(destination)
        yield
    finally:
        os.chdir(cwd)

if __name__ == "__main__":
    print('### ghost ###')
    afk()

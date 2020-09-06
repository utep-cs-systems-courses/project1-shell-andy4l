#! /usr.bin/env python3
'''
Andres Ramos 88585473
The goal for this lab is to mimic
behaviors commonly found in a bash shell
'''
import os, sys, re

while True:
        print(os.getcwd())
        command = input('$ ', )
        
        if command == 'quit':
                sys.exit()
        elif command == 'fork':
                pid = os.fork()
                if pid < 0:
                        print("Fork failed. Exit.")
                elif pid > 0:
                        #print("Parent\n")
                        print("Parent ID:", os.getpid())
                        print("Child process: ", pid)
                else:
                        #print("Child Process")
                        print("Child ID:", os.getpid())
                        print("Parent process: ", os.getpid())

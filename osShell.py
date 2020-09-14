import os, sys, time, re

'''
Andres Ramos 88585473
The goal for this lab is to mimic
behaviors commonly found in a bash shell
'''

def listFile() :
    direct = os.listdir(os.getcwd())
    print(direct)        
    return   


os.fork()
print("Hello World", os.getpid())
while True:

    if 'PS1' in os.environ:
        os.write(1,(os.environ['PS1']).encode())
    else:
        os.write(1, ("$ ").encode())
    command = ""
    command = input()
    
    #Check if 'cd' is in command and split off after cd 
    # so you know which directory to move to 
    if "cd" in command:
        directory = command.split("cd")[1].strip()
    try:
        os.chdir(directory)
    except FileNotFoundError:
        os.write(1, ("No such file or directory.\n").encode())
    continue

    if command == 'ls':
        listFile()

    if command == 'quit':
        sys.exit()
    

    
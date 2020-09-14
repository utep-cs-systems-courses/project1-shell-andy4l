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

def getCWD():
    cdir = os.getcwd()
    os.write(1, (cdir + "\n").encode())
    return

def forkProcess(rc, pid):

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
        args = ["wc", "p3-exec.py"]
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
            try:
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly

        os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
        sys.exit(1)                 # terminate with error

    else:                           # parent (forked ok)
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())
                 



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
        continue

    if command == 'quit':
        sys.exit()
        
    if "cwd" in command:
        getCWD()
        continue

    pid = os.getpid()
    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
    rc = os.fork()
    forkProcess(rc, pid)
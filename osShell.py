import os, sys, time, re

'''
Andres Ramos 88585473
The goal for this lab is to mimic
behaviors commonly found in a bash shell
'''
# def that outputs the list of files and folders in our current directory
def listFile() :
    direct = os.listdir(os.getcwd())
    print(direct)        
    return   

# def that prints the path of our current working directory to standard output
def getCWD():
    cdir = os.getcwd()
    os.write(1, (cdir + "\n").encode())
    return

# takes the rc of our fork, the read and write fd (if any) 
# and a boolean expression to denote if our process is a pipe as parameters.
def forkProcess(rc, pid, r, w, isPipe, background):
    # Checking if rc's value is less than 0.
    # If so thats an indication that the fork failes, and the shell
    # returns to wait for more input
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    # Check the child process that was created
    elif rc == 0:   
                      # child
        # Checks if the command was a pipe
        if isPipe:
            os.close(0)
            os.dup2(w, sys.stdout.fileno(), True)

        # create input and output if any redirection
        input = command.split("<")
        output = command.split(">")
        #os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())


        #pass input/output to redirection def
        isRedirect(input, output)

    else:                           # parent (forked ok)
        #os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())
        if isPipe:
            os.dup2(1, w, True)
        if not background:
            childPidCode = os.wait()
        #os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())
                 

def isRedirect(input, output):
    # redirect childs output
    if len(output) > 1:
        input = output[0].split()
        args = input[0].split()
        os.close(1) # close 
        os.open(output[1].strip(), os.O_CREAT | os.O_WRONLY)
        fd = sys.stdout.fileno()
        os.set_inheritable(fd, True)

    # Assign redirect input into arguments
    if len(input) > 1:
        args = input[0].split()
        os.close(0)
        sys.stdin = open(input[1].strip(), "r")
        fd = sys.stdin.fileno()
        os.set_inheritable(fd, True)

    # if no redirection, split input and assign to args 
    # so it can try and execute the command
    else:
        args = input[0].split()
        

    # Try each directory in the environment path
    for dir in re.split(":", os.environ['PATH']):
        # Checks if command is file path.
        if "/" in args[0]:
            program = args[0]
        else:
            program = "%s/%s" % (dir, args[0])

        # Execute the program
        try:
            os.execve(program, args, os.environ)

        except FileNotFoundError:
            pass

    os.write(2, ("Error: Child could not exec %s\n" % args[0]).encode()) #write to stderr 
    sys.exit(1)                 # terminate with error




#Shell execution starts here
while True:
    # Checks if PS1 variable exists, if not
    # writes one to standard output
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

    # Checking to see if we are going to pipe a command
    if "|" in command:
        r, w = os.pipe()
        
        for command in command.split("|"):
            pid = os.getpid()
            rc = os.fork()
            isPipe = False
            forkProcess(rc, pid, r, w, isPipe)
        continue
    
    # Exit shell
    if command == 'exit':
        sys.exit()
    # Get the current working directory
    if "cwd" in command:
        getCWD()
        continue
    
    background = False

    if "&" in command:
        command = command.split("&")[0]
    background = True

    pid = os.getpid()
    #os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
    rc = os.fork()
    forkProcess(rc, pid, 0, 1, False, background)
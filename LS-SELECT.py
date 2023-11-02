#! /usr/bin/env python3
'''This is merely a proof of concept of a visual interactive selection.
Therefore this script may lack in docstrings and commentary'''

import tty, termios, sys, os
import pyls ### This is the other Script

class _Catch: #This Class is a branch of _Getch : https://code.activestate.com/recipes/134892/
    def __call__(self):
        fi = sys.stdin.fileno() #set input file-interface as 0
        attr = termios.tcgetattr(fi) #get attributes of fi
        try:
            tty.setraw(sys.stdin.fileno())  #try raw input for tty
            key_in = sys.stdin.read(1)          #key_in is a single input
        finally:
            termios.tcsetattr(fi, termios.TCSADRAIN, attr) # add fi, don't change by input
        return key_in


def get_the_dirs(path): #get all dirs in path
    ret = []#will be returned
    dir_content = os.listdir(path)
    for f in dir_content:
        if os.path.isdir(path+"/"+f):
            ret.append(f)

    ret.sort(key=lambda e : pyls.sortingname(e)) # using the sorting from my script
    return ret

def go_up(path):
    return os.path.abspath(path+"/..")
    
def go_down(path,dir):
    return os.path.abspath(path+"/"+dir)
    
def selector():

    print("Welcome to the visual dir selector\n")
    print("\tNavigate with wasd, w is up a dir, s is down, a and d switch choice")
    print("\tto ls the chosen dir, hit l. Hit q to quit\n")

    flags = input("But first, define ls options.\n")
    inkey = _Catch() #<- class on call() prepares stdin.read(1)
    #prepare:
    k = "" #<- this will be the keypress
    path = "/" #starting path
    pos = 0 #position in dir
    nav_list = get_the_dirs("/") #list to navigate
    breadcrumbs = [""] #breadcrumbs are a path to current view

    left_d = "" #dirs left are 0 at start
    right_d = (" ".join(nav_list[pos+1:]))[:60] # there can be many to the right at start

    #The selector loop
    ############################################################################################
    while k !="q":
        if len(breadcrumbs)>3:
            prefix = "..."
        else:
            prefix = "/"
        #the print consists of prefix ->, dirs to the left, pos, dirs to the right
        #to avoid overlapping with old text, 35 spaces are added
        print(prefix + "/".join(breadcrumbs[-2:]) \
                + " : ->  " + left_d +" " \
                +"["+nav_list[pos]+"]"+" "\
                + right_d + " "*35 ,end="\r")
        
        k=inkey() # the magic class is constructed fetching a single input

        if k=="a":  #left
            pos = pos-1
            pos = (max(0,pos)) # no overflow

        elif k=="d": # right
            pos = pos+1
            pos = (min(pos, len(nav_list)-1)) # no underflow

        elif k =="s": #down
            #only go down, if dirs inside that entry
            if len(get_the_dirs(go_down(path,nav_list[pos]))) > 0:
                path = go_down(path,nav_list[pos])  #new path
                breadcrumbs.append(nav_list[pos])   #added breadcrumb before overwrite
                nav_list=get_the_dirs(path)         #get content
                pos = 0                             #reset!

        elif k =="w": #up
            path = go_up(path)                      #new path
            nav_list=get_the_dirs(path)             #get content
            pos = 0                                 #reset
            if len(breadcrumbs)>0:                  #pop last entry if exist
                breadcrumbs.pop()    

        elif (k == "l") or (k =="p"):
            break                                   #escape the while

        elif k == "r":
            print("\n"*100)                         #This is a repair

        left_d = (" ".join(nav_list[:pos]))[-25:]           #refresh the print content
        adding = 25-len(left_d)                             #if left is less,
        right_d = (" ".join(nav_list[pos+1:]))[:25+adding]  #right can be longer
    ############################################################################################
    #Exited the while loop
    if k == "q": #quitted
        print() # finish the print!
        return k
    
    else:                                   #make ls call
        print()                             #finish print!
        print("\n")                         #add spacing
        lsdir = go_down(path,nav_list[pos]) #get dir to be listed
        print(lsdir[1:])                    #Display name without the leading "/"
        # call the pyls ls function, placeholder args[0] corresponding to sys.argv[0]
        pyls.main_ls(["pyls.py","-" + flags, lsdir])   
    return k


if __name__ == '__main__':
    while True:
        key = selector()
        if key != "p":          #SECRET ;)
            break
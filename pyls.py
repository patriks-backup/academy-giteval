#! /usr/bin/env python3
""""A Python Script resembling a part of the linux ls command"""
#import os
#import stat as getstat
#from pathlib import Path as plp
#from datetime import datetime as dt
#from datetime import date as dtdate
#import sys

#options as global variable to get easy access
lsopt = {
"-a" : False,	#show hidden and ./ ../
"-A" : False,	#show hidden but no ./ ../	

"-p" : False,	#append / to dirs	manip
"-Q" : False, 	#name in Quotes		manip

"-g" : False,	# no owner
"-o" : False,	# no group
"-i" : False,	# inode number
"-l" : False,	# long listing
"-s" : False,	# print block size

"-R" : False,	#list subdirs recursive


"-S" : False,	#sort by size		sorting
"-t" : False,	#sort by time		sorting
"-r" : False}	#reverse order		sorting



full_help = '''Welcome to the Path Content Grabber [PCG!] ;)

Usage: file.py [options] [paths]
options:	any of the below either one by one or [-together]
paths:		the paths to the directories (quotes for spaces!)

possible options:	
   -a			do not ignore entries starting with ., show "."&".."

   -A			do not ignore entries starting with ., don't show "."&".."

   -g     		forces -l, but do not list owner

   -o    		forces -l, but do not list group information

   -i			print the index number of each file

   -l			use a long listing format

   -p			append '/' indicator to directories

   -Q			enclose entry names in double quotes

   -r			reverse order while sorting

   -R			list subdirectories recursively

   -s			print the allocated size of each file, in blocks

   -S     		sort by file size, largest first

   -t     		sort by time, newest first; see --time

other calls:

   --help (or -h,?)	display this help and exit (needs to be first!)

   --version (or -v)	output version information and exit (needs to be first!)'''

def colored(text,ftype):
    """Returns a "colored" string to be interpreted in terminal via ANSI Escape Codes.
    They are not all implemented as this is a simple repetitive task
    and with the central objective to learn more python,
    I decided to implement only some examples like DIR, EXEC and FIFO"""

    dircolors = {
    #"dircolors --print-database" gives an even longer list for each system
    "DIR" :"01;34", # directory
    "LINK" :"01;36", # symbolic link.
    "FIFO" : "40;33", # pipe
    "SOCK" :"01;35", # socket
    "DOOR" :"01;35", # door
    "BLK" :"40;33;01", # block device driver
    "CHR" :"40;33;01", # character device driver
    "SETUID" :"37;41", # file that is setuid (u+s)
    "SETGID" :"30;43", # file that is setgid (g+s)	
    "STICKY_OW" :"30;42", # dir that is sticky and other-writable (+t,o+w)
    "DIR_OW": "34;42", # dir that is other-writable (o+w) and not sticky
    "STICKY" :"37;44", # dir with the sticky bit set (+t) and not other-writable
    "EXEC" :"01;32"} # This is for files with execute permission:

    fmt_start = '\033['+dircolors[ftype]+'m' 	# Ansi Start and color code
    fmt_end = "\033[0m"							# Ansi Reset = 0

    return fmt_start + text + fmt_end

def sort_warn():
    '''Prints a warning sring if both sortings are given'''
    print("\n\n    " + colored("Warning!","SETUID") \
        + "\nBoth sortings were given. sorting alphabetically\n")


def get_max_lens(ls_lines):
    """To produce a nice long print, this function gets the
    longest entry in each column and returns paddings to format"""

    max_lens= [] # the list of pads correspondig to the columns
    #for each column ...
    for col in range(len(ls_lines[0])):
        col_max = 0
        #... go trough each entry and get the max len
        for f_num in range(len(ls_lines)):
            if len( ls_lines[f_num][col] ) > col_max:
                col_max = len( ls_lines[f_num][col] )
        max_lens.append(col_max)

    #create padding first everyting left aligned:
    pad_str =[]
    for m in max_lens:
        pad_str.append('{:<'+str(m)+'}')

    #right aligning according to options
    if lsopt["-i"] and lsopt["-s"]:
        pad_str[0] = '{:>'+pad_str[0][3:] #inode
        pad_str[1] = '{:>'+pad_str[1][3:] #blocks
        pad_str[3] = '{:>'+pad_str[3][3:] #n_links
    elif lsopt["-i"]:
        pad_str[0] = '{:>'+pad_str[0][3:] #inode
        pad_str[2] = '{:>'+pad_str[2][3:] #n_links
    elif lsopt["-s"]:
        pad_str[0] = '{:>'+pad_str[0][3:] #blocks
        pad_str[2] = '{:>'+pad_str[2][3:] #n_links
    else:
        pad_str[1] = '{:>'+pad_str[1][3:] #n_links

    pad_str[-3] = '{:>'+pad_str[-3][3:] # -l size is always -3

    return " ".join(pad_str)


def make_print_items(full_lines):
    """This funtion takes full lines and extract print items according to
    the flags. Also formats date and add appendings like symlink-> or dir/"""

    print_lines = []
    for fl in full_lines:   #go through full line and select items
        print_item = []
        if lsopt["-i"]:
            print_item.append(fl[0])    #inode

        if lsopt["-s"]:
            print_item.append(fl[1])    #blksize

        if lsopt["-l"]:
            print_item.append(fl[2])    #permstr
            print_item.append(fl[3])    #num of links
            if not lsopt["-g"]:
                print_item.append(fl[4])#owner
            if not lsopt["-o"]:
                print_item.append(fl[5])#group
            print_item.append(fl[6])	#size

            #format mtime
            diff_days = (dt.now() - fl[7]).days
            c_t = fl[7].strftime("%b %d %H:%M")
            if diff_days > 182:
                c_t = fl[7].strftime("%b %d  %Y")
            print_item.append(c_t)
        #end -l items

        #name plus appending
        if fl[2][0] == "l" and lsopt["-l"]:
            print_item.append(fl[8]+" -> "+os.readlink(fl[10]))

        elif fl[2][0] == "d" and lsopt["-p"]:
            print_item.append(fl[8]+"/")

        else:
            print_item.append(fl[8])

        #done for single
        print_lines.append(print_item)
    #done for all
    return print_lines


def long_print(ls_array):
    '''The ls -l version: check if lines to print exist,
    then get padding, then print each line formatted'''

    if len(ls_array) == 0:
        return ""

    max_list_pad = get_max_lens(ls_array)
    for ln in ls_array:
        print(max_list_pad.format(*ln))


def shortprint(ls_list):
    '''Short print doesn't break items, so maybe in the future
    test_term wil try to fit in line and return a max row len,
    then this could be printed in columns and padded'''

    all_lines = []
    for i in ls_list:
        printitem = " ".join(i)
        all_lines.append(printitem)

    print("        ".join(all_lines))


#### HELPER SECTION ####################

def sort_content(to_sort,pdir,ppdir):
    '''This function returns a sorted list of triplets (dir entries).
    Three different sortings, mtime, size or alphabetically(default).
    To keep consistency with ls and dont mess with empty strings after lstrip("._"),
    the dirs . and .. are added after the alphabetically sort if -a is given'''

    # make the corresponding sort:
    if lsopt["-t"]:	#based on time
        if lsopt["-a"]:
            to_sort = [pdir,ppdir] + to_sort
        to_sort.sort(key=lambda e : e[7])
        to_sort.reverse() # ls sorts newest to top

    elif lsopt["-S"]: # based on size
        if lsopt["-a"]:
            to_sort = [pdir,ppdir] + to_sort
        to_sort.sort(key=lambda e : int(e[6]))
        to_sort.reverse() #ls sorts biggest to top

    else: # based on name, sortingname ignores lower/upper and leading . or _
        to_sort.sort(key=lambda e : sortingname(e[9]))
        if lsopt["-a"]:
            to_sort = [pdir,ppdir] + to_sort # add after sort

    #Check for -r as reverse Flag
    if lsopt["-r"]:
        to_sort.reverse()

    return to_sort

#Helping function to sort by name:
def sortingname(entry):
    '''A helper function to sort alphabetically,
    makes all lower and lstrips for . and _ '''

    entrysort = entry.lower()
    return entrysort.lstrip("_.")


def myparse_arg(args_in):
    '''my really specific argument parsing.
    Checks for calls without args, for -h to print help or -v for version.
    Ignores args[0] and splits by flags and dirs by checking for -.
    dirs are returned in dir_list and flags are processed into global lsopt.'''

    dir_list = [] # list of dirs
    #Simple call, Help or Version#
    if len(args_in) <2:
        #Simple call no args given
        simple_dir = "."
        dir_list.append(simple_dir)
        return dir_list

    #check for help or version:
    if args_in[1] in ["h","-h","-help","--help","?"]:
        print(full_help)
        return False

    elif args_in[1] in ["v","-v","-version","--version"]:
        print("Path Content Grabber [PCG!] ;) Version 0.1")
        return False

    #parse the args further
    if args_in[-1][0] == "-":
    # last arg is option (starts with minus)
    # ->target path is omitted (".")
    # ->all arguments are flags to parse
        simple_dir = "."
        dir_list.append(simple_dir)
        argstr=" ".join(args_in[1:])
    else:
    # last arg is not an option
    # -> target path is last arg
    # -> split arguments into flags and dirs
        args,dir_list = split_args(args_in)
        #print(args,dir_list) # debug
        argstr=" ".join(args)

    #Parse flags to lsopt#
    #for each letter: setting lsopt flags true
    global lsopt
    for sign in argstr:
        if ("-" + sign) in lsopt: # e.g. ["-a"]
            lsopt[("-" + sign) ] = True

    #check dependencies and forcings:
    if lsopt["-g"] or lsopt["-o"]:
        lsopt["-l"] = True
    if lsopt["-a"]:
        lsopt["-A"] = True

    #Warn, if both sortings are given and sort alphabetically
    if lsopt["-S"] and lsopt["-t"]: # maybe the last one?
        sort_warn()
        lsopt["-S"] = False
        lsopt["-t"] = False

    #Done
    return dir_list # <- this is a LIST of dirdicts


def split_args(args_in):	# returns pair (flags, dirs)
    '''a helper function to seperate flags (starting with -) and dirs.
    This was implemented to feature multiple directories support.'''

    flags = []
    dirs = []
    for arg in args_in[1:]:
        if arg[0] == "-":
            flags.append(arg)
        else:
            dirs.append(arg)
    return flags,dirs


def get_full_ls_lines(entries):
    '''This function collects the maximal possible lines for all entry objects.
    It calls make_full_line for each entry by passing name, path and stat.'''

    ls_lines = []
    for cur_f in entries:
        #check if hidden objects are to be processed, leading . and not -A
        if (cur_f.name[0] == ".") and not (lsopt["-A"]):
            pass

        else:
            triplet = [cur_f.name, cur_f.path, cur_f.stat(follow_symlinks=False)]
            fline = make_full_line(triplet[0], triplet[1], triplet[2])
            ls_lines.append(fline)

    return ls_lines

def make_full_line(ename, epath, estat):
    '''This is the core ls functionality, returning the data.
    A full Data-List is created and names colored (not all colors implemented)'''
    #line: ino,blk,perm,numlinks,owner,group,size,date,name
    line_ret = []

    #inode number
    c_i = str(estat.st_ino)
    line_ret.append(c_i)

    #blocksize:
    sysls = os.popen("ls -sad "+"'"+ epath +"'").read()
    c_b = sysls.split(" ")[0]
    line_ret.append(c_b)

    #permissions as string:
    c_p = getstat.filemode(estat.st_mode)
    line_ret.append(c_p)

    #number of links?
    c_nl = str(estat.st_nlink)
    line_ret.append(c_nl)

    #owner & owner group
    c_plp = plp(epath) #pathlib.path can return owner and group
    c_o = c_plp.owner()
    c_g = c_plp.group()
    line_ret.append(c_o)
    line_ret.append(c_g)

    #size: # SYMLINKS DISPLAY TARGET!
    c_s = str(estat.st_size)
    line_ret.append(c_s)

    #time via datetime.datetime as dt
    c_mt= dt.fromtimestamp(estat.st_mtime)
    line_ret.append(c_mt)

    #name and color					##############################
    c_n = ename
    # if it contains a space and no -Q, add ' around
    if (" " in c_n) and (not lsopt["-Q"]):
        c_n = "'"+c_n+"'"

    elif lsopt["-Q"]: # -Q quotes all names
        c_n = '"'+c_n+'"'

    # get coloring, this is the same for every kind, check and color
    # Because if/elif is used, hierarchy matters
    if c_p[0] == "p":
        c_n = colored(c_n,"FIFO")
    elif c_p[0] == "l":
        c_n = colored(c_n,"LINK")
    elif c_p[0] == "d":
        c_n = colored(c_n,"DIR")
    elif "x" in c_p:
        c_n = colored(c_n,"EXEC")


    line_ret.append(c_n)

    line_ret.append(ename)  # the ast two entries are stored, to support...
    line_ret.append(epath)  # later access to name or path (e.g. symlink in print)
    return line_ret


def ls_for_dir(lsdir):
    '''This function creates the ls call for each entry.
    Get absolute path, scan dir, get ls-lines, sort and then print'''

    #Get absolute path
    path_start = lsdir[0]
    if path_start in ["/", "~"]:
        lsdir = lsdir
    else:
        lsdir = os.getcwd()+"/"+lsdir

    if lsdir[-1] == "/" and (len(lsdir)>1):
        lsdir = lsdir[:-1] # cut trailing "/"

    try:
        dirscan = list(os.scandir(lsdir))
    except:
        print("This is no valid path")
        dirscan = False

    if dirscan == False:
        return 1 #exit!

    full_list = get_full_ls_lines(dirscan) # get all data

    #create "." and ".." entries and sort the list
    pdir = make_full_line(".", lsdir+"/.", os.stat(lsdir+"/.",follow_symlinks=False))
    ppdir = make_full_line("..", lsdir+"/..", os.stat(lsdir+"/..",follow_symlinks=False))
    sorted_full = sort_content(full_list,pdir,ppdir)

    prints = make_print_items(sorted_full)

    #print in longformat (-l, print total blocks) or in short:
    if lsopt["-l"]:
        total_blks = 0
        for k in sorted_full:
            total_blks += int(k[1])
        print("insgesamt", total_blks)
        long_print(prints)

    else:
        shortprint(prints)


###MAIN:
def main_ls(args_in):
    '''This is the main module call, parse args get dirs.
    Call ls for each dir (if -R is given add all subdirectories prior).'''

    dirs = myparse_arg(args_in) # sets global 'lsopt' returns list of dirs

    if dirs == False:
        return 0

    for d in dirs:
        if len(dirs)>1 or lsopt["-R"]: # multiple dirs: print name watch for spaces
            if " " in d:
                dp = "'" + d + "'"
            else:
                dp = d
            print(dp + ":")

        #now call ls for each dir
        ls_for_dir(d)

        #RECURSIVE WALK !
        if lsopt["-R"]:
            r_dirs = []
            try:
                walker = list(os.walk(d))
                for rd in walker[1:]:
                    r_dirs.append(rd[0])
            except:
                print("Recursive ERROR for:", d)

            for rd in r_dirs: # again, watch for spaces
                if " " in rd:
                    rdp = "'" + rd + "'"
                else:
                    rdp = rd
                print()
                print(rdp + ":")
                ls_for_dir(rd)

        print() # make a horizontally spacing after each dir
    #done

###########################  Here we go #########################

if __name__ == '__main__':
    #try:
    main_ls(sys.argv)
    #except:
     #   print("Fehler, vermutlich keine Berechtigung")

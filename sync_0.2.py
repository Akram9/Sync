'''
This version is very different from the earlier implementation.

The algorithm is the same as that of syncthing - synchronising the given
directories both way round but only on the same computer system. While
the earilier attempt was the same, the technologies used were making it
a tad bit complicated to maintain and develop further. As a result, the
technologies used in this case are different - builin functions to check
the time of modification of files and to compare with a central log file.
This way, the stopping and restarting of the sync function will not have any
detrimental effect on the synchronisation. An improvement from the earlier 
case is that of deleted files - in this implementation, the file deleted will
not be deleted on both sides, and rather synced both way, if it had been
modified in the interim. This is the algorithm that is used in the syncthing
implementation. This gives great freedom to even implement the software even
on portable storage devices like USB drives and thumb drives.
'''

import os.path
from subprocess import call

list1 = []      # list of all files in directory1
list2 = []      # list of all files in directory2
edit1 = []      # list of files from directory1 edited in the interim
edit2 = []      # list of ifles from directory2 edited in the interim
deleted1 = []   # list of deleted files from directory1
deleted2 = []   # list of deleted files from directory2

def dir1(file):
    print("add dir1 extension to file")

def dir2(file):
    print("add dir2 extension to file")

for i in edit1:
    if i not in deleted1:
        if i in edit2:
            if os.path.getmtime(dir1(i)) < os.path.getmtime(dir2(i)):
                cmd = f"rsync -a {dir2(i)} {dir1(i)}"
                call(cmd.split())

            else:
                cmd = f"rsync -a {dir1(i)} {dir2(i)}"
                call(cmd.split())
        
        else:
            cmd = f"rsync -a {dir1(i)} {dir2(i)}"
            call(cmd.split())

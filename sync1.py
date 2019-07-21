import os
import subprocess as sp

oldlog1 = '/home/akram/Crap/oldlog1.txt'
oldlog2 = '/home/akram/Crap/oldlog2.txt'

dir1 = '/home/akram/Crap/dir1'
dir2 = '/home/akram/Crap/dir2'


def findpath(file, dir):
    for root, dirs, files in os.walk(dir):
        if name == file:
            return(os.path.abspath(os.path.join(root, name)))


def join(dir, filename):
    nfn = dir.split('/') + filename
    nfn2 = ''
    for k in range(len(nfn)-1):
        nfn2 = nfn2 + nfn[k] + '/'
    nfn2 = nfn2 + nfn[-1]
    return(nfn2)


if os.path.isfile(oldlog1):
    with open(oldfile1) as f:
        cont1 = f.readlines()
cont1 = [x.split() for x in cont1]

if os.path.isfile(oldlog2):
    with open(oldlog2) as f:
        cont2 = f.readlines()
cont2 = [x.split() for x in cont2]

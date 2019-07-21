import os
from subprocess import call

oldlog1 = '/home/akram/Crap/oldlog1.txt'
oldlog2 = '/home/akram/Crap/oldlog2.txt'

dir1 = '/home/akram/Crap/dir1'
dir2 = '/home/akram/Crap/dir2'


def join(dir, filename):
    nfn = dir.split('/') + filename
    nfn2 = ''
    for k in range(len(nfn)-1):
        nfn2 = nfn2 + nfn[k] + '/'
    nfn2 = nfn2 + nfn[-1]
    return(nfn2)


if os.path.isfile(oldlog1):
    with open(oldlog1) as f:
        cont1 = f.readlines()
    cont1 = [x.split() for x in cont1]


if os.path.isfile(oldlog2):
    with open(oldlog2) as f:
        cont2 = f.readlines()
    cont2 = [x.split() for x in cont2]


dates1, times1, op1, obj1, paths1,  filenames1 = [], [], [], [], [], []
dates2, times2, op2, obj2, paths2,  filenames2 = [], [], [], [], [], []

modfiles, part = [], []

for i in range(len(cont1)):
    dates1.append(cont1[i][0])
    times1.append(cont1[i][1])
    op1.append(cont1[i][3])
    obj1.append(cont1[i][4])
    paths1.append(cont1[i][-1])
    filenames1.append([x for x in paths1[i].split('/') if x not in dir1.split('/')])

for i in range(len(cont2)):
    dates2.append(cont2[i][0])
    times2.append(cont2[i][1])
    op2.append(cont2[i][3])
    obj2.append(cont2[i][4])
    paths2.append(cont2[i][-1])
    filenames2.append([x for x in paths2[i].split('/') if x not in dir2.split('/')])


for i in range(len(cont1)):
    if op1[i] == "Deleted" and obj1[i] == "file:":
        if filenames1[i] in filenames2:
            date1 = dates1[i]
            time1 = times1[i]
            path1 = paths1[i]
            jlist = [j for j, x in enumerate(filenames2) if x == filenames1[i]]
            date2 = dates2[jlist[-1]]
            time2 = times2[jlist[-1]]
            path2 = paths2[jlist[-1]]

            if date1 > date2 or (date1 == date2 and time1 > time2):
                if os.path.isfile(path2):
                    cmd = f'rm {path2}'
                    call(cmd.split())

        else:
            f2 = join(dir2, filenames1[i])
            if os.path.isfile(f2):
                cmd = f'rm {f2}'
                call(cmd.split())
            # this is so as deletion of dir2/file1 could have been done before dir1/file1

    elif op1[i] == "Moved" and obj1[i] == "file:":
        if paths1[i].split('/')[-1] == cont1[i][-3].split('/')[-1]:
            file = [x for x in cont1[i][-3].split('/') if x not in dir1.split('/')]
            cmd = f'mv {join(dir2, file)} {join(dir2, filenames1[i])}'
            call(cmd.split())

        elif filenames1[i] in modfiles:
            j = modfiles.index(filenames1[i])
            if (dates1[i] > part[j][0]) or (dates1[i] == part[j][0] and times1[i] > part[j][1]):
                part[j] =  (dates1[i], times1[i], dir1)

        else:
            modfiles.append(filenames1[i])
            part.append((dates1[i], times1[i], dir1))

    elif op1[i] == "Modified" and obj1[i] == "file:":
        date1 = dates1[i]
        time1 = times1[i]
        path1 = paths1[i]
        if os.path.isfile(path1):
            if filenames1[i] in filenames2:
                jlist = [j for j, x in enumerate(filenames2) if x == filenames1[i]]
                date2 = dates2[jlist[-1]]
                time2 = times2[jlist[-1]]
                path2 = paths2[jlist[-1]]
                if date1 > date2 or (date1 == date2 and time1 > time2):
                    cmd = f'rsync -a {path1} {path2}'
                    call(cmd.split())
            elif filenames1[i] in modfiles:
                j = modfiles.index(filenames1[i])
                if (dates1[i] > part[j][1]) or (dates1[i] == part[j][1] and times1[i] > part[j][2]):
                    part[j].insert(k + 1, (dates1[i], times1[i], dir1))
            else:
                cmd = f'rsync -a {path1} {join(dir2, filenames1[i])}'
                call(cmd.split())

for i in range(len(cont2)):
    if op2[i] == "Deleted" and obj2[i] == "file:":
        if filenames2[i] in filenames1:
            date2 = dates2[i]
            time2 = times2[i]
            path2 = paths2[i]
            jlist = [j for j, x in enumerate(filenames1) if x == filenames2[i]]
            date1 = dates1[jlist[-1]]
            time1 = times1[jlist[-1]]
            path1 = paths1[jlist[-1]]

            if date2 > date1 or (date1 == date2 and time2 > time1):
                if os.path.isfile(path1):
                    cmd = f'rm {path1}'
                    call(cmd.split())

        else:
            f1 = join(dir1, filenames2[i])
            if os.path.isfile(f1):
                cmd = f'rm {f1}'
                call(cmd.split())
            # this is so as deletion of dir1/file2 could have been done before dir2/file2

    elif op2[i] == "Moved" and obj2[i] == "file:":
        if paths2[i].split('/')[-1] == cont2[i][-3].split('/')[-1]:
            file = [x for x in cont2[i][-3].split('/') if x not in dir2.split('/')]
            cmd = f'mv {join(dir1, file)} {join(dir1, filenames2[i])}'
            call(cmd.split())

        elif filenames2[i] in modfiles:
            j = modfiles.index(filenames2[i])
            if (dates2[i] > part[j][0]) or (dates2[i] == part[j][0] and times2[i] > part[j][1]):
                part[j] = (dates2[i], times2[i], dir2)

        else:
            modfiles.append(filenames2[i])
            part.append((dates2[i], times2[i], dir2))

    elif op2[i] == "Modified" and obj2[i] == "file:":
        date2 = dates2[i]
        time2 = times2[i]
        path2 = paths2[i]
        if os.path.isfile(path2):
            if filenames2[i] in filenames1:
                jlist = [j for j, x in enumerate(filenames1) if x == filenames2[i]]
                date1 = dates1[jlist[-1]]
                time1 = times1[jlist[-1]]
                path1 = paths1[jlist[-1]]
                if date2 > date1 or (date1 == date2 and time2 > time1):
                    cmd = f'rsync -a {path2} {path1}'
                    call(cmd.split())
            elif filenames2[i] in modfiles:
                j = modfiles.index(filenames2[i])
                if (dates2[i] > part[j][2]) or (dates2[i] == part[j][1] and times2[i] > part[j][2]):
                    part[j].insert(k + 1, (dates2[i], times2[i], dir2))
            else:
                cmd = f'rsync -a {path2} {join(dir1, filenames2[i])}'
                call(cmd.split())

for i in range(len(modfiles)):
    if part[i][2] == dir1:
        cmd = f'rsync -a {join(dir1, modfiles[i])} {join(dir2, modfiles[i])}'
    else:
        cmd = f'rsync -a {join(dir2, modfiles[i])} {join(dir1, modfiles[i])}'

    call(cmd.split())


cmd = f'rsync -a {dir1}/ {dir2}'
call(cmd.split())

cmd = f'rsync -a {dir2}/ {dir1}'
call(cmd.split())

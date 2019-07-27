import hashlib
import os
from subprocess import call
from rsync_alg import blockchecksums, rsyncdelta, patchstream

class Sync:
    def __init__(self, dir1, dir2, oldlog):
        self.dir1 = dir1
        self.dir2 = dir2
        self.oldlog = oldlog

    def join(self, dir, filename):
        return('/'.join([dir, '/'.join(filename)]))

    def other_dir(self, dir):
        if (dir == self.dir1):
            return(self.dir2)
        else:
            return(self.dir1)

    def patch(self, file1, file2):
        unpatched = open(file2, 'rb')
        unpatched.seek(0)
        hashes = blockchecksums(unpatched)

        patched = open(file1, 'rb')
        patched.seek(0)
        delta = rsyncdelta(patched, hashes)

        unpatched.seek(0)
        save_to = open('newfile', 'wb')
        patchstream(unpatched, save_to, delta)
        newfile.close()

    def hash_file(self, file):
        if (os.path.isfile(file)):
            sha256hash = hashlib.sha256()
            with open(file, 'rb') as f:
                for block in iter(lambda: f.read(4096), b''):
                    sha256hash.update(block)
            return(sha256hash.hexdigest())
        else:
            return('no hash')

    def sha_check(self, file1, file2):
        hash1 = self.hash_file(file1)
        hash2 = self.hash_file(file2)
        if (hash1 == hash2):
            return(True)
        else:
            return(False)

    def sync_func(self):

        if (os.path.isfile(self.oldlog)):
            with open(self.oldlog) as f:
                cont = f.readlines()
            cont = [x.split() for x in cont]

        dates, times, op, obj, paths, dir, filenames = [], [], [], [], [], [], []
        modfiles, part = [], []

        for i in range(len(cont)):
            dates.append(cont[i][0])
            times.append(cont[i][1])
            op.append(cont[i][3])
            obj.append(cont[i][4])
            paths.append(cont[i][-1])
            if (self.dir1.split('/') == paths[i].split('/')[:len(self.dir1.split('/'))]):
                filenames.append([x for x in paths[i].split('/') if x not in self.dir1.split('/')])
                dir.append(self.dir1)
            else:
                filenames.append([x for x in paths[i].split('/') if x not in self.dir2.split('/')])
                dir.append(self.dir2)

            if (op[i] == "Moved" and obj[i] == "file:"):
                file = [x for x in cont[i][-3].split('/') if x not in dir[i].split('/')]

                if (file[-1] != filenames[i][-1] and (not self.sha_check(self.join(self.other_dir(dir[i]), file), paths[i]))):
                    if (filenames[i] in modfiles):
                        j = modfiles.index(filenames[i])
                        if ((dates[i] > part[j][0]) or (dates[i] == part[j][0] and times[i] > part[j][1])):
                            part[j] =  (dates[i], times[i], dir[i])

                    else:
                        modfiles.append(filenames[i])
                        part.append((dates[i], times[i], dir[i]))

            elif (op[i] == "Modified" and obj[i] == "file:"):
                if (filenames[i] in modfiles):
                    j = modfiles.index(filenames[i])
                    if ((dates[i] > part[j][0]) or (dates[i] == part[j][0] and times[i] > part[j][1])):
                        part[j] =  (dates[i], times[i], dir[i])

                else:
                    modfiles.append(filenames[i])
                    part.append((dates[i], times[i], dir[i]))


        for i in range(len(cont)):
            if (op[i] == "Deleted" and obj[i] == "file:"):
                jlist = [j for j, x in enumerate(filenames) if x == filenames[i]]
                if (jlist[-1] == i):
                    dirc = self.other_dir(dir[i])
                    file = self.join(dirc, filenames[i])
                    if (os.path.isfile(file)):
                        cmd = f'rm {file}'
                        call(cmd.split())

            elif (op[i] == "Moved" and obj[i] == "file:"):
                file = [x for x in cont[i][-3].split('/') if x not in dir[i].split('/')]
                if (cont[i][-3].split('/')[-1] == filenames[i][-1]):
                    dirc = self.other_dir(dir[i])
                    if (os.path.isfile(self.join(dirc, file))):
                        cmd = f'mv {self.join(dirc, file)} {self.join(dirc, filenames[i])}'
                        call(cmd.split())

                        if (file in modfiles):
                            j = modfiles.index(file)
                            if (filenames[i] in modfiles):
                                k = modfiles.index(filenames[i])
                                if ((part[k][0] > part[j][0]) or (part[k][0] == part[j][0] and part[k][1] > part[j][1])):
                                    del modfiles[j]
                                    del part[j]
                                else:
                                    del modfiles[k]
                                    del part[k]
                                    modfiles[j] = filenames[i]
                            else:
                                modfiles[j] = filenames[i]

                elif (self.sha_check(self.join(self.other_dir(dir[i]), file), paths[i])):
                    dirc = self.other_dir(dir[i])
                    file = [x for x in cont[i][-3].split('/') if x not in dir[i].split('/')]
                    if (os.path.isfile(self.join(dirc, file))):
                        cmd = f'mv {self.join(dirc, file)} {self.join(dirc, filenames[i])}'
                        call(cmd.split())

                        if (file in modfiles):
                            j = modfiles.index(file)
                            if (filenames[i] in modfiles):
                                k = modfiles.index(filenames[i])
                                if ((part[k][0] > part[j][0]) or (part[k][0] == part[j][0] and part[k][1] > part[j][1])):
                                    del modfiles[j]
                                    del part[j]
                            else:
                                modfiles[j] = filenames[i]

        for i in range(len(modfiles)):
            if part[i][2] == self.dir1:
                if os.path.isfile(self.join(self.dir1, modfiles[i])):
                    cmd = f'rsync -a {self.join(self.dir1, modfiles[i])} {self.join(self.dir2, modfiles[i])}'
                    call(cmd.split())
            else:
                if os.path.isfile(self.join(self.dir2, modfiles[i])):
                    cmd = f'rsync -a {self.join(self.dir2, modfiles[i])} {self.join(self.dir1, modfiles[i])}'
                    call(cmd.split())

        cmd = f'rsync -a {self.dir1}/ {self.dir2}'
        call(cmd.split())

        cmd = f'rsync -a {self.dir2}/ {self.dir1}'
        call(cmd.split())

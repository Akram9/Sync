from os import lisdir
from os.path import isfile, isdir, join

class watch:
    def __init__(self, dirname):
        self.dirname = dirname

    # function for noting down all the checksums for the files to be found
    def note(self):
        if not isfile('../note.txt'):
            note = open('../note.txt', 'w')

    # function to get all the filenames in the given directory
    def watcher(self, self.dirname):
        if isdir(self.dirname):
            a = listdir(self.dirname)
            b = a[:]

            while a:
                a = []
                for i in b:
                    if isdir(join(self.dirname, i)):
                        a.append(i)

                b = a[:]

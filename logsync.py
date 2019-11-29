#import os
#from multiprocessing import Pool
from subprocess import run
'''
import os
import time
import logging
from multiprocessing import Pool

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

import sync

def log(tup):
    log, oldlog, dir = tup[0], tup[1], tup[2]
    if __name__ == "__main__":

        logging.basicConfig(filename=log, filemode='w',
                            level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        event_handler = LoggingEventHandler()
        observer = Observer()
        observer.schedule(event_handler, dir, recursive=True)
        observer.start()

        time.sleep(200)

        if os.path.isfile(oldlog1):
            with open(oldlog1) as f:
                cont1 = f.readlines()
            # code hunk for sync
            # needs to include time wait
            # watchdog is not going to wait for file shifting


        cmd = f'cp {log} {oldlog}'
        os.system(cmd)
        print('--end--')
        file = open(log, 'w')
        file.close()

log1 = '/home/akram/Crap/log1.txt'
oldlog1 = '/home/akram/Crap/oldlog1.txt'
dir1 = '/home/akram/Crap/dir1/'
log2 = '/home/akram/Crap/log2.txt'
oldlog2 = '/home/akram/Crap/oldlog2.txt'
dir2 = '/home/akram/Crap/dir2/'
'''
'''
if __name__ == '__main__':
    pool = Pool(processes = 2)
    all = ('watch1.py', 'watch2.py')
    def cmd(x):
        os.system(f'python3 {x}')
    pool.map(cmd, all)

def cmd(x):
    os.system(f'python3 {x}')
'''
run("python3 watch1.py & python3 watch2.py", shell=True)

import logging
import threading
import time
from subprocess import call
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from singlesync import Sync


if __name__ == "__main__":

    dir1 = '/media/akram/Safe/Ubuntu/Unsplash'
    dir2 = '/media/akram/Kingston32/Unsplash'
    log = 'unlog.txt'
    oldlog = 'unoldlog.txt'

    logging.basicConfig(filename=log, filemode='w', level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    event_handler = LoggingEventHandler()
    observer = Observer()
    paths = [dir1, dir2]
    threads =[]

    for i in paths:
        targetpath = str(i)
        observer.schedule(event_handler, targetpath, recursive=True)
        threads.append(observer)

    observer.start()

    try:
        while True:
            time.sleep(60)
            cmd = f'cp {log} {oldlog}'
            call(cmd.split())
            a = Sync(dir1, dir2, oldlog)
            a.sync_func()
            with open(log, 'w'): pass

    except KeyboardInterrupt:
        observer.stop()
    observer.join()

import logging
import threading
import time
from subprocess import call
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from singlesync import Sync


if __name__ == "__main__":

    dir1 = input("Enter first directory destination: ")
    dir2 = input("Enter second directory destination: ")
    log = "log.txt"
    oldlog = "oldlog.txt"

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
            time.sleep(50)
            cmd = f'cp {log} {oldlog}'
            call(cmd.split())
            a = Sync(dir1, dir2, oldlog)
            a.sync_func()
            with open(log, 'w'): pass

    except KeyboardInterrupt:
        observer.stop()
    observer.join()

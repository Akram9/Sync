# sync
A syncthing-like sync system to keep folders in the same computer always in sync. The folders mirror each other for the time the program is running.
Changes made in the folders while the program is not running are not checked for now. See issue 3 regarding the same.

Linux-only for now.

Both the files - watch.py and singlesync.py are needed to accomplish syncing. It does not neglect hidden files or directories for now.
Running watch.py should start the syncing mechnism in the terminal.
The required logfiles are, by default, saved in the parent directory to which the files are saved in. To change this, edit `watch.py` lines 14-15 and set the desired location of log files. Both log and oldlog files are required. They can be stored in different locations if needed.

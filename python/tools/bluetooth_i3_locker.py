#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------

""" Simple tool to auto-lock PC checking range of bluetooth device """

__author__ = 'Tadeusz Miszczyk'
__version__ = "1.1.0"

# ----------------------------------------------------------------------------------------------------------------------

import os
import sys
import threading
import time

if sys.version_info < (3, 0, 0):
    import Queue as queue
else:
    import queue

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + '/../library/')
import mylib.system
import mylib.variables_sensitive
from myext.bt_proximity.bt_rssi import BluetoothRSSI

# ----------------------------------------------------------------------------------------------------------------------


class Process(threading.Thread):
    def __init__(self, cmd, queue):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.queue = queue

    def run(self):
        (status, output) = mylib.system.run_command(self.cmd)
        self.queue.put((self.cmd, output, status))

# ----------------------------------------------------------------------------------------------------------------------


def get_locker_background_wallpaper(source_folder):
    """
    This function returns path to graphic image for locker
    for all monitors
    :param  source_folder:Path to folder with graphics for locker like :
             /home/username/Images/locker/
    :return: path to locker wallpaper like :
             /home/username/Images/locker/1920x1080.1680x1050.png
    """
    wallpaper_path = "{0}{1}{2}".format(
        source_folder,
        '.'.join([mylib.system.get_monitor_size(mylib.system.monitor_object(), mon) for mon in range(
            mylib.system.get_monitors_number(mylib.system.monitor_object()))]),
        ".png")

    return wallpaper_path

# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    LOCK_COMMAND = LOCK_APP = "i3lock"
    UNLOCK_COMMAND = "kill -9 $(ps aux | grep %s | grep -v grep | awk '{print $2}')" % LOCK_APP
    user_in_range = -10

    locker_background = get_locker_background_wallpaper(mylib.variables_sensitive.LOCKER_TEMPLATES_FOLDER)
    LOCK_COMMAND += " -i {0}".format(locker_background) if os.path.exists(locker_background) else ''

    queue = queue.Queue()
    try:
        while True:
            btrssi = BluetoothRSSI(addr=mylib.variables_sensitive.BT_DEVICE_UNLOCK_ADDRESS)
            device_in_range = btrssi.get_rssi()
            locked_workstation = mylib.system.is_locked(locker_name=LOCK_APP)

            if device_in_range is not None and device_in_range >= user_in_range:
                if locked_workstation:
                    tunlock = Process(UNLOCK_COMMAND, queue)
                    tunlock.start()
            else:
                if not locked_workstation:
                    tlock = Process(LOCK_COMMAND, queue)
                    tlock.start()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Ended by user")
